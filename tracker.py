import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests
import urllib.request
import json
    

import pandas as pd
import datetime
from datetime import datetime
import math
import time




# токен бота
tele_TOKEN = '1704348480:AAF9LGs3FSyeJSwigwZnBt61nuIWsyEQTRU'


av_times = {}

# our ids
ourids = ['666165975', '488599080', '843657228', '1649362951', '414371773', '488523849', '1005293020', '257372634', '5534439580', '232146889', '387778961' ]
# Grant, Roma, Mark, Vasya, Alexei, Lyosha, Dima, Kavi, Val, Fedor, Yula



# заполнение словаря av_times по файлу
while True:
    try:
        chats_df = pd.read_csv('av_times.csv')
        chats = chats_df.columns.tolist()
        
        i = 0
        for i in range(1, len(chats)):
            av_times[chats[i]] = {'last_message_time':chats_df[chats[i]][0], 'last_delta':chats_df[chats[i]][1], 'average_time_between': chats_df[chats[i]][2], 'cnt': chats_df[chats[i]][3], 'status':chats_df[chats[i]][4], 'ids': chats_df[chats[i]][5]}
        break
    except(FileNotFoundError):
        chats= []
        break


# тут должно быть заполнение списка айдишников по файлу (заполнения оставь на мне)
# while True:
#     try:
#         ids_df = pd.read_csv('our_ids.csv')
#         col = ids_df.columns.tolist()
        
#         i = 0
#         for i in range(1, len(col)):
#             av_times[chats[i]] = {'last_message_time':chats_df[chats[i]][0], 'last_delta':chats_df[chats[i]][1], 'average_time_between': chats_df[chats[i]][2], 'cnt': chats_df[chats[i]][3], 'status':chats_df[chats[i]][4], 'ids': chats_df[chats[i]][5]}
#         break
#     except(FileNotFoundError):
#         chats= []
#         break





print(av_times)    
print(chats)







# Enable logging (логи)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)




# добавить чат в базу данных и иництализировать поля таблицы
def add_chat(update, context):
    if len(context.args) >= 2:
        av_times[context.args[0]] = {'last_message_time': 0 , 'last_delta':0, 'average_time_between':0, 'cnt':0, 'status':0 , 'ids':''} 
        ids = []
        for i in range (1, len(context.args)):
            ids.append(context.args[i])
        av_times[context.args[0]]['ids'] = ids



    print(av_times)  
    df = pd.DataFrame.from_records(av_times)
    df.to_csv('av_times.csv') 
    update.message.reply_text('Информация о чате добавлена.')



# главная (сейчас не рабочая) функция, которая будет высчитывать среднее время ожидания
# нужно прописать два пути развития: 1) если чат только инициализирован (то есть cnt = 0) 2) если он уже в базе данных
# update - это то, что слушает. То есть, update.message - это вновь пришедешее сообщение
# context.args - массив аргументов
def av_time(update , context):
    #  если новый чат
    if (update.message['chat']['title'] not in chats) and (update.message['chat']['type'] != 'private'): 
       
        t = update.message['date'].timestamp()
        av_times[update.message['chat']['title']] = {'last_message_time':t,'last_delta':t, 'average_time_between':0, 'cnt':1}
        chats.append(update.message['chat']['title'])
        print(av_times)

    else:
        t_new = update.message['date'].timestamp()
        
        av_times[update.message['chat']['title']]['last_delta'] = t_new - av_times[update.message['chat']['title']]['last_message_time']
        av_times[update.message['chat']['title']]['cnt'] += 1
        av_times[update.message['chat']['title']]['average_time_between'] = (av_times[update.message['chat']['title']]['average_time_between'] + av_times[update.message['chat']['title']]['last_delta'])/av_times[update.message['chat']['title']]['cnt']
        av_times[update.message['chat']['title']]['last_message_time'] = t_new

    
    print(update.message['date'])
    df = pd.DataFrame.from_records(av_times)
    df.to_csv('av_times.csv')  



# если ошибка, то бот не упадет, но напишет в логи
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)



# вернуть в чат инфу краствую (старое)
def get_data(update, context):
    print(chats, av_times)
    i = 0
    text = 'Информация по времени ответа: \n'
    for i in range(1, len(chats)):
        text += 'В чате ' + chats[i] + ' разница между последними сообщениями = ' + str( divmod(av_times[chats[i]]['last_delta'], 60)[0] ) + ' минут ' + str( divmod(av_times[chats[i]]['last_delta'], 60)[1] ) +' секунд; среднее время между сообщениями = ' +  str( divmod(av_times[chats[i]]['average_time_between'], 60)[0]   ) + ' минут ' + str( divmod(av_times[chats[i]]['average_time_between'], 60)[1] )+ ' секнуд\n\n'
    print(text)
    update.message.reply_text(text)



# тупо вернуть словарь
def get_raw_data(update, context):
    update.message.reply_text(str(av_times))



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(tele_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    

    #  Это командны
    dp.add_handler(CommandHandler("data", get_data ))
    dp.add_handler(CommandHandler("raw", get_raw_data))
    dp.add_handler(CommandHandler("add", add_chat))


    # on noncommand i.e message -
    # это на прослушку      
    dp.add_handler(MessageHandler(Filters.text, av_time))
    
    
    # log all errors
    dp.add_error_handler(error)



    updater.start_polling()
    updater.idle()
    
    

if __name__ == '__main__':
    main()