
from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types import FSInputFile

from lexicon.lexicon_data import (LEXICON_ANSWERS, LEXICON_ADVANTAGES,
                                  LEXICON_CONTACTS)
# from keyboards.reply_keyboards import info_keyboard
from keyboards.inline_keyboards import create_inline_kb


router = Router()


@router.message(Command(commands=['start', 'menu']))
async def process_base_commands(message: Message):
    keyboard = create_inline_kb('info', 'advantages', 'contacts')
    await message.answer(LEXICON_ANSWERS[message.text.split()[0]], reply_markup=keyboard)


@router.message(Command(commands='info'))
async def process_info_command(message: Message):
    keyboard = create_inline_kb('opportunities', 'functionality', 'interface')
    await message.answer(LEXICON_ANSWERS['/info'], reply_markup=keyboard)


@router.message(Command(commands='contacts'))
async def process_contacts_command(message: Message):
    photo = FSInputFile(LEXICON_CONTACTS['photo'])
    keyboard = create_inline_kb('info', 'advantages')
    await message.answer_photo(photo, caption=LEXICON_CONTACTS['contacts'], reply_markup=keyboard)


@router.message(Command(commands=['home_assistant', 'docs_install']))
async def process_links_commands(message: Message):
    keyboard = create_inline_kb('info', 'advantages', 'contacts')
    await message.answer(LEXICON_ANSWERS[message.text.split()[0]], reply_markup=keyboard)


@router.message(Command(commands='operator'))
async def process_operator_command(message: Message):
    await message.answer(LEXICON_ANSWERS['/operator'])


# @router.message(Command(commands='advantages'))
# async def process_advantages_command(message: Message):
#     photo = FSInputFile(LEXICON_ADVANTAGES['photo'])
#     await message.answer_photo(photo)
#     for advantage in LEXICON_ADVANTAGES['advantages']:
#         await sleep(1)
#         await message.answer(advantage)
