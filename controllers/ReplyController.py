class ReplyController:
    def __init__(self, session: AsyncSession):
        self.session = session

    #async funcs

    # async def create(self, question: types.Message, reply: types.Message, employee: types.User, chat: types.Chat):
    #     await self.session.add(
    #        Reply(id=question.message_id, time=reply.date, delta=int(reply.date.timestamp() - question.date.timestamp()), employee=employee.id, chat=chat.id) 
    #     )

    # async def avg_for(self, begin: datetime, end: datetime, chat: types.Chat):
    #     result = await self.session.execute(select(func.avg(Reply.delta).label("avg_delta"))\
    #         .filter(Reply.time >= begin, Reply.time <= end)\
    #         .group_by(Reply.chat)\
    #         .having(Reply.chat == chat.id)
    #         )
    #     return result.first()


    def create(self, question: types.Message, reply: types.Message, employee: types.User, chat: types.Chat):
        self.session.add(
           Reply(id=question.message_id, time=reply.date, delta=int(reply.date.timestamp() - question.date.timestamp()), employee=employee.id, chat=chat.id) 
        )

    def avg_for(self, begin: datetime, end: datetime, chat: types.Chat):
    	result = self.session.execute(select(func.avg(Reply.delta).label("avg_delta"))\
    		.filter(Reply.time >= begin, Reply.time <= end, Reply.chat == chat.id)\
    		)
    	return result.first()