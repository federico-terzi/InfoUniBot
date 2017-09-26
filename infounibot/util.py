import csv
import os

home_dir = os.path.expanduser('~')
path = os.path.join(home_dir,'ids.txt')

def add_id(id):
    file = open(path,"a")
    writer = csv.writer(file)
    writer.writerow([id])
    file.close()

def get_ids():
    file = open(path,"r")
    reader = csv.reader(file)
    data = []
    for row in reader :
        data.append(row)
    file.close()
    return data

def remove_id(del_id):
    ids = get_ids()
    file = open(path ,"w")
    writer = csv.writer(file)
    for id in ids:
        if(id != [str(del_id)]):
            writer.writerow(id)
    file.close()

add_id(123456)
add_id(123457)
add_id(123458)
remove_id(123456)
print(get_ids())