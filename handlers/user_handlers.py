from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types import FSInputFile

from lexicon.lexicon_data import (LEXICON_ANSWERS, LEXICON_ADVANTAGES, LEXICON_CONTACTS, LEXICON_OPPORTUNITIES,
                                  LEXICON_FUNCTIONALITY, LEXICON_INTERFACE, LEXICON_ADVANTAGES)
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


# Хэндлеры срабатывающие на CallbackQuery (Инлайн кнопки)

@router.callback_query(F.data == 'info')
async def process_info_button(callback: CallbackQuery):
    keyboard = create_inline_kb('opportunities', 'functionality', 'interface')
    await callback.message.answer(text=LEXICON_ANSWERS['/info'], reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == 'opportunities')
async def process_opportunities_button(callback: CallbackQuery):
    for photo, opportunity in zip(LEXICON_OPPORTUNITIES['photos'], LEXICON_OPPORTUNITIES['opportunities']):
        photo_file = FSInputFile(photo)
        if LEXICON_OPPORTUNITIES['photos'][-1] == photo:  # Костыли-костылики
            keyboard = create_inline_kb('functionality', 'interface', 'advantages')
            await callback.message.answer_photo(photo_file, caption=opportunity, reply_markup=keyboard)
        else:
            await callback.message.answer_photo(photo_file, caption=opportunity)
            await sleep(.3)

    await callback.answer()


@router.callback_query(F.data == 'functionality')
async def process_functionality_button(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_FUNCTIONALITY['functionality'][0])
    for photo, functionality in zip(LEXICON_FUNCTIONALITY['photos'], LEXICON_FUNCTIONALITY['functionality'][1:]):
        photo_file = FSInputFile(photo)
        if LEXICON_FUNCTIONALITY['photos'][-1] == photo:  # Костыли-костылики
            keyboard = create_inline_kb('opportunities', 'interface', 'advantages')
            await callback.message.answer_photo(photo_file, caption=functionality, reply_markup=keyboard)
        else:
            await callback.message.answer_photo(photo_file, caption=functionality)
            await sleep(.3)

    await callback.answer()


@router.callback_query(F.data == 'interface')
async def process_interface_button(callback: CallbackQuery):
    for photo, interface in zip(LEXICON_INTERFACE['photos'], LEXICON_INTERFACE['interface']):
        photo_file = FSInputFile(photo)
        if LEXICON_INTERFACE['photos'][-1] == photo:  # Костыли-костылики
            keyboard = create_inline_kb('opportunities', 'functionality')
            await callback.message.answer_photo(photo_file, caption=interface, reply_markup=keyboard)
        else:
            await callback.message.answer_photo(photo_file, caption=interface)
            await sleep(.3)

    await callback.answer()


@router.callback_query(F.data == 'contacts')
async def process_contacts_button(callback: CallbackQuery):
    photo_file = FSInputFile(LEXICON_CONTACTS['photo'])
    keyboard = create_inline_kb('info', 'advantages')
    await callback.message.answer_photo(photo_file, caption=LEXICON_CONTACTS['contacts'], reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == 'advantages')
async def process_advantages_button(callback: CallbackQuery):
    photo_file = FSInputFile(LEXICON_ADVANTAGES['photo'])
    await callback.message.answer_photo(photo_file, caption=LEXICON_ADVANTAGES['advantages'][0])
    await sleep(.3)
    keyboard = create_inline_kb('info', 'contacts')
    await callback.message.answer(text=LEXICON_ADVANTAGES['advantages'][1], reply_markup=keyboard)
    await callback.answer()
