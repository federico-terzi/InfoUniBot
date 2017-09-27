from __future__ import print_function
import telebot, os

from infounibot import util
from infounibot.google_cal import CalendarReader

# Get the bot token fron the enviromental variables
from infounibot.util import MessageHandler

BOT_TOKEN = os.environ["bot_token"]

bot = telebot.AsyncTeleBot(BOT_TOKEN)

print("InfoUniBot Calendar Check Cronjob Started...")

calendar = CalendarReader()

print("Loading events...")

calendar.load_events()

if not calendar.has_events():
    print("No events.")
    quit()

print("Loading upcoming events...")

message, message_id = calendar.get_tomorrow_message()

ids = util.get_ids()

print("Sending message to subscribers:", len(ids))

# Carica il MessageHandler
mh = MessageHandler()

for chat_id in ids:
    # Controllo che il messaggio non sia gia stato inviato all'utente
    if not mh.was_event_sent(message_id, chat_id):
        print("Sending to:", chat_id)
        bot.send_message(chat_id, message, parse_mode='Markdown')
        # Segno il messaggio come gia inviato all'utente
        mh.mark_event_as_sent(message_id, chat_id)
    else:
        print("Already sent to:", chat_id)