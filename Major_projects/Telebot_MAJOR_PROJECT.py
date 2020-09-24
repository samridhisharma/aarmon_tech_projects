from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import requests as req
import json

updater = Updater(token='1384782785:AAGjava3k42vR2qTaf2oAGjj_jGGCjBENYw', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Have a great day!")

# WEATHER OF DELHI
def weatherInfo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Wait! We are fetching for the results")

    response = req.get("https://api.openweathermap.org/data/2.5/weather?q=delhi&appid=37643fffe08d4b8b453d5781ef356c29")

    response_text = response.text

    response_dict = json.loads( response_text )

    temperature = str(int( response_dict["main"]["temp"] ) - 273)
    humidity   = str(int(response_dict["main"]["humidity"] ))

    context.bot.send_message(chat_id=update.effective_chat.id, text="Temperature of delhi is: "+temperature+"\nHumidity in delhi is: "+ humidity)
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Humidity of delhi is %s"%humidity)


# COVID STATUS
def covidInfo(update, context):
    print("Searching for result")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Wait! We are fetching for the results")

    response = req.get("https://api.covid19india.org/v3/data-all.json")

    if response.status_code == 200:

        print("Result received")

        dict_data = json.loads(response.text)
        dict_data_today = dict_data['2020-06-11']


        ansToSend=""
        printedNothing=True

        for state, values in dict_data_today.items():

            ansToSend+="state: "+state+"\n"

            try:
                total_confirmed = int( values["total"]["confirmed"] )
                total_tested    = int( values["total"]["tested"] )
                total_death     = int( values["total"]["deceased"])

                ratio_confirmed_vs_tested = (total_confirmed / total_tested ) * 100
                ratio_death_vs_confirmed = (total_death / total_confirmed ) * 100

                ansToSend += "\ttest_ratio : "+str(ratio_confirmed_vs_tested)+"\n\tdeath_ratio : "+str(ratio_death_vs_confirmed)+"\n\n"
                printedNothing=False
            except:
                print("Some error occured")
        
        if printedNothing:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Data not available")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=ansToSend)

    else:

        context.bot.send_message(chat_id=update.effective_chat.id, text="Data not available")

def workHandle(update, context):

    msg = update.message.text.lower()
    if msg.find("weather")>-1:

        weatherInfo(update, context)
    
    elif msg.find("covid")>-1:

        covidInfo(update, context)

def unknownCommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# USER ARTICLE
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id='1',
            title='Weather',
            input_message_content=InputTextMessageContent("Get weather info")
        )
    )
    results.append(
        InlineQueryResultArticle(
            id='2',
            title='Covid',
            input_message_content=InputTextMessageContent("Get covid info")
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

start_handler = CommandHandler('start', start)
start_handler = CommandHandler('stop', stop)
work_handler = MessageHandler(Filters.text & (~Filters.command), workHandle)
unknown_handler = MessageHandler(Filters.command, unknownCommand)
inline_caps_handler = InlineQueryHandler(inline_caps)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(work_handler)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
