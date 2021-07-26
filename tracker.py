import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import json

TELE_TOKEN = "1704348480:AAF9LGs3FSyeJSwigwZnBt61nuIWsyEQTRU"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

ourids = [
    666165975,  # Grant
    488599080,  # Roma
    843657228,  # Mark
    1649362951,  # Vasya
    414371773,  # Alexei
    488523849,  # Lyosha
    1005293020,  # Dima
    257372634,  # Kavi
    553439580,  # Val
    232146889,  # Fedor
    387778961  # Yulia
]


class Tracker:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__data = {}
        self.__staffs = []

        self.__load_staffs()
        self.__load_cache()

    def __load_cache(self):
        pass

    def __load_staffs(self):
        self.__staffs = ourids

    def __get_chat_data(self, chat):
        return self.__data.setdefault(chat.id, {
            "title": chat.title,
            "deltas": [],
            "unanswered_messages": [],
        })

    def __message_handler(self, update, context):
        message = update.message
        chat = update.message.chat

        if chat.type == "private":
            return

        chat_data = self.__get_chat_data(chat)

        if message.from_user.id in self.__staffs:
            if len(chat_data["unanswered_messages"]) == 0:
                return

            first_unanswered_message = chat_data["unanswered_messages"][0]
            delta = message.date - first_unanswered_message.date
            chat_data["deltas"].append(delta.seconds)
            chat_data["unanswered_messages"].clear()
        else:
            chat_data["unanswered_messages"].append(message)

    def __report_handler(self, update, context):
        chat = update.message.chat

        deltas = self.__get_chat_data(chat)["deltas"]

        try:
            avg_time = sum(deltas) / len(deltas)
            minutes = avg_time // 60
            seconds = int(avg_time % 60)
            message = f"В текущем чате среднее время ответа составляет {minutes} минут {seconds} секунд"
        except ZeroDivisionError:
            message = "Статистика по текущему чату пока недоступна"

        update.message.reply_text(message)

    def __get_raw_data_handler(self, update, message):
        update.message.reply_text(str(self.__get_chat_data()))

    def __error_handler(self, update, context):
        self.logger.warning(f"Update {update} caused error {context.error}")

    def start(self):
        self.__updater = Updater(TELE_TOKEN, use_context=True)
        dispatcher = self.__updater.dispatcher

        dispatcher.add_handler(CommandHandler("report", self.__report_handler))
        dispatcher.add_handler(CommandHandler(
            "raw", self.__get_raw_data_handler))
        dispatcher.add_handler(MessageHandler(
            Filters.text, self.__message_handler))
        dispatcher.add_error_handler(self.__error_handler)

        self.__updater.start_polling()
        self.__updater.idle()


if __name__ == "__main__":
    tracker = Tracker()
    tracker.start()
