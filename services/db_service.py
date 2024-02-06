from datetime import datetime
from json import dumps, loads
from aiogram.types import Message
import logging

from database.models import (
    Advantage,
    Contact,
    Feedback,
    Functionality,
    Interface,
    Opportunity,
    User,
    ButtonAnswer,
    MenuButton,
    InlineButton,
    ReplyCancelButton,
    async_session,
)

from misc import redis
from sqlalchemy import select


logger = logging.getLogger(__name__)


async def get_cached_buttons(buttons: list[str]) -> tuple[dict[str, str], list[str]]:
    result = {}
    list_of_buttons = buttons
    for button in list_of_buttons:
        button_answer = await redis.get(button)
        if button_answer:
            result.update({button: button_answer})

    [list_of_buttons.remove(cached_button) for cached_button in result]

    return result, list_of_buttons

async def get_menu_buttons() -> list[dict[str, str]]:
    async with async_session() as session:
        records = await session.scalars(select(MenuButton))
        result = [{record.command: record.answer} for record in records]
        return result

async def get_buttons_data(buttons: list[str], table: InlineButton | ReplyCancelButton) -> dict[str, str]:
    result, buttons_not_in_cache = await get_cached_buttons(buttons)

    if buttons_not_in_cache:
        async with async_session() as session:
            for button in buttons_not_in_cache:
                btn = await session.scalar(select(table).where(table.command == button))
                if btn is None:
                    logger.error(f'"{button}" data from table \"{table.__table__}\" not in DB!!!')
                    result.update({button: button})
                else:
                    logger.info(f'Get "{button}" command from DB.')
                    logger.info(f'Set answer to "{button}" command to Redis.\nReturn answer to "{button}" command from DB!')
                    await redis.set(button, btn.answer)
                    await redis.expire(button, 3600)
                    result.update({btn.command: btn.answer})

    return result

async def get_command_answer(command: str) -> str:
    command = command.split()[0]
    result = await redis.get(command)
    if not result:
        async with async_session() as session:
            records = await session.scalars(select(ButtonAnswer))
            result: str = ''.join(record.answer for record in records if record.command == command)

            if result:
                logger.info(f'Get "{command}" command from DB.')
            else:
                logger.error(f'"{command}" from table \"{ButtonAnswer.__table__}\" data not in DB!!!')
                return 'The data is temporarily unavailable.'

            await redis.set(command, result)
            await redis.expire(command, 3600)
            logger.info(f'Set answer to "{command}" command to Redis.\nReturn answer to "{command}" command from DB!')
            return result
    logger.info(f'Return answer to "{command}" command from Redis!')
    return result

async def get_answer_data(command: str) -> list:
    db_commands = {
        'advantages': Advantage,
        'contacts': Contact,
        'opportunities': Opportunity,
        'functionality': Functionality,
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
            LEXICON_MAIN_MENU_ANSWERS,
            LEXICON_MAIN_MENU_COMMANDS,
            INLINE_BUTTON_COMMANDS,
            REPLY_CANCEL_BUTTON_COMMANDS,
        )
    except ModuleNotFoundError:
        logger.exception('There is no default data to add to the database!!!')
        return
    except ImportError:
        logger.exception('There is no default data for one of the tables to add to the database!!!')
        return

    text_image_models = [
        {'model': Advantage, 'data': LEXICON_ADVANTAGES},
        {'model': Contact, 'data': LEXICON_CONTACTS},
        {'model': Opportunity, 'data': LEXICON_OPPORTUNITIES},
        {'model': Functionality, 'data': LEXICON_FUNCTIONALITY},
        {'model': Interface, 'data': LEXICON_INTERFACE}
    ]

    command_answers_models = [
        {'model': ButtonAnswer, 'data': LEXICON_MAIN_MENU_ANSWERS},
        {'model': MenuButton, 'data': LEXICON_MAIN_MENU_COMMANDS},
        {'model': InlineButton, 'data': INLINE_BUTTON_COMMANDS},
        {'model': ReplyCancelButton, 'data': REPLY_CANCEL_BUTTON_COMMANDS}
    ]

    async with async_session() as session:
        for table in text_image_models:
            model_data = await session.scalar(select(table['model']))
            if model_data is None:
                for data in table['data']:
                    session.add(
                        table['model'](
                            text=data['text'],
                            image_name=data['image_name']
                        )
                    )

        for table in command_answers_models:
            model_data = await session.scalar(select(table['model']))
            if model_data is None:
                for command_data, answer_data in table['data'].items():
                    session.add(
                        table['model'](
                            command=command_data,
                            answer=answer_data
                        )
                    )

        if len(session.new):
            logger.info("Commit default data to DB.")
            await session.commit()

async def add_user_data_to_db(message: Message, user_data: dict[str, str], localized_time: datetime, validated_phone: str) -> None:
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
