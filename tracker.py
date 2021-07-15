import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests
import urllib.request
import json

import telepot

import pandas as pd
import datetime
from datetime import datetime
import math
import time


main_coins = ['bitcoin', 'ethereum']
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTMsInJvbGUiOiJhZG1pbjEiLCJsb2dpbiI6IlZhbGVyaXkiLCJpYXQiOjE2MjYxNjE3NzQsImV4cCI6MTYyNjI0ODE3NH0.NPDHCL2Ux6C7Tv6DjIx0e4yyFaHSCRMP5-VV7I3BxzA'
tele_TOKEN = '1704348480:AAF9LGs3FSyeJSwigwZnBt61nuIWsyEQTRU'
chat_id = '-564875501'

av_times = {}
while True:
    try:
        chats_df = pd.read_csv('av_times.csv')
        chats = chats_df.columns.tolist()
        
        i = 0
        for i in range(1, len(chats)):
            av_times[chats[i]] = {'last_message_time':chats_df[chats[i]][0], 'last_delta':chats_df[chats[i]][1], 'average_time_between': chats_df[chats[i]][2], 'cnt': chats_df[chats[i]][3]}
        break
    except(FileNotFoundError):
        chats= []
        break
# если делаем отчет в день х, то есть баланс на 00:00 дня х. Тогда отчет для дня с 29 на 30, нужны такие даты

print(av_times)    
headers = {'Cookie':'token='+TOKEN}





def telegram_bot_sendtext(bot_message):
    
    bot_token = '1880188697:AAHzKOFN3HqgU5b4672z2RORjT8br9gU0js'
    bot_chatID = '-564875501'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    
    
    response = requests.get(send_text)

    return response.json()






autotable = []
bot = telepot.Bot(tele_TOKEN)






#PORT = int(os.environ.get('PORT', 8443))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



    






def av_time(update , context):
    # if update.message['chat']['id'] in chats:
    #     message_time = update.message['date']
    
    if (update.message['chat']['title'] not in chats) and (update.message['chat']['type'] != 'private'): 
        t = update.message['date'].timestamp()
        av_times[update.message['chat']['title']] = {'last_message_time':t,'last_delta':t, 'average_time_between':0, 'cnt':0}
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

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def get_data(update, context):
    print(chats, av_times)
    i = 0
    text = 'Информация по времени ответа: \n'
    for i in range(1, len(chats)):
        text += 'В чате ' + chats[i] + ' разница между последними сообщениями = ' + str(av_times[chats[i]]['last_delta']) + '; среднее время ожидания = ' + str(av_times[chats[i]]['average_time_between']) + '\n\n'
    print(text)
    update.message.reply_text(text)


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
    
    dp.add_handler(CommandHandler("data", get_data ))
    dp.add_handler(CommandHandler("raw", get_raw_data))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, av_time))
    
    
    # log all errors
    dp.add_error_handler(error)

    
        
    # updater.start_webhook(listen="0.0.0.0",
    #                           port=int(PORT),
    #                           url_path=TOKEN)
    # updater.bot.setWebhook('https://fierce-badlands-07220.herokuapp.com/ ' + TOKEN)

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.

    updater.start_polling()
    updater.idle()
    
    

if __name__ == '__main__':
    main()