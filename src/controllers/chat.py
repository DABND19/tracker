from typing import List
from sqlalchemy.sql.expression import delete
from models import Chat
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete


class ChatController:
    def __init__(self, session: AsyncSession):
        self._session = session

    def create(self, chat: types.Chat):
        self._session.add(Chat(id=chat.id, title=chat.title))

    async def delete(self, chat: types.Chat):
        await self._session.execute(delete(Chat).where(Chat.id == chat.id))

    async def get_all_ids(self) -> List[int]:
        result = await self._session.execute(select(Chat.id))
        return list(map(lambda record: record[0], result.all()))

    async def get_list(self) -> List[Chat]:
        result = await self._session.execute(select(Chat))
        return result.scalars().all()
