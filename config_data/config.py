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
class WebhookSettings:
    web_server_host: str
    web_server_port: str
    webhook_path: str
    webhook_secret: str


@dataclass
class DBSettings:
    name: str
    user: str
    password: str
    host: str
    port: str


@dataclass
class RedisSettings:
    host: str


@dataclass
class DebugSettings:
    debug_value: bool

@dataclass
class Config:
    tg_bot: TgBot
    mail: MailSettings
    omnidesk: Omnidesk
    webhook: WebhookSettings
    database: DBSettings
    redis: RedisSettings
    debug: DebugSettings


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями
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
        ),
        webhook=WebhookSettings(
            web_server_host=env('WEB_SERVER_HOST'),
            web_server_port=env('WEB_SERVER_PORT'),
            webhook_path=env('WEBHOOK_PATH'),
            webhook_secret=env('WEBHOOK_SECRET'),
        ),
        database=DBSettings(
            name=env('POSTGRES_DB'),
            user=env('POSTGRES_USER'),
            password=env('POSTGRES_PASSWORD'),
            host=env('POSTGRES_HOST', '127.0.0.1'),
            port=env('POSTGRES_PORT'),
        ),
        redis=RedisSettings(
            host=env('REDIS_HOST', '127.0.0.1'),
        ),
        debug=DebugSettings(
            debug_value=env('DEBUG', '') == 'True'
        )
    )
