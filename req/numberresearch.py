import requests
import time
import threading

api = 'https://numberresearch.xyz/api/check'
num = 51
found = False

while not found:
    print(num)
    req = requests.post(api, json={"number": str(num)})
    try:
        if req.json()['is_new']:
            found = True
    except KeyError:
        print(req.json())
    num += 1
