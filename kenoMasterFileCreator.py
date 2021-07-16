import os, time
import json
from pprint import pprint
import datetime
import pytz
from datetime import datetime, timezone

def first10chars(x):
    return(x[:10])

def utc_to_local(time):
    utc_dt = datetime(year = int(time[:4]), month = int(time[5:7]), day = int(time[8:10]), hour = int(time[11:13]), minute = int(time[14:16]), second = int(time[17:19]), tzinfo=timezone.utc)
    local_tz = pytz.timezone('Australia/Sydney') 
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) 

def writeToJsonFile(fileName, jsonData):
    print(fileName)
    with open(fileName, 'w') as outfile:
        json.dump(jsonData, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)


def sortDict(unsorted, key):
    print('sortDict')
    reversed = False
    sortedDict = sorted(unsorted, key=lambda i: i[key], reverse=reversed)
    return sortedDict


def createMaster():
    start = time.perf_counter()
    directory = r'./Data/'
    res = []
    count = 0
    sortedFileList = sorted(os.listdir(directory), key = first10chars)

    for filename in sortedFileList:
        filename = './Data/' + filename

    for filename in sorted(os.listdir(directory), key = first10chars):
        if filename.endswith(".json"):
            count+=1
            filename = f'./Data/{filename}'
            with open(filename) as f:
                for value, object in enumerate(json.load(f), 1):
                    #object['closed'] = str(utc_to_local(object['closed']))
                    res.append(object)
        else:
            continue
    
    unique = { each['closed'] : each for each in res }.values()
    
    writeToJsonFile("MasterData.json", sortDict(list(unique), 'closed') )
    print(f'It Took {time.perf_counter() - start:.3f} seconds to create MasterData.json')

def verifyMasterData():
    with open('MasterData.json') as f:
        data = json.load(f)
    unique = { each['closed'] : each for each in data }.values()
    print(len(unique), len(data))

def main():
    createMaster()

if __name__ == '__main__':
    main()