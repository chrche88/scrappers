

import requests
from bs4 import BeautifulSoup

url_login = "https://alleatone.fr/admin/login"

headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

payload = {
    '_token': '',
    'e-mail': 'admin@fyre.fr',
    'password': 'Fyre@ll3@t12020'
}
url1 = 'https://alleatone.fr/admin/stores?date=&date_in=01%2F06%2F2020&date_out=01%2F05%2F2020&distributor_id=&store_name=Poissonerie+Manda'
with requests.Session() as session:
    res = session.get(url_login)

    cookie_val = res.headers['Set-Cookie'].split(";")[0]
    headers['cookie'] = cookie_val

    soup = BeautifulSoup(res.text,"lxml")
    token = soup.select_one('input[name="_token"]')['value']
    payload['_token'] = token

    p = session.post(url_login,data=payload,headers=headers)
    print(p.content)
    r = session.get(url1,headers=headers)
