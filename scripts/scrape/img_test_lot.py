import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, urlretrieve
import json
from forex_python.converter import CurrencyRates
import datetime

site = 'https://www.christies.com/en/auction/art-of-the-islamic-and-indian-worlds-including-oriental-rugs-and-carpets-29639/'

source = requests.get(site).text

soup = BeautifulSoup(source, 'html.parser')

# get lot page data from JS
script = soup.find_all('script')[17].text
try:
    data = script.split(f"window.chrComponents.lots = ", 1)[1].rsplit(';', 1)[0]
except:
    pass
data = json.loads(data)

lot_data = data['data']['lots']

df = pd.DataFrame(lot_data)

#### Get lot links
links = []
for i in df['url']:
    print(i)
    links.append(i)