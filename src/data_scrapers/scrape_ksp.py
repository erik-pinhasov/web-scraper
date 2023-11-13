from database.db_operations import fetch_data
from util.data_handler import *
import json

WEB_URL = 'https://ksp.co.il/web/cat'


def get_filtered_url(json_data, storage, ram):
    storage_url = get_ksp_url(json_data, storage, '012066')
    ram_url = get_ksp_url(json_data, ram, '029')
    if ram_url:
        return f"{WEB_URL}/{storage_url}..{ram_url.split('.')[-1]}?sort=1"
    elif storage_url:
        return f"{WEB_URL}/{storage_url}?sort=1"
    else:
        return f"{WEB_URL}?sort=1"

def get_ksp_url(json_data, wanted_name, cat_id):
    tags = json_data.get('result', {}).get('filter', {}).get(cat_id, {}).get('tags', {})
    model = next((item for item in tags.values() if item.get('name') == wanted_name), None)
    return model['action'] if model else None


def get_items(model_data, brand):
    items = model_data.get('result', {}).get('items', [])
    lowest_prices = {}

    for item in items:
        item_info = get_item_info(item, model_data, brand)
        key = (item_info['model'], item_info['storage'], item_info['ram'])
        lowest_prices[key] = min(lowest_prices.get(key, item_info), item_info, key=lambda x: x['price'])

    return list(lowest_prices.values())


def get_item_info(item, model_data, brand):
    tags = item.get('tags', {})
    model = tags.get('דגם', '')
    storage = tags.get('נפח אחסון', '')
    ram = tags.get('גודל זכרון', '')
    price = item.get('price', '')
    url = get_filtered_url(model_data, storage, ram)
    if not ram and brand == 'apple':
        ram = add_apple_ram(brand, model)
    return pack_data("ksp", brand, model.lower(), storage, ram, price, url)


def get_ksp_items(brand, model):
    item_data = fetch_data("ksp", brand, model)
    soup = playwright_fetch(item_data[0]['url'])
    json_data = json.loads(soup.find('pre').string)

    return json.dumps(get_items(json_data, brand), indent=4, ensure_ascii=False)
