import requests


url = input('url: ')

res = requests.get(url)

page = str(res.text)


with open('req.html', 'w', encoding='utf-8') as file:
        file.write(page)