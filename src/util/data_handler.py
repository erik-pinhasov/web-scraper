import re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from util.text_formatter import remove_properties


def define_storage_ram(brand, model, text):
    text = remove_properties(text, [brand, model])
    pattern = r'\d+(?:tb)?'
    matches = re.findall(pattern, text)
    if any('tb' in item for item in matches):
        storage = next((match for match in matches if 'tb' in match), None)
        ram = next((match+'gb' for match in matches if 'tb' not in match
                    and int(match) <= 16), None)

    else:
        storage = next((match+'gb' for match in matches if int(match) > 16), None)
        ram = next((match+'gb' for match in matches if int(match) <= 16), None)
    if brand.lower() == 'apple':
        ram = add_apple_ram(model)
    return storage, ram


def add_apple_ram(model_name):
    if model_name.lower() in ['iPhone 11', 'iPhone 12', 'iPhone 13', 'iPhone 13 mini']:
        return '4gb'
    elif model_name.lower() in ['iphone 15 pro', 'iphone 15 pro max']:
        return '8gb'
    else:
        return '6gb'


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


def fetch_and_parse(url, driver=None):
    if driver:
        driver.get(url)
        content = driver.page_source
    else:
        response = requests.get(url)
        content = response.content

    soup = BeautifulSoup(content, 'html.parser')
    return soup


def init_chrome():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={user_agent}")
    return webdriver.Chrome(options=chrome_options)