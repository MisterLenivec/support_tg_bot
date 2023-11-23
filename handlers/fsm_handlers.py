from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import CallbackQuery, Message

from keyboards.inline_keyboards import create_inline_kb
from filters.filters import IsCorrectEmail, IsCorrectPhoneNumber


router = Router()

class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_email = State()
    fill_phone = State()
    fill_text = State()


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.callback_query(F.data =='cancel', ~StateFilter(default_state))
async def process_cancel_command_state(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Вы вышли из заполнения обращения.')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()
    await callback.answer()


# Этот хэндлер будет срабатывать на команду /send_feedback
# и переводить бота в состояние ожидания ввода имени
@router.message(Command(commands='send_feedback'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    keyboard = create_inline_kb('cancel')
    await message.answer(text='Пожалуйста, введите ваше имя.', reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода email'а
@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    keyboard = create_inline_kb('cancel')
    await message.answer(text='Спасибо!\n\nВведите адрес вашей электронной почты.', reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_email)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    keyboard = create_inline_kb('cancel')
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\nПожалуйста, введите ваше имя.',
        reply_markup=keyboard
        )


# Этот хэндлер будет срабатывать, если введен корректный email
# и переводить в состояние ввода нномера телефона
@router.message(StateFilter(FSMFillForm.fill_email), IsCorrectEmail())
async def process_email_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "email"
    await state.update_data(email=message.text)
    keyboard = create_inline_kb('cancel')
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text='Спасибо!\n\nВведите ваш номер телефона.', reply_markup=keyboard)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_phone)


# Этот хэндлер будет срабатывать, если во время ввода email'а
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_email))
async def warning_not_email(message: Message):
    keyboard = create_inline_kb('cancel')
    await message.answer(text='Некорректный адрес электронной почты, повторите попытку ввода.', reply_markup=keyboard)


# Этот хэндлер будет срабатывать, если введен корректный телефон
# и переводить в состояние ввода текста
@router.message(StateFilter(FSMFillForm.fill_phone), IsCorrectPhoneNumber())
async def process_phone_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "phone"
    await state.update_data(phone=message.text)
    keyboard = create_inline_kb('cancel')
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text='Спасибо!\n\nВведите текст вашего обращения.', reply_markup=keyboard)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_text)


# Этот хэндлер будет срабатывать, если во время ввода телефона
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_phone))
async def warning_not_phone(message: Message):
    keyboard = create_inline_kb('cancel')
    await message.answer(text='Некорректный номер телефона повторите попытку ввода.', reply_markup=keyboard)


# Этот хэндлер будет срабатывать, если введен корректный текст
# и очищать машину состояний
@router.message(StateFilter(FSMFillForm.fill_text), F.text)
async def process_text_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "phone"
    await state.update_data(text=message.text)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_text)
    data = await state.get_data()
    user_data = f"Имя: {data['name']}\n" \
               f"Почта: {data['email']}\n" \
               f"Телефон: {data['phone']}\n" \
               f"Текст: {data['text']}"

    await state.clear()
    # тут отправка данных
    await message.answer(text=user_data)
    # Отправляем пользователю сообщение
    await message.answer(text="Спасибо за обращение!\nНаш менеджер свяжется с Вами\nДо свидания!")


# Этот хэндлер будет срабатывать, если во время ввода текста
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_text))
async def process_not_text_sent(message: Message):
    keyboard = create_inline_kb('cancel')
    await message.answer(text='Введите текст вашего обращения.', reply_markup=keyboard)
