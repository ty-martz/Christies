from clean_auction_data import *

def main(url=True, algo=True):
    raw_data = pd.read_csv('data/christies_data.csv')
    df = clean_data(raw_data)
    if url:
        links = create_url_table(df)
        links.to_csv('data/auction_links.csv')
    if algo:
        mod = create_model_table(df)
        mod.to_csv('data/model_data.csv')

if __name__ =='__main__':
    main()
