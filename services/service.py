from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

import pytz
from config_data.config import Config, load_config


async def get_structured_data(user_data, message) -> tuple[str, str]:
    tz_moscow = pytz.timezone("Europe/Moscow")
    localized_time: str = message.date.astimezone(tz_moscow).strftime("%d-%m-%Y %H:%M:%S")

    tg_data = (
        f"Время обращения: {localized_time}\n"
        f"ID пользователя в ТГ: {message.from_user.id}\n"
        f"Обращение от бота: {message.from_user.is_bot}\n"
        f"Имя пользователя в ТГ: {message.from_user.first_name}"
    )

    answer_data = (
        f"Имя: {user_data['name']}\n"
        f"Почта: {user_data['email']}\n"
        f"Телефон: {user_data['phone']}\n"
        f"Текст: {user_data['text']}"
    )

    return tg_data, answer_data


async def send_mail(mail_message) -> None:
    config: Config = load_config()

    from_email = config.mail.mail_login
    to_emails = config.mail.email_recipients

    msg = MIMEMultipart()

    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = "Обращение из ТГ обратной связи Емеля"

    msg.attach(MIMEText(mail_message, "plain"))

    smtp_server = SMTP_SSL(config.mail.protocol)
    smtp_server.command_encoding = "utf-8"
    smtp_server.set_debuglevel(1)
    smtp_server.login(from_email, config.mail.app_pass)
    smtp_server.sendmail(from_email, to_emails, msg.as_string())
    smtp_server.quit()
