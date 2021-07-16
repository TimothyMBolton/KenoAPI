import pandas as pd
import itertools
import time
import os
import sys, datetime
import subprocess
from kenoMasterFileCreator import utc_to_local

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


mumsNumbers = [2, 9, 16, 21, 27, 69]
allNumbers = [x for x in range(1, 81)]


def singleGameWinner(game, playedNumbers):
    # print(f'{game = } {playedNumbers = }')
    if(set(playedNumbers).issubset(set(game))):
        return True
    else:
        return False


def getPowerSet(listOfNumbers, length):
    powerset = itertools.combinations(listOfNumbers, length)
    return list(set(powerset))


def sortDict(unsorted, key):
    reversed = False
    if(key == 'Set'):
        reversed = False
    else:
        reversed = True

    sortedDict = sorted(unsorted, key=lambda i: i[key], reverse=reversed)
    return sortedDict


def getRecentWinners(games, sets, key):
    totalGames = len(games)
    results = []

    for i in range(len(sets)):
        count = len(games)
        newCount = len(games)
        gamesAgo = -1
        foundGame = False
        while(not foundGame and count > 0):
            count -= 1
            newCount -= 1
            if(singleGameWinner(games[count]['draw'], sets[i])):
                foundGame = True
                gamesAgo = totalGames-newCount
                drawNumber = games[count]['game-number']
                results.append({
                    "Set": sets[i],
                    "Games Ago": int(gamesAgo),
                    "Draw Number": int(drawNumber),
                    "closed": utc_to_local(games[count]['closed'])
                })

    print('Finished Finding the Winners\n')
    return sortDict(results, key)


def writeWinners(games, fileName, setOfNumbers, setFlag=False, numbersPlayed=1, key='Set'):
    if(setFlag):
        sets = setOfNumbers
    else:
        sets = getPowerSet(setOfNumbers, numbersPlayed)
    
    results = getRecentWinners(games, sets, key)
    
    file = open(fileName, 'a')
    for i in range(len(results)):
        results[i]['Set'] = sorted(results[i]['Set'])
        file.write(f"{results[i]['Set']} Ago: {results[i]['Games Ago']} Draw: {results[i]['Draw Number']}\n")
        if(len(results[i]['Set']) > 4):
                file.write(str(results[i]['closed'])[:-6] + '\n')
        else:
            file.write('\n')
    file.write('\n')
    file.close()


def readCustomFile(fileName):
    a_file = open(fileName, "r")
    list = []
    for line in a_file:
        stripped_line = line.strip()
        line_list = set(stripped_line.split())
        list.append(line_list)

    a_file.close()
    for l in range(len(list)):
        list[l] = [int(item) for item in list[l]]

    if(len(list) == 1):
        return list[0]
    return list


def analyseMumsNumbers(games, filename = 'mumsResults.txt'):
    start = time.perf_counter()
    customSets = readCustomFile('./Sets/customSets.txt')
    if os.path.exists(filename):
        os.remove(filename)
        print("Removed Exististing Results File")
    else:
        print('Hello Father')
    with open('./mumsResults.txt', 'w') as f:
        f.write('Report Completed At: ' + str(datetime.datetime.today())[:-10] + '\n')

    for i in range(2, 6):
        writeWinners(games, filename, mumsNumbers, numbersPlayed= i+1)
    writeWinners(games, filename, customSets, True, key='Games Ago')

    print(
        f'It Took {time.perf_counter() - start} seconds to analyse mums numbers')

    open_file(filename)


def analyseCustomSets(games, filename='customSetsResults.txt'):
    if os.path.exists(filename):
        os.remove(filename)
        print("Removed Exististing Results File")
    else:
        print('Hello Father')

    writeWinners(games, filename, readCustomFile('customSets.txt'), True)
    open_file(filename)
    print('Analyse Custom Sets')


def analyseCustomNumbers(games, length = 3, filename='customNumbersResults.txt'):
    if os.path.exists(filename):
        os.remove(filename)
        print("Removed Exististing Results File")
    else:
        print('Hello Father')

    writeWinners(games, filename, readCustomFile('customNumbers.txt'), numbersPlayed= length, key='Games Ago')
    open_file(filename)
    print('Analyse Custom Numbers')


def analyseAllCombinations(games, length = 3):
    start = time.perf_counter()
    filename = "all" + str(length) + "Combinations.txt"
    if os.path.exists(filename):
        os.remove(filename)
        print("Removed Exististing Results File")
    else:
        print('Hello Father')

    writeWinners(games, filename, allNumbers, numbersPlayed= length, key='Games Ago')

    open_file(filename)
    print(
        f'It Took {time.perf_counter() - start:.3f} seconds to analyse all combinations of length {length}')


if __name__ == "__main__":
    print('Wrong file idiot')
