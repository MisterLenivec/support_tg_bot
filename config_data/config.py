from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
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
        )
    )
