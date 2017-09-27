from __future__ import print_function

import datetime
import telebot, os
from infounibot import util
from infounibot.google_cal import CalendarReader
from infounibot.util import MessageHandler

# IMPOSTAZIONI CRONJOB

NOTIFY_TOMORROW_EVENTS_HOUR = 20

# Get the bot token fron the enviromental variables
BOT_TOKEN = os.environ["bot_token"]

bot = telebot.AsyncTeleBot(BOT_TOKEN)

print("InfoUniBot Calendar Check Cronjob Started...")

calendar = CalendarReader()

print("Loading events...")

calendar.load_events()

if not calendar.has_events():
    print("No events.")
    quit()

# Carico l'ora attuale
now = datetime.datetime.now()

# Carica il MessageHandler
mh = MessageHandler()

# MESSAGGIO DI NOTIFICA DEGLI EVENTI DI DOMANI

# Verifico se e' ora di inviare la notifica per domani
if now.hour == NOTIFY_TOMORROW_EVENTS_HOUR:
    print("Loading tomorrow events...")

    event_message, message_id = calendar.get_tomorrow_message()

    # Costruisco il messaggio
    message = """
Ciao! Ti ricordo che domani avrai queste lezioni:

{lezioni}

Mi raccomando, arriva preparato! :)
    """.format(lezioni=event_message)

    ids = util.get_ids()

    print("Sending tomorrow message to subscribers:", len(ids))

    for chat_id in ids:
        # Controllo che il messaggio non sia gia stato inviato all'utente
        if not mh.was_event_sent(message_id, chat_id):
            print("Sending to:", chat_id)
            bot.send_message(chat_id, message, parse_mode='Markdown')
            # Segno il messaggio come gia inviato all'utente
            mh.mark_event_as_sent(message_id, chat_id)
        else:
            print("Already sent to:", chat_id)