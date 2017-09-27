# coding=utf-8
import telebot
import os
import infounibot.util as util


# Get the bot token fron the enviromental variables
BOT_TOKEN = os.environ["bot_token"]
bot = telebot.TeleBot(BOT_TOKEN)

str_welcome = 'Benvenuto nel fantastico UniBot'

@bot.message_handler(commands=['start'])
def subscribe(message):
    id = message.chat.id
    print(str(id))
    util.add_id(id)
    bot.reply_to(message,str_welcome)



print("Polling...")

bot.polling()
