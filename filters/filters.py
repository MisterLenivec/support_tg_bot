from re import match

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCorrectEmail(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return match(r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$", message.text) is not None


class IsCorrectPhoneNumber(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return match(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message.text) is not None
