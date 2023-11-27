from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_data import INLINE_BUTTON_COMMANDS


def create_inline_kb(*args: str, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=INLINE_BUTTON_COMMANDS[button] if button in INLINE_BUTTON_COMMANDS else button,
                    callback_data=button,
                )
            )
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup(resize_keyboard=True)
