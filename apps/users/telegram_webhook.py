# apps/common/telegram_webhook.py  yoki apps/users/telegram_webhook.py
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.users.models import TelegramLink, User
from apps.common.telegram import send_otp_message
from config import settings


def normalize_phone(raw: str) -> str:
    digits = re.sub(r'\D', '', raw or '')
    if digits.startswith('998') and len(digits) == 12:
        return f'+{digits}'
    if len(digits) == 9:
        return f'+998{digits}'
    if raw.startswith('+'):
        return raw
    return f'+{digits}' if digits else raw


@csrf_exempt
@require_POST
def telegram_webhook(request):
    """
    Telegram: POST https://api.telegram.org/bot<TOKEN>/setWebhook
      ?url=https://yourdomain.com/api/telegram/webhook/
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'ok': True})

    message = data.get('message') or {}
    chat = message.get('chat') or {}
    chat_id = str(chat.get('id', ''))
    text = (message.get('text') or '').strip()
    contact = message.get('contact')  # Contact tugmasi orqali

    if not chat_id:
        return JsonResponse({'ok': True})

    # /start
    # if text.startswith('/start'):
    #     send_otp_message(
    #         chat_id,
    #         "Assalomu alaykum! Mebel House botiga xush kelibsiz.\n\n"
    #         "OTP olish uchun telefon raqamingizni yuboring.\n"
    #         "Masalan: +998901234567\n\n"
    #         "Yoki pastdagi tugma orqali kontaktni ulashing."
    #     )
    #     # Ixtiyoriy: ReplyKeyboardMarkup bilan "Kontaktni ulash" tugmasi
    #     return JsonResponse({'ok': True})
    if text.startswith('/start'):
        import requests
        token = settings.TELEGRAM_OTP_BOT_TOKEN
        requests.post(
            f'https://api.telegram.org/bot{token}/sendMessage',
            json={
                'chat_id': chat_id,
                'text': (
                    "Assalomu alaykum!\n\n"
                    "Telefon yuboring: +998901234567\n"
                    "yoki tugma orqali kontaktni ulashing."
                ),
                'reply_markup': {
                    'keyboard': [[{
                        'text': '📱 Kontaktni ulash',
                        'request_contact': True,
                    }]],
                    'resize_keyboard': True,
                    'one_time_keyboard': True,
                },
            },
            timeout=10,
        )
        return JsonResponse({'ok': True})

    # Kontakt ulashilgan bo‘lsa
    phone = None
    if contact and contact.get('phone_number'):
        phone = normalize_phone(contact['phone_number'])
    elif text and (text.startswith('+') or text.replace(' ', '').isdigit()):
        phone = normalize_phone(text)

    if phone:
        TelegramLink.objects.update_or_create(
            phone=phone,
            defaults={'chat_id': chat_id},
        )
        # Agar User allaqachon bor bo‘lsa — yangilash
        User.objects.filter(phone=phone).update(telegram_chat_id=chat_id)

        send_otp_message(
            chat_id,
            f"✅ Telefon bog‘landi: {phone}\n\n"
            "Endi saytda login/register qilganingizda kod shu yerga keladi."
        )
        return JsonResponse({'ok': True})

    if text and not text.startswith('/'):
        send_otp_message(
            chat_id,
            "Iltimos, telefon raqamni yuboring: +998901234567"
        )

    return JsonResponse({'ok': True})