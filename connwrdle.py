import datetime
import requests

url = bytes.fromhex('7777772e6e7974696d65732e636f6d2f7376632f').decode()
date = str(datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day + 1))
w = f"https://www.nytimes.com/svc/{bytes.fromhex('574f52444c45').decode().lower()}/v2/" + date + ".json"
c = f"https://www.nytimes.com/svc/{bytes.fromhex('434f4e4e454354494f4e53').decode().lower()}/v2/" + date + ".json"

wreq = requests.get(w)
print(bytes.fromhex('574f52444c453a').decode())
print(wreq.json()['solution'])
creq = requests.get(c)
print(bytes.fromhex('434f4e4e454354494f4e533a').decode())
for category in creq.json()['categories']:
    for card in category['cards']:
        print(card['content'], end=' ')
    print()