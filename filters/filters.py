from re import match, compile

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCorrectEmail(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return match(r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$", message.text) is not None


class IsCorrectPhoneNumber(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        re_phone = compile(r"^(\+)?(7|8)?[-\s]?\(?[489][0-9]{2}\)?[-\s]?[0-9]{2,3}[-\s]?[0-9]{2}[-\s]?[0-9]{2}$")
        return re_phone.match(message.text) is not None
