from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import config

async def start_message_kb():
    web_app = WebAppInfo(url=f"https://{config.WEBAPP_DOMAIN}/{config.WEBAPP_PATH}")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мой VPN 🔥", web_app=web_app)]
    ])
    return kb

async def buy_sub_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Месяц - 100₽", callback_data="buy_month")],
        [InlineKeyboardButton(text="Год - 999₽ 🔥", callback_data="buy_year")]
    ])
    return kb

async def buy_month_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я оплатил ✅", callback_data="confirm_month")]
    ])
    return kb

async def buy_year_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я оплатил ✅", callback_data="confirm_year")]
    ])
    return kb

async def revoke_kb(user_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отменить ❌", callback_data=f"revoke_{user_id}")]
    ])
    return kb

async def support_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍💻 Поддержка", url=f"https://t.me/{config.SUPPORT_USERNAME}")]
    ])
    return kb
