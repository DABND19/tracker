from typing import Union
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from loader import chats_store


class TrackedGroupsFilter(BoundFilter):
    async def check(self, obj: Union[types.Message, types.CallbackQuery, types.ChatMemberUpdated]) -> bool:
        if isinstance(obj, types.Message):
            chat = obj.chat
        elif isinstance(obj, types.CallbackQuery):
            chat = obj.message.chat
        elif isinstance(obj, types.ChatMemberUpdated):
            chat = obj.chat
        else:
            return False

        return chat in chats_store
