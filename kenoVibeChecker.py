import json
import argparse
from os import read
import sys
from KenoFunctions import singleGameWinner, readCustomFile, open_file
from kenoMasterFileCreator import utc_to_local
from datetime import datetime


def vibeCheck(games):
    sets = readCustomFile('./Sets/vibeCheckSets.txt')
    with open('./MasterData.json') as f:
        data = json.load(f)

    data = data[-int(games):]
    res = []
    for set in range(len(sets)):
        count = 0
        for value, object in enumerate(data):
            if(singleGameWinner(object['draw'], sets[set])):
                count += 1
        res.append({
            'Set': sets[set],
            'Count': count
        })

    Closed = utc_to_local(data[-1]['closed'])
    Closed = datetime(year=Closed.year, month=Closed.month, day=Closed.day,
                      hour=Closed.hour, minute=Closed.minute, second=Closed.second)

    with open('vibeCheckResults.txt', 'w') as f:
        f.write(str(Closed) + '\n\n')
        for value, object in enumerate(res):
            res[value]['Set'] = sorted(res[value]['Set'])
            f.write(f"{res[value]['Set']} Count: {res[value]['Count']}\n\n")

    open_file('vibeCheckResults.txt')


def main():
    try:
        vibeCheck(sys.argv[1])
    except IndexError:
        print("You need to tell me how many games you want to vibe check!")


if __name__ == '__main__':
    main()
