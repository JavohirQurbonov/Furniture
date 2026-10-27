# import requests
# from django.conf import settings
#
#
# def send_telegram_message(chat_id: str, text: str) -> bool:
#     token = settings.TELEGRAM_BOT_TOKEN
#     if not token or not chat_id:
#         print('[Telegram] Token yoki chat_id yo\'q:', text[:100])
#         return False
#     url = f'https://api.telegram.org/bot{token}/sendMessage'
#     try:
#         r = requests.post(url, json={
#             'chat_id': chat_id,
#             'text': text,
#             'parse_mode': 'HTML',
#         }, timeout=10)
#         return r.ok
#     except Exception as e:
#         print('[Telegram] xato:', e)
#         return False
#
#
# def notify_new_order(order) -> None:
#     """Yangi buyurtma haqida admin ga xabar."""
#     lines = [
#         f'🛒 <b>Yangi buyurtma #{order.id}</b>',
#         f'Mijoz: {order.user.first_name} ({order.user.phone})',
#         f'Telefon: {order.phone}',
#         f'Manzil: {order.address}',
#     ]
#     if order.note:
#         lines.append(f'Izoh: {order.note}')
#     lines.append('— Mahsulotlar —')
#     for item in order.items.select_related('product'):
#         lines.append(
#             f'• {item.product.name_uz} × {item.quantity} = '
#             f'{item.price * item.quantity:,.0f} so\'m'
#         )
#     lines.append(f'<b>Jami: {order.total:,.0f} so\'m</b>')
#
#     send_telegram_message(
#         settings.TELEGRAM_ADMIN_CHAT_ID,
#         '\n'.join(lines),
#     )
#
# def notify_order_cancelled(order) -> None:
#     lines = [
#         f'❌ <b>Buyurtma bekor qilindi #{order.id}</b>',
#         f'Mijoz: {order.user.first_name} ({order.user.phone})',
#         f'Telefon: {order.phone}',
#         f'Manzil: {order.address}',
#         f'Status: cancelled',
#     ]
#     lines.append('— Mahsulotlar —')
#     for item in order.items.select_related('product'):
#         lines.append(
#             f'• {item.product.name_uz} × {item.quantity} = '
#             f'{item.price * item.quantity:,.0f} so\'m'
#         )
#     lines.append(f'<b>Jami: {order.total:,.0f} so\'m</b>')
#
#     send_telegram_message(
#         settings.TELEGRAM_ADMIN_CHAT_ID,
#         '\n'.join(lines),
#     )

import requests
from django.conf import settings


def _send(token: str, chat_id: str, text: str) -> bool:
    if not token or not chat_id:
        print('[Telegram] token yoki chat_id yo\'q')
        return False
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        r = requests.post(
            url,
            json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'},
            timeout=10,
        )
        if not r.ok:
            print('[Telegram] javob:', r.status_code, r.text)
        return r.ok
    except Exception as e:
        print('[Telegram] xato:', e)
        return False


# ---------- OTP bot (user ga) ----------
def send_otp_message(chat_id: str, text: str) -> bool:
    return _send(settings.TELEGRAM_OTP_BOT_TOKEN, chat_id, text)


# ---------- Admin bot (admin ga) ----------
def send_admin_message(text: str) -> bool:
    return _send(
        settings.TELEGRAM_ADMIN_BOT_TOKEN,
        settings.TELEGRAM_ADMIN_CHAT_ID,
        text,
    )


def notify_new_order(order) -> None:
    lines = [
        f'🛒 <b>Yangi buyurtma #{order.id}</b>',
        f'Mijoz: {order.user.first_name} ({order.user.phone})',
        f'Telefon: {order.phone}',
        f'Manzil: {order.address}',
    ]
    if order.note:
        lines.append(f'Izoh: {order.note}')
    lines.append('— Mahsulotlar —')
    for item in order.items.select_related('product'):
        lines.append(
            f'• {item.product.name_uz} × {item.quantity} = '
            f'{item.price * item.quantity:,.0f} so\'m'
        )
    lines.append(f'<b>Jami: {order.total:,.0f} so\'m</b>')
    send_admin_message('\n'.join(lines))


def notify_order_cancelled(order) -> None:
    lines = [
        f'❌ <b>Buyurtma bekor qilindi #{order.id}</b>',
        f'Mijoz: {order.user.first_name} ({order.user.phone})',
        f'Telefon: {order.phone}',
        f'Manzil: {order.address}',
    ]
    for item in order.items.select_related('product'):
        lines.append(
            f'• {item.product.name_uz} × {item.quantity}'
        )
    lines.append(f'<b>Jami: {order.total:,.0f} so\'m</b>')
    send_admin_message('\n'.join(lines))