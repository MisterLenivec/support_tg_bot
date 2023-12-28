from asyncio import sleep
from pathlib import Path

from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, Message
from bot import PICTURES_PATH
from services.db_service import get_answer_data


async def make_callback_response(callback: CallbackQuery, keyboard: InlineKeyboardMarkup, command_name: str) -> None:
    records = await get_answer_data(command_name)
    for idx, record in enumerate(records, start=1):
        photo_file = FSInputFile(Path.joinpath(PICTURES_PATH, record['image_name'])) if record['image_name'] else None
        if len(records) == idx:
            if photo_file is not None:
                await callback.message.answer_photo(photo_file, caption=record['text'], reply_markup=keyboard)
            else:
                await callback.message.answer(text=record['text'], reply_markup=keyboard)
        else:
            if photo_file is not None:
                await callback.message.answer_photo(photo_file, caption=record['text'])
            else:
                await callback.message.answer(text=record['text'])
            await sleep(0.3)

    await callback.answer()


async def make_message_response(message: Message, keyboard: InlineKeyboardMarkup) -> None:
    records = await get_answer_data(message.text)
    for idx, record in enumerate(records, start=1):
        photo_file = FSInputFile(Path.joinpath(PICTURES_PATH, record['image_name'])) if record['image_name'] else None
        if len(records) == idx:
            if photo_file is not None:
                await message.answer_photo(photo_file, caption=record['text'], reply_markup=keyboard)
            else:
                await message.answer(text=record['text'], reply_markup=keyboard)
        else:
            if photo_file is not None:
                await message.answer_photo(photo_file, caption=record['text'])
            else:
                await message.answer(text=record['text'])
            await sleep(0.3)
