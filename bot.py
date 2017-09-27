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



#def handle(msg):
 #   content_type, chat_type, chat_id = telepot.glance(msg)
  #  print(content_type, chat_type, chat_id)
   # #riconoscimento input
    #if content_type == 'text' and  msg['text'] == '/start':
     #   util.add_id(chat_id)




print("Polling...")

bot.polling()



#MessageLoop(bot, handle).run_as_thread()
#print ('Listening ...')

# Keep the program running.
#while 1:
 #   time.sleep(10)

