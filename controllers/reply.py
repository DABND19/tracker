from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, func
from aiogram import types
from models import Reply


class ReplyController:
    def __init__(self, session: AsyncSession):
        self.__session = session

    def create(self, question: types.Message, reply: types.Message):
        self.__session.add(
            Reply(time=reply.date,
                  delta=(reply.date - question.date).total_seconds(),
                  employee=reply.from_user.id,
                  chat=reply.chat.id)
        )

    async def avg_for(self, begin: datetime, end: datetime, chat: types.Chat) -> float:
        query = select(func.avg(Reply.delta).label("avg_delta"))\
            .where(Reply.time >= begin, Reply.time <= end, Reply.chat == chat.id)
        result = await self.__session.execute(query)
        return result.first().avg_delta
