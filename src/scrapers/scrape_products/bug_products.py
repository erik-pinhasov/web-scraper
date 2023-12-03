from util.data_handler import requests_fetch, pack_data, update_lowest_price, prepare_url
from util.text_formatter import format_model_name, get_price_num, define_storage_ram
import json

BASE_URL = 'https://www.bug.co.il/'
SEARCH_URL = 'https://www.bug.co.il/search?key=&filter=,-2_12_108,&q='


def get_items_data(products, brand, model):
    lowest_prices = {}
    for product in products:
        name = product.select_one('span.c1').text

        if model == format_model_name(brand, name):
            storage, ram = define_storage_ram(brand, model, name)
            price = get_price_num(product.select_one('span.c2 span').text)
            update_lowest_price(storage, ram, price, product['href'], lowest_prices)

    return lowest_prices


def get_cheapest_items(products, brand, model):
    lowest_prices = get_items_data(products, brand, model)
    return [pack_data("bug", brand, model, storage, ram, price, BASE_URL + url) for
            (storage, ram), (price, url) in lowest_prices.items()]


def scrape_products(search):
    url = prepare_url(SEARCH_URL, search)
    soup = requests_fetch(url)
    return soup.find_all('a', class_='bordered-product gray product-cube-inner-2 tpurl')


def get_bug_products(brand, model):
    items = scrape_products(f'{brand} {model}')
    return json.dumps(get_cheapest_items(items, brand, model), indent=4, ensure_ascii=False)
