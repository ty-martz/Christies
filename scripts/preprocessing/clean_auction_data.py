import pandas as pd
import numpy as np

def clean_data(df):
    df = df[df['estimate_visible'] == True]

    # dropna based on lot title and price and fill
    df = df.dropna(subset=['title_primary_txt', 'price_realised'])
    fills = {'location':'unknown', 'consigner_information':'unknown'}
    df = df.fillna(value=fills)

    # create new columns
    titles = zip(df['title_primary_txt'], df['title_secondary_txt'])
    df['title_full'] = [f'{p}: {s}' if s is not np.nan else p for p,s in titles]

    # clean up description
    lis = [i.split('<BR>') for i in df['description_txt']]
    str_out = [''.join(lis[i][1:-1]).replace('/n','') for i, z in enumerate(lis)]
    df['clean_description'] = str_out

    # Format dates
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    cols_to_drop = ['Unnamed: 0', 'is_auction_over', 'is_in_progress', 
                'title_tertiary_txt', 'current_bid', 'current_bid_txt',
                'is_saved', 'show_save', 'current_bid', 'current_bid_txt',
                'price_realised_txt', 'lot_withdrawn', 'estimate_txt',
                'estimate_on_request', 'is_estimate_unknown', 'price_on_request',
                'title_secondary_txt', 'estimate_visible', 'image']
    return df.drop(cols_to_drop, axis=1)

def create_url_table(df):
    return df[['object_id', 'url']]

def create_model_table(df):
    return df.drop(['object_id', 'lot_id_txt', 'url', 'title_primary_txt', 
                      'description_txt'], axis=1)

