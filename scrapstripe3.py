

import requests

payload = {'inUserName': 'admin@fyre.fr', 'inUserPass': ''}
urlid='https://alleatone.fr/admin/login'
url1 = 'https://alleatone.fr/admin/stores?date=&date_in=01%2F06%2F2020&date_out=01%2F05%2F2020&distributor_id=&store_name=Poissonerie+Manda'
with requests.Session() as s:
    p=s.post(urlid, data=payload)
    print(p.text)

    r=s.get(url1)
    print(r.text)

