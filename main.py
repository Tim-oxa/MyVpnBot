from aiogram.client.default import DefaultBotProperties
from subscriptions import subscriptions
from aiogram import Bot, Dispatcher
from handlers import commands
from webhook import webhook
from webapp import webapp
from quart import Quart
import asyncio
import config


bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

dp.include_router(commands.router)

app = Quart(__name__)
app.register_blueprint(webapp, url_prefix=f"/{config.WEBAPP_PATH}")
app.register_blueprint(subscriptions)
app.register_blueprint(webhook)

@app.after_serving
async def stop():
    await dp.stop_polling()

async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        app.run_task("127.0.0.1", config.LOCAL_PORT)
    )

asyncio.run(main())
