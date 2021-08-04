from datetime import datetime, timezone

string = '2021-07-15 13:45:20+10:00'

def stringToDate(time):
    utc_dt = datetime(year = int(time[:4]), month = int(time[5:7]), day = int(time[8:10]), hour = int(time[11:13]), minute = int(time[14:16]), second = int(time[17:19]), tzinfo=timezone.utc)
    utc_dt = utc_dt.strftime("%d/%m %H:%M")

    return utc_dt


if __name__ == '__main__':
    print(stringToDate(string).strftime("%d/%m %H:%M"))