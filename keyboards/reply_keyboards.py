from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from services.db_service import get_buttons_data
from database.models import ReplyCancelButton


async def create_reply_kb(*args: tuple[str] | str) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []

    requested_buttons = list(args)
    buttons_dict = await get_buttons_data(requested_buttons, ReplyCancelButton)
    for button in buttons_dict:
        buttons.append(KeyboardButton(text=buttons_dict[button]))

    kb_builder.row(*buttons, width=1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
