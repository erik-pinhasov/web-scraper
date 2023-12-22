import urllib
import requests
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/109.0.0.0 Safari/537.36'


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


def requests_fetch(url):
    # Fetches and returns the HTML content of the specified URL using requests library (use for BUG and Ivory).
    response = session.get(url)
    content = response.content
    return get_soup(content)


def playwright_fetch(context, url):
    # Fetches and returns the HTML content of the specified URL using Playwright (use for KSP).
    page = context.new_page()
    page.goto(url)
    return get_soup(page.content())


def launch_playwright(pw):
    # Launches a Playwright browser
    browser = pw.chromium.launch()
    return browser, browser.new_context(user_agent=USER_AGENT)



session = requests.Session()
