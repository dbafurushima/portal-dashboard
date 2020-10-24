import random

YEAR = '2020'
MONTH = '10'
DAY = 5

INI_HOUR = 0
INI_MIN = 0

FILENAME = 'data_with_year.txt'

fp = open(FILENAME, 'a+')

def make_info(last_hour, last_min, fp):
    global DAY
    global YEAR
    global MONTH
    if last_hour == 24:
        hour = 0
        DAY += 1
    else:
        hour = last_hour + 1

    if last_min == 60:
        minute = 0
    else:
        minute = last_min + 1

    strfmt = f'{YEAR}-{MONTH}-{DAY} {hour}:{minute},{random.randint(10, 100)}'
    fp.write(f'{strfmt}\n')
    return hour, minute

lh, lm = INI_HOUR, INI_MIN

for _ in range(200):
    lh, lm = make_info(lh, lm, fp)
fp.close()
