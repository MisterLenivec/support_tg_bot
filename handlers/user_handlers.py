from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, FSInputFile, Message, ReplyKeyboardRemove
from config_data.config import FeedbackDialog, FSMFillForm

from keyboards.reply_keyboards import create_reply_kb
from keyboards.inline_keyboards import create_inline_kb
from lexicon.lexicon_data import (
    LEXICON_ADVANTAGES,
    LEXICON_ANSWERS,
    LEXICON_CONTACTS,
    LEXICON_FUNCTIONALITY,
    LEXICON_INTERFACE,
    LEXICON_OPPORTUNITIES,
    REPLY_BUTTON_COMMANDS,
    BASE_COMMANDS
)

router = Router()


# Этот хэндлер будет срабатывать на команду "/cancel_feedback" в состоянии заполнения обращения,
# и отключать машину состояний
@router.message(F.text == REPLY_BUTTON_COMMANDS["cancel_feedback"], StateFilter(FSMFillForm))
async def process_cancel_feedback_command(message: Message, state: FSMContext):
    await message.answer(text="Вы отменили заполнение обращения.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel_operator" в состоянии диалога с оператором,
# и отключать машину состояний
@router.message(F.text == REPLY_BUTTON_COMMANDS["cancel_operator"], StateFilter(FeedbackDialog))
async def process_cancel_operator_command(message: Message, state: FSMContext):
    await message.answer(text="Вы завершили общение с оператором.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Вообще два нижних хандлера бы объеденить в один с проврекой на не дефолт стейт,
# но тогда нужно придумать универсальное сообщение подходящее для обоих случаев.
# Тут будем игнорировать нажатия на меню кнопки во время заполнения формы.
@router.message(Command(commands=BASE_COMMANDS), StateFilter(FSMFillForm))
async def process_ignore_comands_in_fillform(message: Message):
    await message.answer(
        "Команды недоступны во время заполнения обращения.\n"
        f"Если вы хотите отменить заполнение, нажмите кнопку \"{REPLY_BUTTON_COMMANDS['cancel_feedback']}\" "
        "сразу под строкой ввода."
        )


# Тут будем игнорировать нажатия на меню кнопки во время диалога с оператором.
@router.message(Command(commands=BASE_COMMANDS), StateFilter(FeedbackDialog))
async def process_ignore_commands_in_dialog(message: Message):
    await message.answer(
        "Команды недоступны во время диалога с оператором.\n"
        f"Если вы хотите выйти из диалога, нажмите кнопку \"{REPLY_BUTTON_COMMANDS['cancel_operator']}\" "
        "сразу под строкой ввода."
        )


# Тут будем игнорировать нажатия на инлайн кнопки во время включенной машины состояний.
@router.callback_query(F.data.in_({
    "info", "opportunities", "functionality", "interface", "contacts", "advantages"
    }), ~StateFilter(default_state))
async def process_ignore_calback_action(callback: CallbackQuery):
    await callback.answer()


# Этот хэндлер будет срабатывать на команду /operator
# и переводить бота в состояние диалога с оператором
@router.message(Command(commands="operator"), StateFilter(default_state))
async def process_operator_command(message: Message, state: FSMContext):
    keyboard = create_reply_kb("cancel_operator")
    await message.answer(LEXICON_ANSWERS["/operator"], reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FeedbackDialog.support)


# Этот хэндлер будет срабатывать на команду /send_feedback
# и переводить бота в состояние ожидания ввода имени
@router.message(Command(commands="send_feedback"), StateFilter(default_state))
async def process_send_feedback_command(message: Message, state: FSMContext):
    keyboard = create_reply_kb("cancel_feedback")
    await message.answer(text="Пожалуйста, введите ваше имя.", reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


@router.message(Command(commands=["start", "menu"]))
async def process_base_commands(message: Message):
    keyboard = create_inline_kb("info", "advantages", "contacts")
    await message.answer(LEXICON_ANSWERS[message.text.split()[0]], reply_markup=keyboard)


@router.message(Command(commands="info"))
async def process_info_command(message: Message):
    keyboard = create_inline_kb("opportunities", "functionality", "interface")
    await message.answer(LEXICON_ANSWERS["/info"], reply_markup=keyboard)


@router.message(Command(commands="contacts"))
async def process_contacts_command(message: Message):
    photo = FSInputFile(LEXICON_CONTACTS["photo"])
    keyboard = create_inline_kb("info", "advantages")
    await message.answer_photo(photo, caption=LEXICON_CONTACTS["contacts"], reply_markup=keyboard)


@router.message(Command(commands=["home_assistant", "docs_install"]))
async def process_links_commands(message: Message):
    keyboard = create_inline_kb("info", "advantages", "contacts")
    await message.answer(LEXICON_ANSWERS[message.text.split()[0]], reply_markup=keyboard)


# Хэндлеры срабатывающие на CallbackQuery (Инлайн кнопки)


@router.callback_query(F.data == "info")
async def process_info_button(callback: CallbackQuery):
    keyboard = create_inline_kb("opportunities", "functionality", "interface")
    await callback.message.answer(text=LEXICON_ANSWERS["/info"], reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "opportunities")
async def process_opportunities_button(callback: CallbackQuery):
    for photo, opportunity in zip(LEXICON_OPPORTUNITIES["photos"], LEXICON_OPPORTUNITIES["opportunities"]):
        photo_file = FSInputFile(photo)
        if LEXICON_OPPORTUNITIES["photos"][-1] == photo:  # Костыли-костылики
            keyboard = create_inline_kb("functionality", "interface", "advantages")
            await callback.message.answer_photo(photo_file, caption=opportunity, reply_markup=keyboard)
        else:
            await callback.message.answer_photo(photo_file, caption=opportunity)
            await sleep(0.3)

    await callback.answer()


@router.callback_query(F.data == "functionality")
async def process_functionality_button(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_FUNCTIONALITY["functionality"][0])
    for photo, functionality in zip(LEXICON_FUNCTIONALITY["photos"], LEXICON_FUNCTIONALITY["functionality"][1:]):
        photo_file = FSInputFile(photo)
        if LEXICON_FUNCTIONALITY["photos"][-1] == photo:  # Костыли-костылики
            keyboard = create_inline_kb("opportunities", "interface", "advantages")
            await callback.message.answer_photo(photo_file, caption=functionality, reply_markup=keyboard)
        else:
            await callback.message.answer_photo(photo_file, caption=functionality)
            await sleep(0.3)

    await callback.answer()


@router.callback_query(F.data == "interface")
async def process_interface_button(callback: CallbackQuery):
    for photo, interface in zip(LEXICON_INTERFACE["photos"], LEXICON_INTERFACE["interface"]):
        photo_file = FSInputFile(photo)
        if LEXICON_INTERFACE["photos"][-1] == photo:  # Костыли-костылики
            keyboard = create_inline_kb("opportunities", "functionality")
            await callback.message.answer_photo(photo_file, caption=interface, reply_markup=keyboard)
        else:
            await callback.message.answer_photo(photo_file, caption=interface)
            await sleep(0.3)

    await callback.answer()


@router.callback_query(F.data == "contacts")
async def process_contacts_button(callback: CallbackQuery):
    photo_file = FSInputFile(LEXICON_CONTACTS["photo"])
    keyboard = create_inline_kb("info", "advantages")
    await callback.message.answer_photo(photo_file, caption=LEXICON_CONTACTS["contacts"], reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "advantages")
async def process_advantages_button(callback: CallbackQuery):
    photo_file = FSInputFile(LEXICON_ADVANTAGES["photo"])
    await callback.message.answer_photo(photo_file, caption=LEXICON_ADVANTAGES["advantages"][0])
    await sleep(0.3)
    keyboard = create_inline_kb("info", "contacts")
    await callback.message.answer(text=LEXICON_ADVANTAGES["advantages"][1], reply_markup=keyboard)
    await callback.answer()
