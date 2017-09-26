import telepot
from telepot.loop import MessageLoop
import time
import csv


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    #riconoscimento input
    if content_type == 'text' and  msg['text'] == '/start':
        print(chat_id)
        control = True
        control_file = open("notify.csv","r")
        control_reader = csv.reader(control_file)

        for row in control_reader :
            if not control :
                break
            print(row)
            if row == [str(chat_id)] :
                control = False
        control_file.close()
        if control :
            notify_file = open("notify.csv", "a")
            writer = csv.writer(notify_file)
            writer.writerow([str(chat_id)])
            bot.sendMessage(chat_id, str_welcome)
            notify_file.close()
        else:
            bot.sendMessage(chat_id, "Sei già registrato")







token = '476538995:AAHelMdFw_UZI_e_AceSpAvtV3hZKvEq9OE'

bot = telepot.Bot(token)



str_welcome = 'Benvenuto nel fantastico UniBot'

MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)

