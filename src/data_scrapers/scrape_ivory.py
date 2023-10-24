from database.db_operations import fetch_data
from util.data_handler import fetch_and_parse, pack_data
import json


def get_cheapest(prices):
    all_prices = [int(price.text.replace(',', '')) for price in prices]
    return min(all_prices) if all_prices else None


def scrape_products(item):
    url = item.get("url")
    soup = fetch_and_parse(url, driver=None)
    prices = soup.select("span.price , span.print-actual-price")
    storage = item.get("storage").upper()
    ram = item.get("ram").upper()
    return pack_data("ivory", item.get("brand"), item.get("model"), storage, ram, get_cheapest(prices), url)


def get_ivory_items(brand, model):
    products = fetch_data("ivory", brand, model)
    scraped_data = []

    for item in products:
        item_data = scrape_products(item)
        scraped_data.append(item_data)

    return json.dumps(scraped_data, indent=4, ensure_ascii=False)