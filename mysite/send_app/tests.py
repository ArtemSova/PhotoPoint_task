from django.test import TestCase
from unittest.mock import patch
from send_app.services import EmailService, SMSService, TelegramService, NotificationService


class NotificationTests(TestCase):

    @patch('send_app.services.send_mail')
    def test_email_service_success(self, mock_send_mail):
        mock_send_mail.return_value = 1
        result = EmailService.send("Test", "Hello", "user@example.com")
        self.assertTrue(result)

    @patch('requests.post')
    def test_sms_service_success(self, mock_post):
        mock_post.return_value.json.return_value = {"status": "OK"}
        result = SMSService.send("Test SMS", "+79991234567")
        self.assertTrue(result)

    @patch('requests.post')
    def test_telegram_service_success(self, mock_post):
        mock_post.return_value.status_code = 200
        result = TelegramService.send("Test Telegram", "329725203")
        self.assertTrue(result)

    @patch('send_app.services.EmailService.send', return_value=False)
    @patch('send_app.services.SMSService.send', return_value=False)
    @patch('send_app.services.TelegramService.send', return_value=True)
    def test_notification_fallback(self, mock_tg, mock_sms, mock_email):
        result = NotificationService.send_notification("Hi", "Fallback", "user@example.com", "+79990001122")
        self.assertEqual(result, "Telegram")


