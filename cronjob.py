from __future__ import print_function

import datetime
import telebot, os
from infounibot import util
from infounibot.google_cal import CalendarReader
from infounibot.util import MessageHandler

# IMPOSTAZIONI CRONJOB

NOTIFY_TOMORROW_EVENTS_HOUR = 20
NOTIFY_UPCOMING_EVENT_ALERT_TIME = 1800  # Mezzora prima

# Get the bot token fron the enviromental variables
BOT_TOKEN = os.environ["bot_token"]

bot = telebot.AsyncTeleBot(BOT_TOKEN)

print("InfoUniBot Calendar Check Cronjob Started...")

calendar = CalendarReader(avoid_caching=True)

print("Loading events...")

calendar.load_events()

if not calendar.has_events():
    print("No events.")
    quit()

# Carico l'ora attuale
now = datetime.datetime.now()

# Carica il MessageHandler
mh = MessageHandler()

# Prendo gli ID delle persone
ids = util.get_ids()

# MESSAGGIO DI NOTIFICA PER GLI EVENTI IMMINENTI

print("Loading upcoming events...")

upcoming_events = calendar.get_upcoming_events(remaining_time=NOTIFY_UPCOMING_EVENT_ALERT_TIME)

for event in upcoming_events:
    message = """
Ciao! Ti ricordo che tra poco iniziera' questa lezione:

{lezione}

Mi raccomando, arriva puntuale! :)
            """.format(lezione=event.message())
    for chat_id in ids:
        # Controllo che il messaggio non sia gia stato inviato all'utente
        if not mh.was_event_sent(event.id, chat_id):
            print("Sending to:", chat_id)
            bot.send_message(chat_id, message, parse_mode='Markdown')
            # Segno il messaggio come gia inviato all'utente
            mh.mark_event_as_sent(event.id, chat_id)
        else:
            print("Already sent to:", chat_id)

# MESSAGGIO DI NOTIFICA DEGLI EVENTI DI DOMANI

# Verifico se e' ora di inviare la notifica per domani
if now.hour == NOTIFY_TOMORROW_EVENTS_HOUR:
    print("Loading tomorrow events...")

    event_message, message_id = calendar.get_tomorrow_message()

    # Verifica che ci siano eventi per domani
    if message_id is not None:
        # Costruisco il messaggio
        message = """
Ciao! Ti ricordo che domani avrai queste lezioni:

{lezioni}

Mi raccomando, arriva preparato! :)
        """.format(lezioni=event_message)

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