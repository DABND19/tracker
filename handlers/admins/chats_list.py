from filters.admins import AdminsFilter
from aiogram import types
from aiogram.utils.markdown import bold
from aiogram.dispatcher.filters import Command
from aiogram.types.inline_keyboard import InlineKeyboardButton
from loader import dp, Session
from controllers.chat import ChatController


@dp.message_handler(Command(["chats"]), AdminsFilter())
async def chats_list_handler(message: types.Message):
    async with Session() as session:
        chat_controller = ChatController(session)
        chats = await chat_controller.get_list()
    keyboard = types.InlineKeyboardMarkup()
    for chat in chats:
        keyboard.add(InlineKeyboardButton(chat.title, callback_data=f"chat_{chat.id}"))
    await message.answer(bold("Active chats: "), reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN)
