import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


logger = logging.getLogger(__name__)

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int = 1) -> None:
        self.limit = TTLCache(maxsize=10000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if event.chat.id in self.limit:
            logger.warning(f'Spam (update id={data["event_update"].update_id}) from user tg_id={event.from_user.id} was detected.')
            return

        self.limit[event.chat.id] = None
        return await handler(event, data)
