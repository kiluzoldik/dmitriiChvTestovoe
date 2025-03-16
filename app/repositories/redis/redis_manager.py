import aioredis
from pydantic import BaseModel

from app.config import settings


class RedisManager:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(url=settings.REDIS_URL)

    async def disconnect(self):
        await self.redis.close()

    async def save_data(self, data: BaseModel):
        new_data = data.model_dump()
        await self.redis.set(
            new_data["code"], str(new_data["user_id"]), ex=new_data["expire"]
        )

    async def remove_code(self, ref_code: str):
        await self.redis.delete(ref_code)

    async def check_code(self, code: str):
        return await self.redis.get(code)


redis_manager = RedisManager()
