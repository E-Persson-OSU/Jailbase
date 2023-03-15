""" imports list """
import http.client
import json
import csv
import time
import config
import random
import services.db as db

"""global variables"""
conn = http.client.HTTPSConnection("jailbase-jailbase.p.rapidapi.com")

headers = config.headers

"""run this to search chosen jail for records containing first and last name"""
def searchjailbase(source_id, last_name, first_name=""):
    searcharg = ""
    if len(first_name) > 0:
        searcharg = "/search/?source_id={}&last_name={}&first_name={}".format(source_id, last_name, first_name)
    else:
        searcharg = "/search/?source_id={}&last_name={}".format(source_id, last_name)
    conn.request("GET", searcharg, headers=headers)
    data = ''
    while True:
        try:
            res = conn.getresponse()
            data = res.read()
            data = data.decode("utf-8")
            data = json.loads(data)
            break
        except ValueError:
            print('Gateway Timeout, trying again...')

    return data

"""run this to get list of ohio jails"""
def getsourceids():
    conn.request("GET", "/sources/", headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    sourceids = []
    records = data["records"]
    for record in records:
        sourceids.append(record["source_id"])        
    return sourceids

def getnamedict():
    name = []
    namedict = []
    with open('names.csv', newline='') as namefile:
        reader = csv.DictReader(namefile)
        for row in reader:
            name = [row['last_name'], row['first_name']]
            namedict.append(name)
    return namedict

"""grab recent from random sourceid and """
def getrecent():
    sourceids = getsourceids()
    random_id = random.choice(sourceids)
    conn.request("GET", "/recent/?source_id={}".format(random_id), headers=headers)
    attempts = 0
    while True:
        try:
            res = conn.getresponse()
            data = res.read()
            data = data.decode("utf-8")
            data = json.loads(data)
            break   
        except (json.decoder.JSONDecodeError, http.client.ResponseNotReady) :
            print("Server error 500, trying again")
            time.sleep(2)
            attempts = attempts + 1
            if attempts > 2:
                data = db.getrecentdb()
                break
    
    records = data["records"]
    db.addrecentdb(records)
    return records


def main(args):
    namedict = []
    name = ["",""]
    args.pop(0)
    if len(args) == 2:
        name[0] = (args[0])
        name[1] = (args[1])
    elif len(args) == 1:
        name[0] = (args[0])
    namedict.append(name)

    sourceidlist = getsourceids()
    bookinglist = []
    
    for sourceid in sourceidlist:
        print("Now searching {} for {}, {}".format(sourceid, name[0], name[1]))
        record = searchjailbase(sourceid,name[0],name[1])
        if len(record['records']) > 0:
            for booking in record['records']:
                bookinglist.append(booking)
    print(bookinglist)
