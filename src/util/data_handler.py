import re
import urllib
import requests
from bs4 import BeautifulSoup
from util.text_formatter import remove_properties


def define_storage_ram(brand, model, text):
    text = remove_properties(text, [brand, model])
    pattern = r'\d+(?:tb)?'
    matches = re.findall(pattern, text)
    if any('tb' in item for item in matches):
        storage = next((match for match in matches if 'tb' in match), None)
        ram = next((match + 'gb' for match in matches if 'tb' not in match
                    and int(match) <= 16), None)

    else:
        storage = next((match + 'gb' for match in matches if int(match) > 16), None)
        ram = next((match + 'gb' for match in matches if int(match) <= 16), None)
    if brand.lower() == 'apple':
        ram = add_apple_ram(brand, model)
    return storage, ram


def update_lowest_price(storage, ram, price, url, lowest_prices):
    if (storage, ram) not in lowest_prices or price < lowest_prices[(storage, ram)][0]:
        lowest_prices[(storage, ram)] = (price, url)


def add_apple_ram(brand, model):
    if brand.lower() != 'apple':
        return None
    if model.lower() in ['iphone 11', 'iphone 12', 'iphone 13', 'iphone 13 mini']:
        return '4GB'
    elif model.lower() in ['iphone 15 pro', 'iphone 15 pro max']:
        return '8GB'
    else:
        return '6GB'


def pack_data(website, brand, model, storage, ram, min_price, url):
    return {
        "website": website,
        "brand": brand,
        "model": model,
        "storage": storage,
        "ram": ram,
        "price": min_price,
        "url": url
    }


def get_soup(content):
    return BeautifulSoup(content, 'html.parser')


def scrape_url(url, param):
    encoded = urllib.parse.quote(param)
    url = f'{url}{encoded}'
    return requests_fetch(url)


def requests_fetch(url):
    response = requests.get(url)
    content = response.content
    return get_soup(content)


def get_playwright_page(context, url):
    page = context.new_page()
    page.goto(url)
    return get_soup(page.content())
