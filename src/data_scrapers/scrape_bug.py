import urllib
from util.data_handler import fetch_and_parse, pack_data, define_storage_ram
from util.text_formatter import extract_model_name
import json

BASE_URL = 'https://www.bug.co.il/'


def update_lowest_price(storage, ram, product, lowest_prices):
    price = product.select_one('span.c2 span').text.replace(',', '').replace(' ₪', '').strip()
    url = product['href']

    if (storage, ram) not in lowest_prices or price < lowest_prices[(storage, ram)][0]:
        lowest_prices[(storage, ram)] = (price, url)


def find_products(products, brand, model):
    lowest_prices = {}
    for product in products:
        name = product.select_one('span.c1').text.strip()
        ext_model = extract_model_name(brand, name)

        if model == ext_model:
            storage, ram = define_storage_ram(brand, model, name)
            update_lowest_price(storage, ram, product, lowest_prices)

    return lowest_prices


def get_cheapest_items(products, brand, model):
    lowest_prices = find_products(products, brand, model)
    return [pack_data("bug", brand, model, storage.upper(), ram.upper(), price, BASE_URL + url) for
            (storage, ram), (price, url) in lowest_prices.items()]


def scrape_products(search):
    encoded_search = urllib.parse.quote(f"'{search}'")
    url = f'https://www.bug.co.il/search?&q={encoded_search}&key=&filter=,-2_12_108,'
    soup = fetch_and_parse(url, driver=None)
    return soup.find_all('a', class_='bordered-product gray product-cube-inner-2 tpurl')


def get_bug_items(brand, model):
    items = scrape_products(f"{brand} {model}")
    products = get_cheapest_items(items, brand, model)
    return json.dumps(products, indent=4, ensure_ascii=False)
