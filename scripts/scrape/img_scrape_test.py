# test page: https://www.christies.com/lot/lot-6361810?ldp_breadcrumb=back&intObjectID=6361810&from=salessummary&lid=1

import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import json

#page = 'https://www.christies.com/lot/lot-6361810?ldp_breadcrumb=back&intObjectID=6361810&from=salessummary&lid=1'
#page = 'https://www.christies.com/lot/lot-6361828?ldp_breadcrumb=back&intObjectID=6361828&from=salessummary&lid=1'
page = 'https://www.christies.com/lot/a-fatimid-shallow-glass-dish-probably-egypt-6361829/?intObjectID=6361829&lid=1'

htmldata = urlopen(page)
soup = BeautifulSoup(htmldata, 'html.parser')
image = soup.find_all('img', {'class':'chr-img'})[0]

img = image['src'].split('?')[0]
item_name = image['alt'].strip()

lot_head = str(soup.find_all('div', {'class':'chr-lot-header__thumbnails'})[0]).split('data-namespace="')[1].split('"')[0]
script = soup.find_all('script')[15].text
#load price from javascript
try:
    data = script.split(f"window.chrComponents.{lot_head} = ", 1)[1].rsplit(';', 1)[0]
except:
    pass
data = json.loads(data)
price = data['data']['lots'][0]['price_realised']

print_vals = True
if print_vals:
    print(item_name)
    print(img)
    print(price)