from django.urls import path
from . import views

urlpatterns = [
    path('', views.send_test_view, name='send_test'),
    path('send/email/', views.send_email_view, name='send_email'),
    path('send/sms/', views.send_sms_view, name='send_sms'),
    path('send/telegram/', views.send_telegram_view, name='send_telegram'),
    path('send/notification/', views.send_notification_view, name='send_notification'),
]

