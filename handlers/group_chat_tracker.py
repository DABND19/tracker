from filters import TrackedGroupsFilter
from aiogram import types
from loader import dp, Session, chats_store
from controllers.reply import ReplyController
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types.chat import ChatType
from data.store.employees import EmployeeStore


@dp.message_handler(ChatTypeFilter(chat_type=[ChatType.GROUP]), TrackedGroupsFilter())
async def group_chat_tracker(message: types.Message) -> None:
    store = chats_store[message.chat.id]
    async with store.lock, Session() as session:
        if await EmployeeStore.contains(message.from_user.id):
            if not store.unanswered_messages:
                return

            question = store.unanswered_messages[0]
            reply_controller = ReplyController(session)
            reply_controller.create(question, reply=message)
            store.unanswered_messages.clear()
            await session.commit()
        else:
            store.unanswered_messages.append(message)
