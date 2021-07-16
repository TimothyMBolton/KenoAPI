import json
from datetime import date, datetime
from kenoAPI import updateMasterData
from KenoFunctions import analyseAllCombinations, analyseCustomSets, analyseMumsNumbers
import time

mumsNumbers = [2, 9, 16, 21, 27, 69]
allNumbers = [x for x in range(1, 81)]


def main():
    updateMasterData()
    start = time.perf_counter()
    with open('./MasterData.json') as f:
        games = json.load(f)
    print(f'It took {time.perf_counter() - start} seconds to read MasterData.json')
    print(len(games))
    analyseMumsNumbers(games)
    # analyseAllCombinations(games, 3)

if __name__ == '__main__':
    main()