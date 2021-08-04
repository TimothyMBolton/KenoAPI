import json
from datetime import date, datetime
from kenoAPI import updateMasterData
from KenoFunctions import analyseAllCombinations, analyseCustomSets, analyseMumsNumbers
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json, datetime
from pprint import pprint
import requests, pytz
from datetime import datetime, timezone


mumsNumbers = [2, 9, 16, 21, 27, 69]
allNumbers = [x for x in range(1, 81)]


def main():
    updateMasterData()
    with open('index.txt', 'w') as f:
        f.write(str(0))
    start = time.perf_counter()
    with open('./MasterData.json') as f:
        games = json.load(f)
    print(f'It took {time.perf_counter() - start} seconds to read MasterData.json')
    mumsResults = analyseMumsNumbers(games)
    pprint(mumsResults)
    mumsResults = [item for sublist in mumsResults for item in sublist]

    cred = credentials.ApplicationDefault()

    firebase_admin.initialize_app(cred, {
    'projectId': 'keno-server-88b59',
    })
    db = firestore.client()


    # for i, item in enumerate(mumsResults):
    #     addDoc = db.collection("MumsNumbers").document(str(item['Set']))
    #     addDoc.set(item)
    
if __name__ == '__main__':
    main()