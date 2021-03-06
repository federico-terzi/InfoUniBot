# coding=utf-8
import telebot
import os

import time

import infounibot.util as util
import infounibot.google_cal as cal
import infounibot.telecomander as tc
from telebot import types

# Get the bot token fron the enviromental variables
BOT_TOKEN = os.environ["bot_token"]
bot = telebot.AsyncTeleBot(BOT_TOKEN)

str_welcome = """Benvenuto nel fantastico *UniBot*! 🎉

Ti terrò informato di tutte le lezioni, gli esami e gli avvisi.

Se hai bisogno di informazioni, puoi chiedermele quando vuoi con questi comandi:

/domani permette di vedere le lezioni di domani.
/oggi permette di vedere le lezioni rimaste di oggi.

Puoi disabilitare le notifiche in qualunque momento digitando: 
/stop

Grazie e a presto! :)
"""


markup = types.ReplyKeyboardMarkup(row_width=2)

itembtn1 = types.KeyboardButton('/domani')
itembtn2 = types.KeyboardButton('/oggi')
markup.add(itembtn1, itembtn2)

@bot.message_handler(commands=['avvisi','Avvisi'])
def show_avvisi(message):
    text = 'AVVISI:\n'
    i = 1
    avvisi = tc.list_avvisi()
    if(len(avvisi) != 0):
        for avviso in avvisi:
            text=text+("#{id}:*{titolo}*\n{avviso}\n\n").format(id=i,titolo=avviso['titolo'],avviso=avviso['testo'])
            i=i+1
    else:
        text=text+"*Non ci sono nuovi avvisi*"
    bot.send_message(message.chat.id,text,parse_mode='Markdown')

@bot.message_handler(commands=['add','Add'])
def inserisci_avviso(message):
    text = message.text # (?)
    text = text.strip()
    text = text[4:]
    #if(message.chat.id == 0):#inseriremo i nostri ID manualmente , purtroppo
    tc.scriviAvviso(text)

@bot.message_handler(commands=['rm','Rm'])
def elimina_avviso(message):
    text = message.text
    text = text.strip()
    text = text[3:4]

    #if(message.chat.id ==0):
    tc.elimina_avviso(int(text))


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
    text = calendar.get_tomorrow_full_message()
    print(str(text))
    bot.send_message(message.chat.id, text, parse_mode='Markdown')  # Serve ad aggiungere la formattazione tipo grassetto

@bot.message_handler(commands=['oggi', 'Oggi'])
def send_today(message):
    calendar = cal.CalendarReader()
    calendar.load_events()
    text = calendar.get_today_full_message()
    print(str(text))
    bot.send_message(message.chat.id, text, parse_mode='Markdown')  # Serve ad aggiungere la formattazione tipo grassetto

@bot.message_handler(commands=['resetcache'])
def reset_cache(message):
    calendar = cal.CalendarReader()
    calendar.reset_event_cache()
    bot.send_message(message.chat.id, "Cache Eventi resettata!", parse_mode='Markdown')


# Eseguo il polling, con recupero in caso di errore
print("Polling...")
bot.polling(none_stop=True, timeout=60)
