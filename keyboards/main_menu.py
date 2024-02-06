import logging

from aiogram import Bot
from aiogram.types import BotCommand
from services.db_service import get_menu_buttons


logger = logging.getLogger(__name__)

# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    logger.info('Prepare main menu keyboard.')
    buttons = await get_menu_buttons()
    main_menu_commands = []
    for button in buttons:
        for command, description in button.items():
            main_menu_commands.append(BotCommand(command=command, description=description))

    await bot.set_my_commands(main_menu_commands)
    logger.info('The main menu keyboard was installed.')
