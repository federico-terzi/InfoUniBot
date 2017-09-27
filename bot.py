# coding=utf-8
import telebot
import os
import infounibot.util as util
import infounibot.google_cal as cal
from telebot import types

# Get the bot token fron the enviromental variables
BOT_TOKEN = os.environ["bot_token"]
bot = telebot.TeleBot(BOT_TOKEN)

str_welcome = """Benvenuto nel fantastico *UniBot*! 🎉

Ti terrò informato di tutte le lezioni, gli esami e gli avvisi.

Se hai bisogno di informazioni, puoi chiedermele quando vuoi con questi comandi:

/domani permette di vedere le lezioni di domani.

Puoi disabilitare le notifiche in qualunque momento digitando: 
/stop

Grazie e a presto! :)
"""


markup = types.ReplyKeyboardMarkup(row_width=2)

itembtn2 = types.KeyboardButton('/domani')
markup.add(itembtn2)


@bot.message_handler(commands=['start','Start'])
def subscribe(message):
    id = message.chat.id
    print(str(id))
    util.add_id(id)
    bot.send_message(id, str_welcome, reply_markup=markup, parse_mode='Markdown')  # Serve ad aggiungere la formattazione tipo grassetto

@bot.message_handler(commands=['stop','Stop'])
def unsub(message):
    id = message.chat.id
    util.remove_id(id)
    bot.reply_to(message,"Non riceverai più nessuna notifica.\n Grazie e alla prossima volta!.")

@bot.message_handler(commands=['domani','Domani'])
def send_tomorrow(message):
    calendar = cal.CalendarReader()
    calendar.load_events()
    text = calendar.get_tomorrow_message()
    print(str(text))
    bot.send_message(message.chat.id, parse_mode='Markdown')  # Serve ad aggiungere la formattazione tipo grassetto

print("Polling...")

bot.polling(none_stop=True)
