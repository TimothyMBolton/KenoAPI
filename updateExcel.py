import pandas as pd
import json, time
from kenoMasterFileCreator import utc_to_local
from datetime import datetime

# df = pd.read_json('./Data/MasterData.json')
# df = df.drop(columns=['_type'])
columns = ['Data Number', 'Games Ago', 'Closed', 'Draw Number', 'Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5', 'Ball 6', 'Ball 7', 'Ball 8', 'Ball 9', 'Ball 10', 'Ball 11', 'Ball 12', 'Ball 13', 'Ball 14', 'Ball 15', 'Ball 16', 'Ball 17', 'Ball 18', 'Ball 19', 'Ball 20', 'Bonus', 'Heads or Tails']
df = pd.DataFrame(columns = columns)
start = time.perf_counter()
with open('MasterData.json') as f:
    data = json.load(f)
    data = data[-10000:]
    for value, object in enumerate(data):
        Closed = utc_to_local(object['closed'])
        Closed = datetime(year = Closed.year, month = Closed.month, day=Closed.day, hour = Closed.hour, minute = Closed.minute, second = Closed.second)
        if(value % 1000 == 0):
            print(value)
        df = df.append({
        'Data Number': value + 1, #value+1
        'Games Ago': len(data) - value, 
        'Closed': Closed, 
        'Draw Number': object['game-number'], 
        'Ball 1': object['draw'][0], 
        'Ball 2': object['draw'][1], 
        'Ball 3': object['draw'][2], 
        'Ball 4': object['draw'][3], 
        'Ball 5': object['draw'][4], 
        'Ball 6': object['draw'][5], 
        'Ball 7': object['draw'][6], 
        'Ball 8': object['draw'][7], 
        'Ball 9': object['draw'][8], 
        'Ball 10': object['draw'][9], 
        'Ball 11': object['draw'][10], 
        'Ball 12': object['draw'][11], 
        'Ball 13': object['draw'][12], 
        'Ball 14': object['draw'][13], 
        'Ball 15': object['draw'][14], 
        'Ball 16': object['draw'][15], 
        'Ball 17': object['draw'][16], 
        'Ball 18': object['draw'][17], 
        'Ball 19': object['draw'][18],
        'Ball 20': object['draw'][19],
        'Bonus': object['variants']['bonus'],
        'Heads or Tails': object['variants']['heads-or-tails']['result']
        }, ignore_index=True)

end = time.perf_counter()

df.to_excel(r'./Master Data.xlsx', index = False, sheet_name='Master Data')
print('before')
print(df.tail())

print(f'It took {end-start} seconds to complete')