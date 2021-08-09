from datetime import timedelta
from aiogram import types
from aiogram.utils.markdown import text, bold
from aiogram.dispatcher.filters import Text
from loader import dp, Session
from controllers.reply import ReplyController
import asyncio


@dp.callback_query_handler(Text(startswith="chat_"))
async def chat_stats_handler(callback_query: types.CallbackQuery):
    _, chat_id = callback_query.data.split("_")
    chat_id = int(chat_id)
    async with Session() as session:
        reply_controller = ReplyController(session)
        chat_report, employees_report = await asyncio.gather(reply_controller.chat_report(chat_id),
                                                             reply_controller.employees_report(chat_id))
        if chat_report.avg_delta is None:
            await callback_query.answer("We don't have stats for this chat")
            return

        payload = text(bold(chat_report.title),
                       *map(lambda employee: f"{employee.full_name}: {employee.avg_delta}", employees_report),
                       f"Total for this chat: {chat_report.avg_delta}",
                       sep="\n")

        await callback_query.message.edit_text(payload, parse_mode=types.ParseMode.MARKDOWN)
