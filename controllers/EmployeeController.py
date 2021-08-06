from models import Employee
from sqlalchemy.sql import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import types


class EmployeeController:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create(self, user: types.User):
        self.__session.add(
            Employee(id=user.id,
                     username=user.username,
                     full_name=user.full_name)
        )

    async def delete(self, user: types.User):
        await self.__session.execute(delete(Employee).where(Employee.id == user.id))

    async def get_all_ids(self):
        result = await self.__session.execute(select(Employee.id))
        return result.all()
