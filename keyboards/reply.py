from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import config

async def main_menu_kb():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Моя подписка 👤")],
        [KeyboardButton(text="Купить безлимит 🔥")],
        [KeyboardButton(text="👨‍💻 Поддержка")]
    ], resize_keyboard=True)
    return kb
