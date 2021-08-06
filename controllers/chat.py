from sqlalchemy.sql.expression import delete
from models import Chat
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete


class ChatController:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create(self, chat: types.Chat):
        self.__session.add(Chat(id=chat.id, title=chat.title))

    async def delete(self, chat: types.Chat):
        await self.__session.execute(delete(Chat).where(Chat.id == chat.id))

    async def get_all_ids(self):
        result = await self.__session.execute(select(Chat.id))
        return result.all()
