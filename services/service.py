import pytz

from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from environs import Env

async def get_structured_data(user_data, message) -> tuple[str, str]:
    tz_moscow = pytz.timezone("Europe/Moscow")
    localized_time: str = message.date.astimezone(tz_moscow).strftime("%d-%m-%Y %H:%M:%S")

    tg_data = f"Время обращения: {localized_time}\n" \
        f"ID пользователя в ТГ: {message.from_user.id}\n" \
        f"Обращение от бота: {message.from_user.is_bot}\n" \
        f"Имя пользователя в ТГ: {message.from_user.first_name}"

    answer_data = f"Имя: {user_data['name']}\n" \
        f"Почта: {user_data['email']}\n" \
        f"Телефон: {user_data['phone']}\n" \
        f"Текст: {user_data['text']}"

    return tg_data, answer_data


async def send_mail(mail_message) -> None:
    env = Env()
    env.read_env()

    from_email = env('MAIL_LOGIN')
    to_emails = [env('EMAIL_RECIPIENT')]
    print(from_email, to_emails)

    msg = MIMEMultipart()

    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = 'Обращение из ТГ обратной связи Емеля'

    msg.attach(MIMEText(mail_message, "plain"))

    smtp_server = SMTP_SSL(env('PROTOCOL'))
    smtp_server.command_encoding = 'utf-8'
    smtp_server.set_debuglevel(1)
    smtp_server.login(from_email, env('APP_PASS'))
    smtp_server.sendmail(from_email, to_emails, msg.as_string())

    smtp_server.quit()
