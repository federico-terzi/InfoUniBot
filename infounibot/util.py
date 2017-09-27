import csv
import os

home_dir = os.path.expanduser('~')
path = os.path.join(home_dir,'ids.txt')

def add_id(id):
    ids = get_ids()
    found = False
    for idz in ids :
        if(idz == id ):
            found = True
            break
    if not found:
        file = open(path,"a")
        writer = csv.writer(file)
        writer.writerow([id])
        file.close()

def get_ids():
    try:
        file = open(path,"r")
    except IOError:
        return []  # Modificato per restituire lista vuota, piu comoda cosi non serve fare un controllo prima
    reader = csv.reader(file)
    data = []
    for row in reader :
        data.append(int(row[0]))
    file.close()
    return data

def remove_id(del_id):
    ids = get_ids()
    file = open(path ,"w")
    writer = csv.writer(file)
    for id in ids:
        if(id != del_id):
            writer.writerow([id])
    file.close()


class MessageHandler(object):
    """
    Classe usata per gestire i messaggi inviati/ricevuti
    """
    def __init__(self):
        # Genero il percorso del file
        home_dir = os.path.expanduser('~')
        self.path = os.path.join(home_dir, 'messages.txt')

        # Carica tutti i messaggi inviati
        self.messages = []

        try:
            with open(self.path, "r") as f:
                self.messages = map(lambda x: x.strip(), f.readlines())
        except Exception as e:
            print(e)

    def save_messages(self):
        """
        Saves the messages
        """
        lines = '\n'.join(self.messages)
        try:
            with open(self.path, "w") as f:
                f.write(lines)
        except Exception as e:
            print(e)

    def mark_event_as_sent(self, event_id, chat_id):
        """
        Mark a message as sent for a specific chat
        """
        token = event_id + "-" + str(chat_id)
        if token not in self.messages:
            self.messages.append(token)
            self.save_messages()

    def was_event_sent(self, event_id, chat_id):
        """
        Check if an event was already sent to a chat
        """
        token = event_id + "-" + str(chat_id)
        return token in self.messages
