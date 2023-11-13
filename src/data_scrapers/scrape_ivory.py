from util.data_handler import scrape_url, pack_data, update_lowest_price, add_apple_ram
from util.text_formatter import get_price_num
import json

SEARCH_URL = 'https://www.ivory.co.il/catalog.php?act=cat&cuts=2735&orderBy=priceLow&q='
COMP_URL = 'https://www.ivory.co.il/catalog_compare.php?ids='


def get_product_ids(soup):
    unique_prices = set()

    return ','.join([
        (unique_prices.add(price.get_text()), item.find('a', class_='row product-anchor')['data-product-id'])[1]
        for item in soup.find_all('div', class_='row p-1 entry-wrapper')
        if (price := item.select_one("span.price, span.print-actual-price")) and price.get_text() not in unique_prices
    ])


def get_comp_data(soup):
    return [soup.select('span.d-inline-block'), soup.select('div.description'), soup.select('div.table_row.id1227'),
            soup.select('div.table_row.id4388')]


def get_items_data(soup, brand, model):
    prices, urls, storages, rams = get_comp_data(soup)
    lowest_prices = {}

    for i in range(len(prices)):
        storage = storages[i].text.strip() if storages else None
        ram = rams[i].text.strip() if rams else add_apple_ram(brand, model)
        price = get_price_num(prices[i].text)
        url = urls[i].find('a').get('href')
        update_lowest_price(storage, ram, price, url, lowest_prices)

    return [pack_data("ivory", brand, model, storage, ram, price, url) for
            (storage, ram), (price, url) in lowest_prices.items()]


def get_ivory_items(brand, model):
    soup = scrape_url(SEARCH_URL, f"'{brand} {model}'")
    product_ids = get_product_ids(soup)
    soup = scrape_url(COMP_URL, product_ids)
    products = get_items_data(soup, brand, model)
    return json.dumps(products, indent=4, ensure_ascii=False)
