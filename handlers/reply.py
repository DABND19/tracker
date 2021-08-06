from loader import dp, chats_store, Session
from aiogram import types
from controllers.reply import ReplyController
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types.chat import ChatType


# add reply filter
@dp.message_handler(ChatTypeFilter([ChatType.GROUP]))
async def reply_handler(reply: types.Message) -> None:
    store = chats_store[reply.chat.id]
    async with store.lock, Session() as session:
        if not store.unanswered_messages:
            return

        question = store.unanswered_messages[0]
        reply_controller = ReplyController(session)
        await reply_controller.create(question, reply)
        store.unanswered_messages.clear()
        await session.commit()
