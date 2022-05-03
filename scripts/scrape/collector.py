import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import json

def get_christies_data(years=list(range(2010, 2021))):
    
    merge_list = []
    for y in years:
        for m in list(range(1,13)):
            try:
                site = 'https://www.christies.com/en/results?month=' + str(m) + '&year=' + str(y) + ''
            except:
                print(str(m) + '/' + str(y) + ' could not parse')
            source = requests.get(site).text

            soup = BeautifulSoup(source, 'html.parser')

            #### Get auction locations, titles, and links
            locs = []
            for i in soup.find_all('div', {'class':'chr-event-tile__details-footer'}):
                locs.append(i.find('span', {'class':'chr-body'}).text)

            titles = []
            links = []
            for i in soup.find_all('a', {'class':'chr-event-tile__title'}):
                titles.append(i.text.strip())
                links.append(i['href'])

            for title, loc, link in zip(titles, locs, links):
                try:
                    info = urlopen(str(link)).read()
                except:
                    print('error on detail link')
                soup = BeautifulSoup(info, features="html.parser")
                script = soup.findAll('script')[16].text

                #load data info from javascript
                try:
                    data = script.split("window.chrComponents.lots = ", 1)[1].rsplit(';', 1)[0]
                except:
                    continue
                data = json.loads(data)
                lot_data = data['data']['lots']

                df = pd.DataFrame(lot_data)

                # make pandas series of title and location toappend to df
                df['lot_title'] = [title] * len(df)
                df['location'] = [loc] * len(df)

                merge_list.append(df)
                #print('lot complete')
        print('year ' + str(y) + ' complete!')

    output = pd.concat(merge_list,ignore_index=True)

    return output

