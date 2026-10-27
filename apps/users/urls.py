from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.telegram_webhook import telegram_webhook
from apps.users.views import SendOTPView, VerifyOTPView, RegisterView, MeView


urlpatterns = [
    path('send-otp/',SendOTPView.as_view()),
    path('verify-otp/',VerifyOTPView.as_view()),
    path('register/',RegisterView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    path('me/',MeView.as_view()),
    path('api/telegram/webhook/', telegram_webhook),
]