import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from re import sub
from smtplib import SMTP_SSL

import pytz
from config_data.config import Config, load_config


async def get_validated_phone(phone) -> str:
    validated: str = sub(r'\D', '', phone)
    if len(validated) > 10:
        return '8' + validated[1:]
    return '8' + validated

async def get_structured_data(user_data, message) -> tuple[str, str, datetime, str]:
    tz_moscow = pytz.timezone("Europe/Moscow")
    localized_time: datetime = datetime.now().astimezone(tz_moscow).replace(microsecond=0)
    localized_time_str: str = localized_time.strftime("%d-%m-%Y %H:%M:%S")
    validated_phone: str = await get_validated_phone(user_data['phone'])

    tg_data = (
        f"Время обращения: {localized_time_str}\n"
        f"ID пользователя в ТГ: {message.from_user.id}\n"
        f"Обращение от бота: {message.from_user.is_bot}\n"
        f"Имя пользователя в ТГ: {message.from_user.first_name}"
    )

    answer_data = (
        f"Имя: {user_data['name']}\n"
        f"Почта: {user_data['email']}\n"
        f"Телефон: {validated_phone}\n"
        f"Текст: {user_data['text']}"
    )
    logging.info(f'Return structured feedback data from user with tg_id - {message.from_user.id}.')
    return tg_data, answer_data, localized_time, validated_phone


async def send_mail(mail_message, user_id) -> None:
    logging.info(f'Prepare send feedback to email from user with tg_id - {user_id}.')
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
    logging.info(f'Feedback to email from user with tg_id - {user_id} was sended.')
