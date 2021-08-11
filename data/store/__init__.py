from asyncio.locks import Lock
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession
from loader import Session
import redis
from data.config import REDIS_HOST
from datetime import timedelta


engine = redis.Redis(host=REDIS_HOST)


class BaseStore:
    LOADING_LOCK = Lock()
    KEY = None
    EXPIRES = timedelta(minutes=15)

    @staticmethod
    async def _load_from_db(session: AsyncSession) -> List:
        return []

    @classmethod
    async def contains(cls, item):
        await cls._load_if_expired()
        return engine.sismember(cls.KEY, item)

    @classmethod
    async def load(cls) -> None:
        with engine.pipeline() as pipe:
            async with Session() as session:
                items = await cls._load_from_db(session)
            pipe.sadd(cls.KEY, *items)
            pipe.expire(cls.KEY, int(cls.EXPIRES.total_seconds()))
            pipe.execute()

    @classmethod
    async def _load_if_expired(cls) -> None:
        async with cls.LOADING_LOCK:
            if engine.ttl(cls.KEY) == -2:
                await cls.load()
