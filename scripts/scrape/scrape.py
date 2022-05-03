from collector import get_christies_data

def main():
    yrs = [2010]
    scrape_data = get_christies_data(years=yrs)
    if len(yrs) == 1:
        scrape_data.to_csv(f'data/christies_data_{yrs[0]}.csv')
    else:
        min_yr = min(yrs)
        max_yr = max(yrs)
        scrape_data.to_csv(f'data/christies_data_{min_yr}_{max_yr}.csv')

if __name__ == '__main__':
    main()