from datetime import datetime
from json import dumps, loads
import logging

from database.models import (
    Advantages,
    Contacts,
    Feedback,
    Functionalities,
    Interface,
    Opportunities,
    User,
    async_session,
)

from misc import redis
from sqlalchemy import select


logger = logging.getLogger(__name__)

async def get_answer_data(command) -> list:
    db_commands = {
        'advantages': Advantages,
        'contacts': Contacts,
        'opportunities': Opportunities,
        'functionality': Functionalities,
        'interface': Interface,
        }
    command = command.replace('/', '').split()[0]

    result = await redis.get(command)
    if result is not None:
        result = loads(result)

    if not result:
        async with async_session() as session:
            records = await session.scalars(select(db_commands[command]))
            result = [{'text': record.text, 'image_name': record.image_name} for record in records]

            if result:
                logger.info(f'Get "{command}" command from DB.')
            else:
                logger.error(f'"{command}" data not in DB!!!')
                return [{'text': 'The data is temporarily unavailable.', 'image_name': None}]

            await redis.set(command, dumps(result))
            await redis.expire(command, 3600)
            logger.info(f'Set answer to "{command}" command to Redis.\nReturn answer to "{command}" command from DB!')
            return result
    logger.info(f'Return answer to "{command}" command from Redis!')
    return result

async def add_default_answers_to_db() -> None:
    try:
        from lexicon.lexicon_answers import (
            LEXICON_ADVANTAGES,
            LEXICON_CONTACTS,
            LEXICON_FUNCTIONALITY,
            LEXICON_INTERFACE,
            LEXICON_OPPORTUNITIES,
        )
    except ModuleNotFoundError:
        logger.error('There is no default data to add to the database!!!')
        return

    models_and_deafult_data = [
        {'model': Advantages, 'data': LEXICON_ADVANTAGES},
        {'model': Contacts, 'data': LEXICON_CONTACTS},
        {'model': Opportunities, 'data': LEXICON_OPPORTUNITIES},
        {'model': Functionalities, 'data': LEXICON_FUNCTIONALITY},
        {'model': Interface, 'data': LEXICON_INTERFACE},
    ]

    async with async_session() as session:
        for table in models_and_deafult_data:
            model_data = await session.scalar(select(table['model']))
            if model_data is None:
                for data in table['data']:
                    session.add(
                        table['model'](
                            text=data['text'],
                            image_name=data['image_name']
                        )
                    )

        if len(session.new):
            logger.info("Commit default data to DB.")
            await session.commit()

async def add_user_data_to_db(message, user_data: dict[str, str], localized_time: datetime, validated_phone: str) -> None:
    async with async_session() as session:
        select_command = select(User).where(User.tg_id == message.from_user.id)
        some_user = await session.scalar(select_command)
        if some_user is None:
            session.add(User(
            tg_id=message.from_user.id,
            created_on=localized_time,
            feedbacks=[Feedback(
                is_bot=message.from_user.is_bot,
                tg_nickname=message.from_user.first_name,
                name=user_data['name'],
                mail=user_data['email'],
                phone=validated_phone,
                created_on=localized_time,
                appeal=user_data['text']
            )]))
            logger.info(f'Add new user and feedback with tg_id - "{message.from_user.id}" to DB.')
        else:
            session.add(Feedback(
                user_id=some_user.id,
                is_bot=message.from_user.is_bot,
                tg_nickname=message.from_user.first_name,
                name=user_data['name'],
                mail=user_data['email'],
                phone=validated_phone,
                created_on=localized_time,
                appeal=user_data['text']
                ))
            logger.info(f'Add new feedback from user with tg_id - "{message.from_user.id}" to DB.')

        await session.commit()
