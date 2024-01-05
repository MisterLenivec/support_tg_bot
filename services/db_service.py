from datetime import datetime
from json import dumps, loads

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
from lexicon.lexicon_answers import (
    LEXICON_ADVANTAGES,
    LEXICON_CONTACTS,
    LEXICON_FUNCTIONALITY,
    LEXICON_INTERFACE,
    LEXICON_OPPORTUNITIES,
)
from misc import redis
from sqlalchemy import select


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
    if not result:
        async with async_session() as session:
            records = await session.scalars(select(db_commands[command]))
            result = [{'text': record.text, 'image_name': record.image_name} for record in records]
            await redis.set(command, dumps(result))
            await redis.expire(command, 3600)
            return result
    return loads(result)

async def add_default_answers_to_db():
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

        await session.commit()
