import os
import csv

def scriviAvviso(avviso):
    file = open(path, "a")
    csv_writer = csv.writer(file)
    csv_writer.writerow([avviso])
    file.close()



def list_avvisi():
    file = open(path,"r")
    csv_reader = csv.reader(file)
    data = []
    for row in csv_reader:
        data.append(row)
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

scriviAvviso('merda')
scriviAvviso('cavolo')
scriviAvviso('shit')
elimina_avviso(2)
print(str(list_avvisi()))