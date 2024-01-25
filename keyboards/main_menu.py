import logging

from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon_data import LEXICON_MAIN_MENU_COMMANDS


logger = logging.getLogger(__name__)

# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    logger.info('Prepare main menu keyboard.')
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_MAIN_MENU_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)
    logger.info('The main menu keyboard was installed.')
