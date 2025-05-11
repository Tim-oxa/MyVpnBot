from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import *
from services.database import db
from utils.users import create_user, upgrade_user_subscription, downgrade_user_to_free, user_exists
from keyboards.reply import main_menu_kb
from keyboards.inline import start_message_kb, buy_sub_kb, buy_month_kb, buy_year_kb, revoke_kb, support_kb
import config


router = Router()


@router.message(Command("start"))
async def start(message: Message, bot: Bot):
    if not await user_exists(message.from_user.id):
        await create_user(
            user_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )

    await message.answer_sticker(config.STICKER_ID, reply_markup=await main_menu_kb())
    await bot.copy_message(
        message.from_user.id,
        config.MESSAGES_CHANNEL,
        config.START_MESSAGE_ID,
        reply_markup=await start_message_kb()
    )


@router.message(F.text == "Моя подписка 👤")
async def my_sub(message: Message, bot: Bot):
    await bot.copy_message(
        message.from_user.id,
        config.MESSAGES_CHANNEL,
        config.MY_SUB_MESSAGE_ID,
        reply_markup=await start_message_kb()
    )


@router.message(F.text == "Купить безлимит 🔥")
@router.message(Command("pay"))
async def buy_sub(message: Message, bot: Bot):
    await bot.copy_message(
        message.from_user.id,
        config.MESSAGES_CHANNEL,
        config.BUY_SUB_MESSAGE_ID,
        reply_markup=await buy_sub_kb()
    )


@router.callback_query(F.data.in_(["buy_month", "buy_year"]))
async def buy_month_or_year(call: CallbackQuery, bot: Bot):
    if call.data == "buy_month":
        await bot.copy_message(
            call.from_user.id,
            config.MESSAGES_CHANNEL,
            config.BUY_MONTH_MESSAGE_ID,
            reply_markup=await buy_month_kb()
        )
    elif call.data == "buy_year":
        await bot.copy_message(
            call.from_user.id,
            config.MESSAGES_CHANNEL,
            config.BUY_YEAR_MESSAGE_ID,
            reply_markup=await buy_year_kb()
        )


@router.callback_query(F.data.in_(["confirm_month", "confirm_year"]))
async def confirm_payment(call: CallbackQuery, bot: Bot):
    await call.message.delete()
    if call.data == "confirm_month":
        text = "Месяц"
        await upgrade_user_subscription(call.from_user.id, "month")
        await bot.copy_message(
            call.from_user.id,
            config.MESSAGES_CHANNEL,
            config.CONFIRM_PAYMENT_MONTH_MESSAGE_ID
        )
    else:
        text = "Год"
        await upgrade_user_subscription(call.from_user.id, "year")
        await bot.copy_message(
            call.from_user.id,
            config.MESSAGES_CHANNEL,
            config.CONFIRM_PAYMENT_YEAR_MESSAGE_ID
        )
    await bot.send_message(
        config.ADMIN_ID,
        f"{call.from_user.id} @{call.from_user.username} {text}",
        reply_markup=await revoke_kb(call.from_user.id)
    )


@router.callback_query(F.data.startswith("revoke_"))
async def revoke_payment(call: CallbackQuery, bot: Bot):
    user_id = int(call.data.split("_")[1])
    await downgrade_user_to_free(user_id)
    await bot.copy_message(
        user_id,
        config.MESSAGES_CHANNEL,
        config.REVOKE_PAYMENT_MESSAGE_ID,
        reply_markup=await support_kb()
    )
    await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[[]]))


@router.message(F.text == "👨‍💻 Поддержка")
async def support(message: Message):
    await message.answer(f"Поддержка: @{config.SUPPORT_USERNAME}", reply_markup=await support_kb())
