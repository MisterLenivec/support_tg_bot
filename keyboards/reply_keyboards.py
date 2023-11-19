from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import INFO_BUTTONS


kb_builder = ReplyKeyboardBuilder()

buttons: list[KeyboardButton] = [
    KeyboardButton(text=button) for button in INFO_BUTTONS
]

kb_builder.row(*buttons, width=2)

info_keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)
