from collector import get_christies_data

def main():
    scrape_data = get_christies_data()
    scrape_data.to_csv('christies_data.csv')

if __name__ == '__main__':
    main()