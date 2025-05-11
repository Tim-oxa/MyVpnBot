from quart import Blueprint, request
from aiogram import Bot
import config


webhook = Blueprint(
    "Webhook",
    __name__
)

bot = Bot(config.BOT_TOKEN)


@webhook.post(f"/{config.WEBHOOK_PATH}")
async def remna_webhook():
    data = await request.get_json()
    remna_user = data["data"]
    if data["event"] == "user.expired":
        try:
            await bot.forward_message(
                int(remna_user["username"][1:]),
                config.MESSAGES_CHANNEL,
                config.EXPIRE_MESSAGE_ID
            )
        except Exception as E:
            print(E)
    elif data["event"] == "user.limited":
        try:
            await bot.forward_message(
                int(remna_user["username"][1:]),
                config.MESSAGES_CHANNEL,
                config.LIMITED_MESSAGE_ID
            )
        except Exception as E:
            print(E)
    return "OK"
