from clean_auction_data import *

def main(url=True, csv=True, pickle=True):
    raw_data = pd.read_csv('data/christies_data.csv')
    df = clean_data(raw_data)
    if url:
        links = create_url_table(df)
        links.to_csv('data/auction_links.csv')
    if csv:
        mod = create_model_table(df)
        mod.to_csv('data/model_data.csv')
    if pickle:
        jar = create_model_table(df)
        jar.to_pickle('data/model_data.pkl')

if __name__ =='__main__':
    main(False, False, True)
