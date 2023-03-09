""" imports list """
import http.client
import json
import csv
import sys
import config

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
    ohsourceids = []
    records = data["records"]
    for record in records:
        state = record["state_full"]
        if state.lower() == "ohio":
            ohsourceids.append(record["source_id"])
            
    return ohsourceids

def getnamedict():
    name = []
    namedict = []
    with open('names.csv', newline='') as namefile:
        reader = csv.DictReader(namefile)
        for row in reader:
            name = [row['last_name'], row['first_name']]
            namedict.append(name)
    return namedict


def main(args):
    namedict = []
    name = []
    if len(args) > 0:
        name.append(args[1])
        name.append(args[2])
        namedict.append(name)
    else:
        namedict = getnamedict()

    sourceidlist = getsourceids()
    bookinglist = []
    
    for sourceid in sourceidlist:
        print("Now searching {}".format(sourceid))
        for name in namedict:
                record = searchjailbase(sourceid,name[0],name[1])
                if len(record['records']) > 0:
                    for booking in record['records']:
                        bookinglist.append(booking)
    print(bookinglist)


main(sys.argv)