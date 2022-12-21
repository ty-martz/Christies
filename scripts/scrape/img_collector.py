import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, urlretrieve
import json
from forex_python.converter import CurrencyRates
import datetime

def get_christies_images(years=list(range(2010, 2021))):
    
    merge_list = []
    for y in years:
        for m in list(range(1,13)):
            try:
                site = 'https://www.christies.com/en/results?month=' + str(m) + '&year=' + str(y) + ''
            except:
                print(str(m) + '/' + str(y) + ' could not parse')
            source = requests.get(site).text

            soup = BeautifulSoup(source, 'html.parser')

            #### Get lot links from month history
            links = []
            for i in soup.find_all('a', {'class':'chr-event-tile__title'}):
                links.append(i['href'])

            # go through each lot link
            for link in links:
                try:
                    info = urlopen(str(link)).read()
                except:
                    print('error on detail link')
                soup = BeautifulSoup(info, features="html.parser")

                #in each lot, access the specific item
                script = soup.find_all('script')[17].text
                try:
                    data = script.split(f"window.chrComponents.lots = ", 1)[1].rsplit(';', 1)[0]
                except:
                    pass
                data = json.loads(data)

                lot_data = data['data']['lots']

                df = pd.DataFrame(lot_data)

                #### Get item links
                item_links = []
                for i in df['url']:
                    print(i)
                    item_links.append(i)

                item_details = []
                # loop through each item in the lot
                for ilink in item_links:

                    htmldata = urlopen(ilink)
                    soup = BeautifulSoup(htmldata, 'html.parser')

                    #retreive item name, image url, and filename
                    image = soup.find_all('img', {'class':'chr-img'})[0]
                    item_name = image['alt'].strip()
                    img = image['src'].split('?')[0]
                    img_name = img.split('/')[-1]
                    
                    #### save image to dir ####
                    urlretrieve(img, f'data/imgs/{img_name}')

                    script = soup.findAll('script')[16].text

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
                    conv_date = datetime.datetime(y, m, 1,11,0,0,0)
                    #rate = converter.get_rate('USD', currency, conv_date)
                    usd_price = converter.convert('USD', currency, price, conv_date)
                    item_details.append([img_name, img, usd_price])
                merge_list.append(item_details)
        print('year ' + str(y) + ' complete!')

    output = pd.concat(merge_list, columns=['img_title', 'img_file', 'usd_price'], ignore_index=True)

    return output

