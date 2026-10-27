import random
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from apps.users.models import OTPCode, User, TelegramLink
from apps.common.telegram import send_otp_message


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def get_chat_id_for_phone(phone: str) -> str | None:
    user = (
        User.objects.filter(phone=phone)
        .exclude(telegram_chat_id__isnull=True)
        .exclude(telegram_chat_id='')
        .first()
    )
    if user:
        return user.telegram_chat_id

    link = TelegramLink.objects.filter(phone=phone).first()
    if link:
        return link.chat_id
    return None


def send_otp(phone: str) -> dict:
    chat_id = get_chat_id_for_phone(phone)

    if not chat_id:
        return {
            'ok': False,
            'code': 'TELEGRAM_NOT_LINKED',
            'detail': (
                'Avval Telegram botga /start bosing va telefon raqamingizni yuboring.'
            ),
        }

    code = generate_otp()
    OTPCode.objects.create(phone=phone, code=code)

    text = (
        f"🔐 Sahovat Mebel — tasdiqlash kodi\n\n"
        f"<b>{code}</b>\n\n"
        f"Telefon: {phone}\n"
        f"Amal qilish muddati: {settings.OTP_TTL_SECONDS // 60} daqiqa.\n"
        f"Kodni hech kimga bermang."
    )
    sent = send_otp_message(str(chat_id), text)

    if not sent:
        return {
            'ok': False,
            'code': 'SEND_FAILED',
            'detail': 'Telegramga yuborib bo‘lmadi. Keyinroq urinib ko‘ring.',
        }

    return {'ok': True, 'detail': 'OTP Telegram botga yuborildi'}


def verify_otp(phone: str, code: str) -> bool:
    ttl = timezone.now() - timedelta(seconds=settings.OTP_TTL_SECONDS)
    otp = (
        OTPCode.objects.filter(
            phone=phone, code=code, is_used=False, created_at__gte=ttl
        )
        .order_by('-created_at')
        .first()
    )
    if not otp:
        return False
    otp.is_used = True
    otp.save(update_fields=['is_used'])
    return True


