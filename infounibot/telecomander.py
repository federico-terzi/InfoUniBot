import os
import csv
import uuid



def formatta(testo):
    testo=str(testo).upper().replace("[", "").replace("]", "").replace("'", "").replace('"','');
    return testo


def scriviAvviso(avviso):
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
        d ={"id":row[0],'titolo':formatta(row[1]),'testo':formatta(row[2])}
        data.append(d)
    file.close()
    return data

def elimina_avviso(number):
    list = list_avvisi()
    i = 0
    print(str(list))
    file = open(path, "w")
    csv_writer = csv.writer(file)
    if(number>0):
        list.pop(number-1)
    for el in list:
        csv_writer.writerow(el)
    file.close()

home_dir = os.path.expanduser('~')
path = os.path.join(home_dir,'avvisi.txt')
