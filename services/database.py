from services.remna import remna
import motor.motor_asyncio
import datetime as dt
import random
import string
import config

class MDB:
    def __init__(self):
        self.db = motor.motor_asyncio.AsyncIOMotorClient(config.DB_URL).get_database(config.DB_NAME)

    async def get_user(self, user_id: int = None, sub: str = None, uid: str = None):
        if user_id:
            user = await self.db["users"].find_one({"id": user_id})
        elif sub:
            user = await self.db["users"].find_one({"sub": sub})
        else:
            user = await self.db["users"].find_one({"uid": uid})
        return user

    async def create_user(self,
                          user_id: int,
                          full_name: str,
                          sub: str,
                          uid: str,
                          username: str = None):
        user = await self.db["users"].insert_one({
            "id": user_id,
            "username": username,
            "full_name": full_name,
            "sub": sub,
            "uid": uid
        })
        return user

db = MDB()
