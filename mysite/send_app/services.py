import logging
import smtplib
import requests

from django.core.mail import send_mail
from django.conf import settings
from mysite.settings import env


logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send(subject: str, message: str, to_email: str) -> bool:
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email],
                fail_silently=False,
            )
            logger.info(f"Email sent to {to_email}")
            return True
        except smtplib.SMTPException as e:
            logger.error(f"Email send failed: {e}")
            return False


class SMSService:
    @staticmethod
    def send(message: str, to_phone: str) -> bool:
        try:
            api_id = env('SMS_RU_API_ID')
            url = "https://sms.ru/sms/send"
            payload = {
                "api_id": api_id,
                "to": to_phone,
                "msg": message,
                "json": 1
            }
            response = requests.post(url, data=payload, timeout=10)
            data = response.json()

            if data.get("status") == "OK":
                logger.info(f"SMS sent to {to_phone}")
                return True
            else:
                logger.error(f"SMS.ru error: {data}")
                return False

        except Exception as e:
            logger.error(f"SMS send failed: {e}")
            return False


class TelegramService:
    @staticmethod
    def send(message, chat_id):
        bot_token = env("TELEGRAM_BOT_TOKEN", default=None)
        if not bot_token:
            print("Telegram send failed: TELEGRAM_BOT_TOKEN not set")
            return False

        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            response = requests.post(url, data={"chat_id": chat_id, "text": message})
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram send failed: {e}")
            return False


class NotificationService:
    """Основной сервис: пробует поочередно Email → SMS → Telegram"""
    @staticmethod
    def send_notification(subject, message, email=None, phone=None, chat_id=None):
        if EmailService.send(subject, message, email):
            return "Email"
        if SMSService.send(message, phone):
            return "SMS"
        if TelegramService.send(message, chat_id):
            return "Telegram"
        return "Failed"
