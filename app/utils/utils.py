from email.message import EmailMessage
from aiohttp import ClientSession
import aiosmtplib

from app.config import settings
from app.exceptions import EmailException, EmailSenderException


async def email_verify(email: str):
    async with ClientSession() as session:
        async with session.get(
            f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.EMAIL_API_KEY}"
        ) as response:
            if response.status == 200:
                data = await response.json()
                is_valid = data["data"]["gibberish"]
                if is_valid == "false":
                    raise EmailException


async def send_referral_email(email_to: str, referral_code: str):
    try:
        email = EmailMessage()
        email["From"] = settings.SMTP_USER
        email["To"] = email_to
        email["Subject"] = "Ваш реферальный код"

        message_body = (
            f"Ваш реферальный код: {referral_code}\n\nС уважением,\nЧилловый парень"
        )
        email.set_content(message_body)

        # Настройки SMTP-сервера
        smtp_config = {
            "hostname": settings.SMTP_SERVER,
            "port": settings.SMTP_PORT,
            "start_tls": True,
            "username": settings.SMTP_USER,
            "password": settings.SMTP_PASS,
        }

        await aiosmtplib.send(email, **smtp_config)
    except Exception:
        raise EmailSenderException
