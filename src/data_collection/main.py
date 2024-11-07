import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_listing_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for item in soup.find_all('a', class_='Link Link_js_inited Link_size_m Link_theme_islands SerpItemLink OffersSerpItem__link OffersSerpItem__titleLink'):
        link = item.get('href')
        if link and '/offer/' in link:
            links.append(link)
    print(links)
    return links


def parse_listing(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('h1', class_='OfferCardSummaryInfo__description--3-iC7').text.strip()
    price = soup.find('span', class_='OfferCardSummaryInfo__price--2FD3C OfferCardSummaryInfo__priceWithLeftMargin--3I6Y8').text.strip()
    description = soup.find('p', class_='OfferCardTextDescription__text--2jHPh').text.strip()
    
    sales_history = []
    for sale in soup.find_all('div', class_='sale-history'):
        date = sale.find('span', class_='date').text.strip()
        price = sale.find('span', class_='price').text.strip()
        sales_history.append({'date': date, 'price': price})
    
    return {
        'title': title,
        'price': price,
        'description': description,
        'sales_history': sales_history
    }


def main():
    base_url = 'https://realty.yandex.ru/moskva/kupit/kvartira/'
    listing_links = get_listing_links(base_url)
    
    data = []
    for link in listing_links:
        listing_url = f'https://realty.yandex.ru{link}'
        listing_data = parse_listing(listing_url)
        data.append(listing_data)
        time.sleep(1)  
    

    df = pd.DataFrame(data)
    df.to_csv('moscow_apartments.csv', index=False)
    df.to_parquet('moscow_apartments.parquet', engine='pyarrow', index=False)

    print('Парсер отработал успешно!')

if __name__ == '__main__':
    main()

