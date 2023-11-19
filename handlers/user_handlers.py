
from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types import FSInputFile

from lexicon.lexicon import LEXICON_ANSWERS, LEXICON_ADVANTAGES
from keyboards.reply_keyboards import info_keyboard


router = Router()


@router.message(Command(commands=['start', 'menu', 'home_assistant', 'docs_install']))
async def process_base_commands(message: Message):
    await message.answer(LEXICON_ANSWERS[message.text.split()[0]])


@router.message(Command(commands='info'))
async def process_info_command(message: Message):
    await message.answer(LEXICON_ANSWERS['/info'], reply_markup=info_keyboard)


@router.message(Command(commands='advantages'))
async def process_advantages_command(message: Message):
    photo = FSInputFile(LEXICON_ADVANTAGES['photo'])
    await message.answer_photo(photo)
    for advantage in LEXICON_ADVANTAGES['advantages']:
        await sleep(1)
        await message.answer(advantage)
