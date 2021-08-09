from typing import Union
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from loader import Session
from controllers.employee import EmployeeController


class AdminsFilter(BoundFilter):
    async def check(self, obj: Union[types.Message, types.CallbackQuery]) -> bool:
        if isinstance(obj, types.Message):
            user = obj.from_user
        elif isinstance(obj, types.CallbackQuery):
            user = obj.message.from_user
        else:
            return False

        async with Session() as session:
            employee_controller = EmployeeController(session)
            admins_ids = employee_controller.get_admins_ids()

        return user.id in admins_ids
