import requests


url = input('url: ')

res = requests.get(url)

page = str(res.text)

if 'never gonna' in page or 'rick roll' in page or 'rickroll' in page or 'rick' in page:
    print('dont open its a rickroll')
else:
        with open('req.html', 'w', encoding='utf-8') as file:
                file.write(page)
