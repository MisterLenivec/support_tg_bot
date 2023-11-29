from dataclasses import dataclass

from aiogram.fsm.state import State, StatesGroup
from environs import Env


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_email = State()
    fill_phone = State()
    fill_text = State()


class FeedbackDialog(StatesGroup):
    support = State()


@dataclass
class TgBot:
    token: str

@dataclass
class Omnidesk:
    token: str


@dataclass
class MailSettings:
    mail_login: str
    email_recipients: str
    protocol: str
    app_pass: str


@dataclass
class Config:
    tg_bot: TgBot
    mail: MailSettings
    omnidesk: Omnidesk


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненным полем token
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        mail=MailSettings(
            mail_login=env('MAIL_LOGIN'),
            email_recipients=[env('EMAIL_RECIPIENT')],
            protocol=env('PROTOCOL'),
            app_pass=env('APP_PASS')
        ),
        omnidesk=Omnidesk(
            token=env('OMNIDESK_TOKEN')
        )
    )
