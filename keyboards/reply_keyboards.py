from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon_data import REPLY_BUTTON_COMMANDS


def create_reply_kb(*args: str) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []

    for button in args:
        buttons.append(
            KeyboardButton(
                text=REPLY_BUTTON_COMMANDS[button] if button in REPLY_BUTTON_COMMANDS else button,
            )
        )

    kb_builder.row(*buttons, width=1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
