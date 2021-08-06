from aiogram import types
from loader import dp, chats_store
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types.chat import ChatType


#add question_filter
@dp.message_handler(ChatTypeFilter([ChatType.GROUP]))
async def question_handler(message: types.Message) -> None:
    store = chats_store[message.chat.id]
    async with store.lock:
        store.unanswered_messages.append(message)
