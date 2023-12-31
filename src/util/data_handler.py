import time
import urllib
import requests
import json
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


def update_lowest_price(storage, ram, price, url, lowest_prices, pid=None):
    # Updates the lowest price products for a specific storage and RAM combination.
    key = (storage, ram)
    if pid and (key not in lowest_prices or price < lowest_prices[key][0]):
        lowest_prices[key] = (price, url, pid)
    elif not pid and (key not in lowest_prices or price < lowest_prices[key][0]):
        lowest_prices[key] = (price, url)


def pack_data(website, brand, model, storage, ram, min_price, url, pid=None):
    # Packs product information into a dictionary.
    return {
        "website": website,
        "brand": brand,
        "model": model,
        "storage": storage,
        "ram": ram,
        "price": min_price,
        "url": url,
        "pid": pid if pid else None
    }


def get_soup(content):
    # BeautifulSoup page parser
    return BeautifulSoup(content, 'html.parser')


def convert_to_json(data):
    return json.dumps(data, indent=4, ensure_ascii=False)


def prepare_url(url, param):
    # Prepares a URL by encoding the search parameter.
    param = param.replace(' ', '-')
    param = urllib.parse.quote(f'"{param}-"')
    return f'{url}{param}'


# def requests_fetch(url):
#     # Fetches and returns the HTML content of the specified URL using requests library (use for BUG and Ivory).
#     response = session.get(url, headers={'User-Agent': USER_AGENT})
#     content = response.content
#     return get_soup(content)


def requests_fetch(url, max_attempts=2, delay=2):
    # Fetches and returns the HTML content of the specified URL using requests library
    # Waits for a delay between attempts to allow the page to load.

    for _ in range(max_attempts):
        response = session.get(url, headers={'User-Agent': USER_AGENT})
        content = response.content

        if '403' not in str(response.status_code):
            return get_soup(content)

        time.sleep(delay)
    return None


session = requests.Session()
