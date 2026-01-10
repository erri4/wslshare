import datetime
import requests

date = str(datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day))
wordle = "https://www.nytimes.com/svc/wordle/v2/" + date + ".json"
connctions = "https://www.nytimes.com/svc/connections/v2/" + date + ".json"

wreq = requests.get(wordle)
print('WORDLE:')
print(wreq.json()['solution'])
creq = requests.get(connctions)
print('CONNECTIONS:')
for category in creq.json()['categories']:
    for card in category['cards']:
        print(card['content'], end=' ')
    print()