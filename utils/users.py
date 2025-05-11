from services.database import db
from services.remna import remna
import datetime as dt
import random
import string
import config

async def get_user(user_id: int = None, sub: str = None, uid: str = None):
    if user_id:
        remna_user = await remna.get(f"{config.USERNAME_PREFIX}{user_id}")
    elif sub:
        user = await db.get_user(sub=sub)
        remna_user = await remna.get(f"{config.USERNAME_PREFIX}{user['id']}")
    else:
        user = await db.get_user(uid=uid)
        remna_user = await remna.get(f"{config.USERNAME_PREFIX}{user['id']}")
    return remna_user

async def user_exists(user_id: int = None, sub: str = None, uid: str = None):
    if user_id:
        user = await db.get_user(user_id)
    elif sub:
        user = await db.get_user(sub=sub)
    else:
        user = await db.get_user(uid=uid)
    if user:
        return True
    else:
        return False

async def create_user(user_id: int,
                      full_name: str,
                      username: str = None):
    remna_user = await remna.create(
        username=f"{config.USERNAME_PREFIX}{user_id}",
        traffic_limit=1024 * 1024 * 1024 * config.DEFAULT_TRAFFIC_LIMIT,
        traffic_strategy=config.DEFAULT_TRAFFIC_STRATEGY,
        inbounds=config.DEFAULT_INBOUNDS,
        expire=dt.datetime.today().replace(year=2099).isoformat(),
        description=username
    )
    sub = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    await db.create_user(
        user_id=user_id,
        full_name=full_name,
        sub=sub,
        uid=remna_user["uuid"],
        username=username
    )
    return remna_user

async def upgrade_user_subscription(user_id: int,
                                    duration: str):
    date = dt.datetime.today()
    if duration == "month":
        date += dt.timedelta(days=31)
    elif duration == "year":
        date += dt.timedelta(days=365)
    remna_user = await remna.edit(
        username=f"{config.USERNAME_PREFIX}{user_id}",
        traffic_limit=1024 * 1024 * 1024 * config.SUBSCRIPTION_TRAFFIC_LIMIT,
        expire=date.isoformat()
    )
    return remna_user

async def downgrade_user_to_free(user_id: int):
    remna_user = await remna.edit(
        username=f"{config.USERNAME_PREFIX}{user_id}",
        traffic_limit=1024 * 1024 * 1024 * config.DEFAULT_TRAFFIC_LIMIT,
        expire=dt.datetime.today().replace(year=2099).isoformat()
    )
    return remna_user
