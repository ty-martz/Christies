# test page: https://www.christies.com/lot/lot-6361810?ldp_breadcrumb=back&intObjectID=6361810&from=salessummary&lid=1

# TO DO:
    # update currecy exchange
    # change image url to download and save
        # Local sample
        # storage options - Google, Dropbox, zip, DB setup?


import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, urlretrieve
import json
from forex_python.converter import CurrencyRates
import datetime

#page = 'https://www.christies.com/lot/lot-6361810?ldp_breadcrumb=back&intObjectID=6361810&from=salessummary&lid=1'
#page = 'https://www.christies.com/lot/lot-6361828?ldp_breadcrumb=back&intObjectID=6361828&from=salessummary&lid=1'
page = 'https://www.christies.com/lot/a-fatimid-shallow-glass-dish-probably-egypt-6361829/?intObjectID=6361829&lid=1'
year = 2022
month = 3
day = 1 # default to first of the month for currency conversions

htmldata = urlopen(page)
soup = BeautifulSoup(htmldata, 'html.parser')

#retreive item name, image url, and filename
image = soup.find_all('img', {'class':'chr-img'})[0]
item_name = image['alt'].strip()
img = image['src'].split('?')[0]
img_name = img.split('/')[-1]

# save image to dir
save_image = False
if save_image:
    urlretrieve(img, f'data/sample_imgs/{img_name}')

# find unique lot_header in html
lot_head = str(soup.find_all('div', {'class':'chr-lot-header__thumbnails'})[0]).split('data-namespace="')[1].split('"')[0]

# get data from JS
script = soup.find_all('script')[15].text
try:
    data = script.split(f"window.chrComponents.{lot_head} = ", 1)[1].rsplit(';', 1)[0]
except:
    pass
data = json.loads(data)

# extract price and currency
price = data['data']['lots'][0]['price_realised']
currency = data['data']['lots'][0]['price_realised_txt'].strip().split(' ')[0]

converter = CurrencyRates()
conv_date = datetime.datetime(year, month, day,11,0,0,0)
rate = converter.get_rate('USD', currency, conv_date)
usd_price = converter.convert('USD', currency, price, conv_date)

print_vals = True
if print_vals:
    print(item_name)
    print(img)
    print(f'Local currency price = {currency} {price}')
    print(f'FXRate = {rate}')
    print(f'Converted to USD = {usd_price}')
