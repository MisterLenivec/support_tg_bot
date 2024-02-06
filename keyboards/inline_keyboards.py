from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import InlineButton
from services.db_service import get_buttons_data


async def create_inline_kb(*args: tuple[str], **kwargs: dict[str, str]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        requested_buttons = list(args)
        buttons_dict = await get_buttons_data(requested_buttons, InlineButton)
        for button, text in buttons_dict.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button,))

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup(resize_keyboard=True)
