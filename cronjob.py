import telebot, os
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

upcoming_events = calendar.get_tomorrow_events()

if len(upcoming_events) == 0:
    print("No upcoming events.")
    quit()

messages = ""

for event in upcoming_events:
    message = event.message()
    messages += message + "\n\n"

bot.send_message(298233140, messages, parse_mode='Markdown')