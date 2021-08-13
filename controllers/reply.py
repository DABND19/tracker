from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, func
from aiogram import types
from models import Reply, Employee, Chat
from typing import Optional, NamedTuple, List, Optional


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
        self._session = session

    def create(self, question: types.Message, reply: types.Message):
        self._session.add(
            Reply(time=reply.date,
                  delta=(reply.date - question.date).total_seconds(),
                  employee=reply.from_user.id,
                  chat=reply.chat.id)
        )

    async def chat_report(self, chat_id: int) -> Optional[ChatReport]:
        subquery = select(Reply.chat,
                          func.avg(Reply.delta).label("avg_delta"),
                          func.count(Reply.id).label("replies_count"))\
            .group_by(Reply.chat)\
            .where(Reply.chat == chat_id)\
            .subquery()

        query = select(subquery, Chat.title).join(Chat)

        result = await self._session.execute(query)
        record = result.first()
        
        if record is None:
            return None
        
        return ChatReport(title=record.title, avg_delta=timedelta(seconds=int(record.avg_delta)), replies_count=record.replies_count)

    async def employees_report(self, chat_id: int) -> List[EmployeeStats]:
        subquery = select(Reply.employee,
                          func.avg(Reply.delta).label("avg_delta"),
                          func.count(Reply.employee).label("replies_count"))\
            .where(Reply.chat == chat_id)\
            .group_by(Reply.chat, Reply.employee)\
            .subquery()

        query = select(subquery, Employee.full_name).join(Employee)

        result = await self._session.execute(query)
        return list(map(lambda record: EmployeeStats(full_name=record.full_name, avg_delta=timedelta(seconds=int(record.avg_delta)), replies_count=record.replies_count),
                        result.all()))
