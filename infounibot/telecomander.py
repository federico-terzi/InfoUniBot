import os
import csv
import uuid



def formatta(testo):
    testo=str(testo).replace("[", "").replace("]", "").replace("'", "").replace('"','');
    return testo
def formatta_id(testo):
    return testo.replace("[", "").replace("]", "")

def scriviAvviso(avviso):
    if ':' in avviso:
        file = open(path, "a")
        avviso="{id}:{avviso}".format(id=uuid.uuid4(),avviso=avviso)
        csv_writer = csv.writer(file)
        csv_writer.writerow([avviso])
        file.close()

def list_avvisi():
    file = open(path,"r")
    csv_reader = csv.reader(file)
    data = []
    for row in csv_reader:
        row = str(row).split(":")
        d ={"id":str(row[0]),'titolo':formatta(row[1]).upper(),'testo':formatta(row[2])}
        data.append(d)
    file.close()
    return data

def elimina_avviso(number):
    list = list_avvisi()
    i = 0
    print(str(list))
    file = open(path, "w")
    csv_writer = csv.writer(file)
    if(number-1< len(list)):
        list.pop(number-1)
    for el in list:
        avviso = "{id}:{titolo}:{avviso}".format(id=formatta(el['id']),titolo=formatta(el['titolo']),avviso=formatta(el['testo']))
        csv_writer.writerow([avviso])
    file.close()

home_dir = os.path.expanduser('~')
path = os.path.join(home_dir,'avvisi.txt')

elimina_avviso(1)