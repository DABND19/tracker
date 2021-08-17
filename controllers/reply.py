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
            Reply(question_time=question.date,
                  reply_time=reply.date,
                  employee=reply.from_user.id,
                  chat=reply.chat.id)
        )

    @staticmethod
    def select_replies_deltas(*fields):
        return select(*fields, func.extract("epoch", Reply.reply_time - Reply.question_time).label("delta_seconds"))

    async def chat_report(self, chat_id: int) -> Optional[ChatReport]:
        replies_deltas = self.select_replies_deltas(Reply.chat)\
            .where(Reply.chat == chat_id)\
            .subquery()
        subquery = select(replies_deltas.c.chat,
                          func.avg(replies_deltas.c.delta_seconds).label("avg_delta"),
                          func.count().label("replies_count"))\
                              .group_by(replies_deltas.c.chat).cte()

        query = select(subquery, Chat.title)\
            .join(Chat, subquery.c.chat == Chat.id)

        result = await self._session.execute(query)
        record = result.first()

        if record is None:
            return None

        return ChatReport(title=record.title, avg_delta=timedelta(seconds=int(record.avg_delta)), replies_count=record.replies_count)

    async def employees_report(self, chat_id: int) -> List[EmployeeStats]:
        replies_deltas = self.select_replies_deltas(Reply.employee)\
            .where(Reply.chat == chat_id)\
            .subquery()
        subquery = select(replies_deltas.c.employee,
                          func.avg(replies_deltas.c.delta_seconds).label("avg_delta"),
                          func.count(replies_deltas.c.employee).label("replies_count"))\
            .group_by(replies_deltas.c.employee)\
            .cte()

        query = select(subquery, Employee.full_name)\
            .join(Employee, subquery.c.employee == Employee.id)

        result = await self._session.execute(query)
        return list(map(lambda record: EmployeeStats(full_name=record.full_name, avg_delta=timedelta(seconds=int(record.avg_delta)), replies_count=record.replies_count), result.all()))
