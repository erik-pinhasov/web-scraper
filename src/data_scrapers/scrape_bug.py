import urllib
from util.data_handler import scrape_url, pack_data, define_storage_ram, update_lowest_price
from util.text_formatter import extract_model_name, get_price_num
import json

BASE_URL = 'https://www.bug.co.il/'
SEARCH_URL = 'https://www.bug.co.il/search?key=&filter=,-2_12_108,&q='


def get_items_data(products, brand, model):
    lowest_prices = {}
    for product in products:
        name = product.select_one('span.c1').text.strip()
        ext_model = extract_model_name(brand, name)

        if model == ext_model:
            storage, ram = define_storage_ram(brand, model, name)
            price = get_price_num(product.select_one('span.c2 span').text)
            url = product['href']
            update_lowest_price(storage, ram, price, url, lowest_prices)

    return lowest_prices


def get_cheapest_items(products, brand, model):
    lowest_prices = get_items_data(products, brand, model)
    return [pack_data("bug", brand, model, storage.upper(), ram.upper(), price, BASE_URL + url) for
            (storage, ram), (price, url) in lowest_prices.items()]


def scrape_products(search):
    soup = scrape_url(SEARCH_URL, search)
    return soup.find_all('a', class_='bordered-product gray product-cube-inner-2 tpurl')


def get_bug_items(brand, model):
    items = scrape_products(f"'{brand} {model}'")
    products = get_cheapest_items(items, brand, model)
    return json.dumps(products, indent=4, ensure_ascii=False)
