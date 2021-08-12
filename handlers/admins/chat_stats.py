from aiogram import types
from aiogram.utils.markdown import text, bold, pre
from aiogram.dispatcher.filters import Text
from loader import dp, Session
from controllers.reply import ReplyController
from itertools import chain
from tabulate import tabulate


@dp.callback_query_handler(Text(startswith="chat_"))
async def chat_stats_handler(callback_query: types.CallbackQuery):
    _, chat_id = callback_query.data.split("_")
    chat_id = int(chat_id)
    async with Session() as session:
        reply_controller = ReplyController(session)
        chat_report = await reply_controller.chat_report(chat_id)
        employees_report = await reply_controller.employees_report(chat_id)
        if chat_report.avg_delta is None:
            await callback_query.answer("We don't have stats for this chat")
            return

        table = tabulate({
            "Name": chain(map(lambda employee: employee.full_name, employees_report)),
            "Avg": chain(map(lambda employee: employee.avg_delta, employees_report), [chat_report.avg_delta]),
            "Count": chain(map(lambda employee: employee.replies_count, employees_report), [chat_report.replies_count])
        }, tablefmt="plain", headers="keys")

        payload = text(bold(chat_report.title), pre(table), sep="\n")

        await callback_query.message.edit_text(payload, parse_mode=types.ParseMode.MARKDOWN)
