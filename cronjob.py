from __future__ import print_function
import telebot, os

from infounibot import util
from infounibot.google_cal import CalendarReader

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

print("Loading upcoming events...")

message = calendar.get_tomorrow_message()

ids = util.get_ids()

print("Sending message to subscribers:", len(ids))

for id in ids:
    print("Sending to:", id)
    bot.send_message(id, message, parse_mode='Markdown')