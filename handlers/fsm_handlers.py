from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from config_data.config import FeedbackDialog, FSMFillForm
from filters.filters import IsCorrectEmail, IsCorrectPhoneNumber
from keyboards.reply_keyboards import create_reply_kb
from services.service import get_structured_data, send_mail


router = Router()


# Этот хэндлер будет срабатывать, при переводе на оператора
@router.message(StateFilter(FeedbackDialog.support))
async def process_support_sent(message: Message, state: FSMContext):
    # Тут прописать логику, пока тут ничего не происходит, при вводе чего либо будет ответ и сброс состояния.
    await message.answer(text="Очень важное сообщение, спасибо, досвидания.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода email'а
@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    keyboard = create_reply_kb("cancel_feedback")
    await message.answer(text="Спасибо!\n\nВведите адрес вашей электронной почты.", reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_email)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    keyboard = create_reply_kb("cancel_feedback")
    await message.answer(
        text="То, что вы отправили не похоже на имя\n\nПожалуйста, введите ваше имя.", reply_markup=keyboard
    )


# Этот хэндлер будет срабатывать, если введен корректный email
# и переводить в состояние ввода нномера телефона
@router.message(StateFilter(FSMFillForm.fill_email), IsCorrectEmail())
async def process_email_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "email"
    await state.update_data(email=message.text)
    keyboard = create_reply_kb("cancel_feedback")
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text="Спасибо!\n\nВведите ваш номер телефона.", reply_markup=keyboard)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_phone)


# Этот хэндлер будет срабатывать, если во время ввода email'а
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_email))
async def warning_not_email(message: Message):
    keyboard = create_reply_kb("cancel_feedback")
    await message.answer(text="Некорректный адрес электронной почты, повторите попытку ввода.", reply_markup=keyboard)


# Этот хэндлер будет срабатывать, если введен корректный телефон
# и переводить в состояние ввода текста
@router.message(StateFilter(FSMFillForm.fill_phone), IsCorrectPhoneNumber())
async def process_phone_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "phone"
    await state.update_data(phone=message.text)
    keyboard = create_reply_kb("cancel_feedback")
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text="Спасибо!\n\nВведите текст вашего обращения.", reply_markup=keyboard)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_text)


# Этот хэндлер будет срабатывать, если во время ввода телефона
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_phone))
async def warning_not_phone(message: Message):
    keyboard = create_reply_kb("cancel_feedback")
    await message.answer(text="Некорректный номер телефона повторите попытку ввода.", reply_markup=keyboard)


# Этот хэндлер будет срабатывать, если введен корректный текст
# и очищать машину состояний
@router.message(StateFilter(FSMFillForm.fill_text), F.text)
async def process_text_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "phone"
    await state.update_data(text=message.text)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_text)
    user_data: dict[str:str] = await state.get_data()

    tg_data, answer_data = await get_structured_data(user_data, message)
    await send_mail(tg_data + "\n\n" + answer_data)

    await state.clear()
    # тут отправка данных
    await message.answer(text=answer_data)
    # Отправляем пользователю сообщение
    await message.answer(text="Спасибо за обращение!\nНаш менеджер свяжется с Вами\nДо свидания!",
                         reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать, если во время ввода текста
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_text))
async def process_not_text_sent(message: Message):
    keyboard = create_reply_kb("cancel_feedback")
    await message.answer(text="Введите текст вашего обращения.", reply_markup=keyboard)
