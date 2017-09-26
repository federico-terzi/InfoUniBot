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
    file = open(path,"r")
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
