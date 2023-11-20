from util.data_handler import requests_fetch, pack_data, update_lowest_price, prepare_url
from util.text_formatter import get_price_num, add_apple_ram, format_model_name, define_storage_ram
import json

SEARCH_URL = 'https://www.ivory.co.il/catalog.php?act=cat&cuts=2735&orderBy=priceLow&q='
COMP_URL = 'https://www.ivory.co.il/catalog_compare.php?ids='


def get_product_ids(soup, brand, model):
    unique_prices = {}

    for item in soup.find_all('a', class_='row product-anchor'):
        item_name = item.find('div', class_='col-md-12 col-12 title_product_catalog mb-md-1 main-text-area').text
        if model == format_model_name(brand, item_name):
            price = item.select_one("span.price, span.print-actual-price").text
            unique_prices.setdefault(price, item['data-product-id'])

    return ','.join(unique_prices.values())


def get_item_properties(soup):
    return [soup.select('div.description'), soup.select('span.d-inline-block'),
            soup.select('div.table_row.id1227'), soup.select('div.table_row.id4388')]


def get_items_data(soup, brand, model):
    names, prices, storages, rams = get_item_properties(soup)
    lowest_prices = {}

    for i in range(len(prices)):
        name = names[i].text.strip()
        storage = storages[i].text.strip() if storages else None
        ram = rams[i].text.strip() if rams else add_apple_ram(brand, model)
        storage, ram = define_storage_ram(brand, model, name) if storage is None and ram is None else (storage, ram)
        price = get_price_num(prices[i].text)
        url = names[i].find('a').get('href')
        update_lowest_price(storage, ram, price, url, lowest_prices)

    return [pack_data("ivory", brand, model, storage, ram, price, url) for
            (storage, ram), (price, url) in lowest_prices.items()]


def get_ivory_items(brand, model):
    url = prepare_url(SEARCH_URL, f'{brand.replace("xiaomi", "")} {model.replace("plus", "")}')
    soup = requests_fetch(url)
    product_ids = get_product_ids(soup, brand, model)

    soup = requests_fetch(f'{COMP_URL}{product_ids}')
    products = get_items_data(soup, brand, model)
    return json.dumps(products, indent=4, ensure_ascii=False)
