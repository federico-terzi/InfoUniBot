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

messages = ""

for event in calendar.get_upcoming_events(remaining_time=86400*2, min_difference=86400):
    message = event.message()
    messages += message + "\n\n"

# CAMBIARE CHAT ID
bot.send_message(0, messages, parse_mode='Markdown')