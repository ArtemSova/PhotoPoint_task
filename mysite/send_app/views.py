from django.shortcuts import render, redirect
from django.http import HttpResponse
from .services import EmailService, SMSService, TelegramService, NotificationService


def send_test_view(request):
    """Главная страница с кнопками"""
    return render(request, 'send_app/send_test.html')


def send_email_view(request):
    EmailService.send("Тестовое сообщение", "Тестовое сообщение", "artem@nightsova.ru")
    return HttpResponse("✅ Email отправлен!")


def send_sms_view(request):
    SMSService.send("Тестовое сообщение", "+79129202644")
    return HttpResponse("✅ SMS отправлено!")


def send_telegram_view(request):
    TelegramService.send("Тестовое сообщение", "329725203")  # нужный ID
    return HttpResponse("✅ Сообщение в Telegram отправлено!")

def send_notification_view(request):
    """Надежная доставка через NotificationService"""
    result = NotificationService.send_notification(
        subject="Тестовое сообщение",
        message="Тестовое сообщение",
        email="artem@nightsova.ru",
        phone="+79129202644",
        chat_id="329725203",
    )

    if result == "Failed":
        return HttpResponse("❌ Не удалось доставить сообщение ни одним способом")
    return HttpResponse(f"✅ Сообщение отправлено через: {result}")
