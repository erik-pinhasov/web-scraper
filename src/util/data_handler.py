import urllib
import requests
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(HTML, like Gecko) Chrome/94.0.4606.71'


def update_lowest_price(storage, ram, price, url, lowest_prices, pid=None):
    key = (storage, ram)
    if pid and (key not in lowest_prices or price < lowest_prices[key][0]):
        lowest_prices[key] = (price, url, pid)
    elif not pid and (key not in lowest_prices or price < lowest_prices[key][0]):
        lowest_prices[key] = (price, url)


def pack_data(website, brand, model, storage, ram, min_price, url, pid=None):
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
    return BeautifulSoup(content, 'html.parser')


def prepare_url(url, param):
    param = param.replace(' ', '-')
    param = urllib.parse.quote(f'"{param}"')
    return f'{url}{param}'


def requests_fetch(url):
    response = requests.get(url)
    content = response.content
    return get_soup(content)


def playwright_fetch(context, url):
    page = context.new_page()
    page.goto(url)
    return get_soup(page.content())


def launch_playwright(pw):
    browser = pw.chromium.launch()
    return browser, browser.new_context(user_agent=USER_AGENT)


def close_playwright(browser, context):
    context.close()
    browser.close()
