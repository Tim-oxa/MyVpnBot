from quart import Blueprint, render_template, request, jsonify
from utils.users import create_user, user_exists, get_user
from services.database import db
from operator import itemgetter
import datetime as dt
import urllib.parse
import hashlib
import config
import json
import hmac


webapp = Blueprint(
    "Web App",
    __name__,
    template_folder="templates",
    static_folder="static"
)


months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря"
]


@webapp.get("/")
async def webapp_index():
    return await render_template(
        "index.html",
        webapp_domain=config.WEBAPP_DOMAIN,
        webapp_path=config.WEBAPP_PATH
    )


@webapp.post("/verify")
async def verify():
    data = await request.get_json()
    init_data = data.get("init_data")

    if not init_data:
        return jsonify({"ok": False, "error": "Missing init_data"}), 400

    try:
        parsed_data = dict(urllib.parse.parse_qsl(init_data))
    except ValueError:
        return "", 404
    if "hash" not in parsed_data:
        return "", 404

    hash_ = parsed_data.pop('hash')
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=config.BOT_TOKEN.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    if calculated_hash == hash_:
        user = json.loads(parsed_data["user"])
        if not await user_exists(user["id"]):
            await create_user(
                user_id=user["id"],
                full_name=f"{user['first_name']} {user['last_name']}",
                username=user.get("username")
            )
        user = await db.get_user(user["id"])
        return jsonify({"ok": True, "sub": user["sub"]})
    else:
        return jsonify({"ok": False, "error": "Invalid signature"}), 403


@webapp.get("/page/<sub>")
async def sub_page(sub: str):
    if await user_exists(sub=sub):
        remna_user = await get_user(sub=sub)
        if remna_user["status"] == "LIMITED":
            return await render_template(
                "limited.html",
                webapp_path=config.WEBAPP_PATH,
                bot_username=config.BOT_USERNAME
            )
        status = "Активна ✅" if remna_user["status"] == "ACTIVE" else "Неактивна ❌"
        traffic_used = round(remna_user["usedTrafficBytes"] / 1024 / 1024 / 1024, 2)
        traffic_limit = round(remna_user["trafficLimitBytes"] / 1024 / 1024 / 1024)
        date = dt.datetime.fromisoformat(remna_user["expireAt"])
        expire = "Никогда" if date.year == 2099 else f"{date.day} {months[date.month-1]} {date.year} года"
        sub_url = f"https://{config.SUBS_DOMAIN}/{sub}"
        return await render_template(
            "sub.html",
            status=status,
            traffic_used=traffic_used,
            traffic_limit=traffic_limit,
            expire=expire,
            sub_url=sub_url,
            webapp_path=config.WEBAPP_PATH,
            app_url=config.APP_URL
        )
    else:
        return "", 404
