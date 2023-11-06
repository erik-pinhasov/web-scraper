import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
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
        ram = add_apple_ram(model)
    return storage, ram


def add_apple_ram(model_name):
    if model_name.lower() in ['iphone 11', 'iphone 12', 'iphone 13', 'iphone 13 mini']:
        return '4GB'
    elif model_name.lower() in ['iphone 15 pro', 'iphone 15 pro max']:
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


def requests_fetch(url):
    response = requests.get(url)
    content = response.content
    return get_soup(content)


def playwright_fetch(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                                 ' (KHTML, like Gecko) Chrome/94.0.4606.71"')
        page = context.new_page()
        page.goto(url)
        content = page.content()

        context.close()
        browser.close()

    return get_soup(content)
