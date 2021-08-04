import glob
import os
import os
import shutil
from typing import Generator
import requests
import json
from datetime import date, datetime, timedelta
from pprint import pprint
from kenoMasterFileCreator import createMaster, first10chars
import time


URL_RECENT_GAMES = 'https://api-info-nsw.keno.com.au/v2/info/history?jurisdiction=NSW'
urlTest = 'https://api-info-nsw.keno.com.au/v2/info/history?jurisdiction=NSW&starting_game_number=600&number_of_games=200&date=2021-07-07&page_size=20&page_number=1'

STARTING_GAME = 600
NUMBER_OF_GAMES = 100
DATE = 3
CURRENT_DATE = date.today()
URL = 'https://api-info-nsw.keno.com.au/v2/info/history?jurisdiction=NSW&starting_game_number={STARTING_GAME}&number_of_games={NUMBER_OF_GAMES}&date={DATE}&page_size={NUMBER_OF_GAMES}&page_number=1'

URLTEST2017 = 'https://api-info-nsw.keno.com.au/v2/info/history?jurisdiction=NSW&starting_game_number=0&number_of_games=200&date=2017-11-22&page_size=200&page_number=1'


MASTER_URL = 'https://api-info-nsw.keno.com.au/v2/info/history?jurisdiction=NSW&starting_game_number=600&number_of_games=200&date=2021-07-07&page_size=20&page_number=1'

def getGames(STARTING_GAME, DATE, NUMBER_OF_GAMES=200):
    URL = f'https://api-info-nsw.keno.com.au/v2/info/history?jurisdiction=NSW&starting_game_number={STARTING_GAME}&number_of_games={NUMBER_OF_GAMES}&date={DATE}&page_size={NUMBER_OF_GAMES}&page_number=1'
    data = requests.get(URL).json()
    return data

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def findTodaysGames(debug=False):
    count = 0
    startDate = date.today()
    numberOfGames = 200
    endGame = requests.get(URL_RECENT_GAMES).json()['items'][0]['game-number']
    startGame = findStartGame(date.today(), debug, endGame)
    step = 300
    res = []
    length = 1
    while length > 0:
        games = getGames(startGame, startDate, numberOfGames)
        length = len(games['items'])
        for game in games['items']:
            res.append(game)
        startGame += numberOfGames
        startGame %= 1000
    for i, game in enumerate(res):
        if(game['game-number'] == endGame):
            res = res[:i+1]
    return res

def findStartGame(date, debug=False, endGame = 999):
    global globalCount
    count = 0
    currentGame = endGame
    foundStartGame = False
    step = 900
    if(endGame < 999):
        step = 250
    length = 0
    while not foundStartGame:
        try:
            length = len(getGames(currentGame, date)['items'])
        except KeyError:
            pass

        if(debug):
            print(f'{length = }, {currentGame = }, {step = }, {count = }')

        if(length > 0):
            currentGame -= step
            currentGame %= 1000
            step = max(int(step/2), 1)
        else:
            currentGame += step
            currentGame %= 1000
            # step = max(int(step/2), 1)
        try:
            if(len(getGames(currentGame, date)['items']) > 0 and len(getGames((currentGame - 1)%1000, date)['items']) <= 0):
                return currentGame
            elif(len(getGames((currentGame + 1)%1000, date)['items']) > 0 and len(getGames(currentGame, date)['items']) <= 0):
                return currentGame + 1

        except KeyError:
            if(currentGame == 999 or currentGame == 0):
                if(len(getGames(0, date)['items']) > 0 and  len(getGames(999, date)['items']) == 0):
                    return 0
            currentGame += step
            currentGame %= 1000
        count += 1
        if(count > 50):
            return -1
    return -1

def findIndexOfLastSavedGame(gamesToAdd, lastSavedGame):
    for i, object in enumerate(gamesToAdd):
            if(object['game-number'] == lastSavedGame):
                return i

def updateMasterData(fileName="MasterData.json"):
    start = time.perf_counter()
    directory = r'./Data/'
    sortedFileList = sorted(os.listdir(directory), key = first10chars)
    sortedFileList.remove('.DS_Store')
    dateR = sortedFileList[-1][:10]
    lastDateDownloaded = date(year= int(dateR[:4]), month = int(dateR[5:7]), day = int(dateR[8:10]))
    
    with open(directory + sortedFileList[-1]) as f:
        data = json.load(f)
        lastGameDownloaded = data[1]['game-number']

    today = date.today()
    with open(fileName) as f:
        data = json.load(f)
    
    if(lastDateDownloaded == date.today()):
        writeToJsonFile('./Data/' + str(date.today()) + ' Keno Games.json', findTodaysGames())
        createMaster()
    else:
        writeToJsonFile('./Data/' + str(date.today()) + ' Keno Games.json', findTodaysGames())
        for singleDate in daterange(lastDateDownloaded, date.today()):
            writeToJsonFile('./Data/' + str(singleDate) + ' Keno Games.json', findDaysGames(singleDate))
        createMaster()
    print(f'It Took {time.perf_counter() - start} seconds to update the games')
    # writeToJsonFile("MasterData.json", data)
    
def findDaysGames(startDate, debug=False):
    res = []
    endDate = startDate + timedelta(days=1)
    startGame = findStartGame(startDate, debug)
    endGame = findStartGame(endDate, debug)
    length = 1
    numberOfGames = 200
    while length > 0:
        print(f'{startGame = } {startDate = } {numberOfGames = }')
        games = getGames(startGame, startDate, numberOfGames)
        length = len(games['items'])
        for game in games['items']:
            res.append(game)
        startGame += numberOfGames
        startGame %= 1000
    for i, game in enumerate(res):
        if(game['game-number'] == endGame):
            res = res[:i+1]
    return res

def moveFiles():
    sourcepath='./'
    sourcefiles = os.listdir(sourcepath)
    destinationpath = './Data'
    for file in sourcefiles:
        if file.endswith('.json'):
            shutil.move(os.path.join(sourcepath,file), os.path.join(destinationpath,file))

def writeToJsonFile(fileName, jsonData):
    if os.path.exists(fileName):
        print('File Exists')
    else:
        createMaster()
    
    with open(fileName, 'w') as outfile:
        json.dump(jsonData, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)

def main():
    updateMasterData()
    # today = date.today() - timedelta(days=1)
    # print(findDaysGames(today)[-1]['game-number'])

if __name__ == '__main__':
    main()
