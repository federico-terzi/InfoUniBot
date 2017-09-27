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
    file = open(path, "w")
    csv_writer = csv.writer(file)
    if(number>0):
        for el in list:
            if(i != number-1):
                csv_writer.writerow(el)
                i+=1
    file.close()

home_dir = os.path.expanduser('~')
path = os.path.join(home_dir,'avvisi.txt')

