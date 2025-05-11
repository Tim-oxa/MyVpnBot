from quart import Blueprint, redirect, request
from utils.users import get_user, user_exists
from services.database import db
import config


subscriptions = Blueprint(
    "Subscriptions",
    __name__,
    template_folder="subscriptions/templates",
    static_folder="subscriptions/static"
)


@subscriptions.get("/app")
async def get_app():
    user_agent = request.headers.get("User-Agent", "")
    if "Windows" in user_agent:
        link = "https://github.com/Happ-proxy/happ-desktop/releases/latest/download/setup-Happ.x86.exe"
    elif "iPhone" in user_agent:
        link = "https://apps.apple.com/us/app/happ-proxy-utility/id6504287215"
    elif "Mac OS" in user_agent:
        link = "https://apps.apple.com/us/app/happ-proxy-utility/id6504287215"
    elif "Android" in user_agent:
        link = "https://play.google.com/store/apps/details?id=com.happproxy"
    else:
        link = "https://happ.su"
    return redirect(link)


@subscriptions.get("/<sub>")
async def sub_redirect(sub: str):
    if await user_exists(sub=sub):
        remna_user = await get_user(sub=sub)
        return redirect(remna_user["happ"]["cryptoLink"])
    else:
        return "", 404


@subscriptions.get("/get/<uid>")
async def get_sub(uid: str):
    if await user_exists(uid=uid):
        user = await db.get_user(uid=uid)
        remna_user = await get_user(user["id"])
        return redirect(remna_user["subscriptionUrl"])
    return "", 404
