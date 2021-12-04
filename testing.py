import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json, datetime
import requests, pytz
from datetime import datetime, timezone
from pprint import pprint

def hello_world(request):
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
    'projectId': 'keno-server-88b59',
    })
    db = firestore.client()

    res = ''
    URL = "https://api-info-nsw.keno.com.au/v2/info/history?jurisdiction=NSW"
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.3.1134600273.1625577500; _gcl_au=1.1.514206993.1625577500; _fbp=fb.2.1625577500326.865857123; _scid=d4b438be-a931-486b-83c2-07cc9f100eab; __qca=P0-1128952437-1625577500527; _sctr=1|1625493600000; mbox=PC#1dcf733c6a1741d6ac47a879d70391b9.36_0#1689229149|session#9101477eec104c1880e1fc501010b302#1625986208; _uetvid=a21bbb40de5c11ebaf5d79558ca8a75b",
    "Host": "api-info-nsw.keno.com.au",
    "If-None-Match": "W/\"1640-Wb4uuYFATz9ljhiafpHdHfhPeHA\"",
    "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    }
    data = requests.get(URL,  headers=headers).json()

    data = data['items']
    data = data[:5]
    docs = db.collection("lastAddedGame").stream()
    for doc in docs:
      max_game = doc.get('gamenumber')
      last_recorded_game = max_game
    
    last_game_added = -1
    mumsNumbersQuery = db.collection("MumsNumbers").stream()


    mumsSets = []
    for doc in mumsNumbersQuery:
        mumsSets.append(doc.to_dict())

    for setDict in mumsSets:
        setQuery = setDict['Set']
        for _, object in enumerate(reversed(data)):
            if(object['game-number'] > setDict['LastChecked'] or int(object['game-number']) == 0): #if the new game number is greater than the value of the last checked field
                if(set(setQuery).issubset(set(object['draw']))): #if its a winner
                    setDict['Games Ago'] = 0
                    setDict['LastChecked'] = object['game-number']
                    setDict['Draw Number'] = object['game-number'] 
                else: #if not a winner
                    setDict['LastChecked'] = object['game-number']
                    setDict['Games Ago'] += 1

                last_game_added = object['game-number']
    for doc in mumsSets:
        pprint(doc)
        db.collection("MumsNumbers").document(str(doc['Set'])).set(doc)

    db.collection("lastAddedGame").document('last_added_game').set({"gamenumber": last_game_added})
    return {"result": str(last_game_added)}