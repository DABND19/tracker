class EmployeeController:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def create(self, user: types.User):
    #     await self.session.add(
    #        Employee(id=user.id, username=user.username, fullname=user.fullname) 
    #     )

    # async def delete(self, user: types.User):
    # 	await self.session.delete(
    # 			Employee(id=user.id)
    # 		)

    # async def get_all_ids(self):
    # 	result = await self.session.execute(
    # 		select(Employee.id)
    # 		)
    # 	return result.all()


    def create(self, user: types.User):
        self.session.add(
           Employee(id=user.id, username=user.username, fullname=user.full_name) 
        )

    def delete(self, user: types.User):
    	self.session.execute(
    			delete(Employee).where(Employee.id == user.id)
    		)

    def get_all_ids(self):
    	result = self.session.execute(
    		select(Employee.id)
    		)
    	return result.all()