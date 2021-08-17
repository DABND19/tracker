from asyncio.locks import Lock
from controllers.chat import ChatController
from sqlalchemy.ext.asyncio import AsyncSession
from typing import NamedTuple, List
from aiogram import types


class ChatStore(NamedTuple):
    lock: Lock
    unanswered_messages: List[types.Message]


class ChatsStore:
    def __init__(self):
        self._data: dict[int, ChatStore] = {}

    async def load(self, session: AsyncSession) -> None:
        controller = ChatController(session)
        chats = await controller.get_all_ids()
        self._data = {
            chat_id: ChatStore(lock=Lock(), unanswered_messages=[]) for chat_id in chats
        }

    def __getitem__(self, key: int) -> ChatStore:
        return self._data[key]

    def __contains__(self, chat: types.Chat) -> bool:
        return chat.id in self._data.keys()
    
    def add_chat(self, chat: types.Chat) -> None:
        self._data.setdefault(chat.id, ChatStore(lock=Lock(), unanswered_messages=[]))
