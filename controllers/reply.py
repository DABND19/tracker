from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, func
from aiogram import types
from models import Reply, Employee, Chat
from typing import Optional, NamedTuple, List


class EmployeeStats(NamedTuple):
    full_name: str
    avg_delta: timedelta
    replies_count: int


class ChatReport(NamedTuple):
    title: str
    avg_delta: Optional[timedelta]
    replies_count: int


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

    async def chat_report(self, chat_id: int, begin: Optional[datetime] = None, end: datetime = None) -> ChatReport:
        query = select(Chat.title,
                       func.avg(Reply.delta),
                       func.count(Reply.id))\
            .where(Reply.chat == chat_id)\
            .join(Chat, Chat.id == Reply.chat)

        if not begin is None:
            query = query.where(Reply.time >= begin)
        if not end is None:
            query = query.where(Reply.time <= end)

        result = await self.__session.execute(query)
        record = result.first()
        return ChatReport(title=record[0], avg_delta=timedelta(seconds=int(record[1])), replies_count=record[2])

    async def employees_report(self, chat_id: int, begin: Optional[datetime] = None, end: Optional[datetime] = None) -> List[EmployeeStats]:
        query = select(Employee.full_name,
                       func.avg(Reply.delta),
                       func.count(Reply.employee))\
            .where(Reply.chat == chat_id)\
            .group_by(Reply.employee)\
            .join(Employee, Employee.id == Reply.employee)

        if not begin is None:
            query = query.where(Reply.time >= begin)
        if not end is None:
            query = query.where(Reply.time <= end)

        result = await self.__session.execute(query)
        return list(map(lambda record: EmployeeStats(full_name=record[0], avg_delta=timedelta(seconds=int(record[1])), replies_count=record[2]),
                        result.all()))
