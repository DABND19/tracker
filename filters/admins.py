from data.store.admins import AdminsStore
from typing import Union
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class AdminsFilter(BoundFilter):
    async def check(self, obj: Union[types.Message, types.CallbackQuery]) -> bool:
        if isinstance(obj, types.Message):
            user = obj.from_user
        elif isinstance(obj, types.CallbackQuery):
            user = obj.message.from_user
        else:
            return False

        return await AdminsStore.contains(user.id)
