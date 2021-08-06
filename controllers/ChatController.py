class ChatController:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def create(self, chat: types.Chat):
    #     await self.session.add(
    #        Employee(id=chat.id, title=chat.title) 
    #     )

    # async def delete(self, chat: types.Chat):
    # 	  await self.session.execute(
    #             delete(Chat).where(Chat.id == chat.id)
    #         )

    # async def get_all_ids(self):
    # 	result = await self.session.execute(
    # 		select(Chat.id)
    # 		)
    # 	return result.all()


    def create(self, chat: types.Chat):
        self.session.add(
           Chat(id=chat.id, title=chat.title) 
        )

    def delete(self, chat: types.Chat):
    	self.session.execute(
    			delete(Chat).where(Chat.id == chat.id)
    		)

    def get_all_ids(self):
    	result = self.session.execute(
    		select(Chat.id)
    		)
    	return result.all()