from collector import get_christies_data
from img_collector import get_christies_images

def main(meta=True, images=True, yrs=[2020]):
    if meta:
        scrape_data = get_christies_data(years=yrs)
        if len(yrs) == 1:
            scrape_data.to_csv(f'data/christies_data_{yrs[0]}.csv')
        else:
            min_yr = min(yrs)
            max_yr = max(yrs)
            scrape_data.to_csv(f'data/christies_data_{min_yr}_{max_yr}.csv')
    
    if images:
        img_data = get_christies_images(years=yrs)
        if len(yrs) == 1:
            img_data.to_csv(f'data/christies_images_{yrs[0]}.csv')
        else:
            min_yr = min(yrs)
            max_yr = max(yrs)
            img_data.to_csv(f'data/christies_images_{min_yr}_{max_yr}.csv')

if __name__ == '__main__':
    main()