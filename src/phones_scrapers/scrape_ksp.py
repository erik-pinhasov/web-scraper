from util.data_handler import *
import json
from playwright.sync_api import sync_playwright
from util.text_formatter import add_apple_ram, format_model_name

JSON_URL = 'https://ksp.co.il/m_action/api/'
WEB_URL = 'https://ksp.co.il/web/cat'


def get_filtered_url(json_data, storage, ram):
    storage_url = get_ksp_url(json_data, None, storage, '012066')
    ram_url = get_ksp_url(json_data, None, ram, '029')

    if ram_url:
        return f"{WEB_URL}/{storage_url}..{ram_url.split('.')[-1]}?sort=1"
    elif storage_url:
        return f"{WEB_URL}/{storage_url}?sort=1"
    else:
        return f"{WEB_URL}?sort=1"


def compare_type(param, brand, model):
    if 'gb' in param:
        return param == model
    else:
        param = format_model_name(brand, param)
        return param == model


def get_ksp_url(json_data, brand, model, cat_id):
    tags = json_data.get('filter', {}).get(cat_id, {}).get('tags', {})
    model = next((item for item in tags.values() if compare_type(item.get('name').lower(), brand, model.lower())), None)
    return model['action'] if model else None


def check_discount(context, items):
    items_pids = ','.join(item['pid'] for item in items)
    items_prices = get_json_data(context, f'{JSON_URL}bms/{items_pids}')

    for item in items:
        discount = items_prices.get(item['pid'], {}).get('discount')
        item['price'] = discount.get('value') if discount else item['price']


def get_items(model_data, brand):
    items = model_data.get('items', [])
    lowest_prices = {}

    for item in items:
        model, storage, ram = get_item_properties(item.get('tags', {}), brand)
        pid = str(item.get('uin', ''))
        price = item.get('price', '')
        url = get_filtered_url(model_data, storage, ram)
        update_lowest_price(storage, ram, price, url, lowest_prices, pid)

    return [pack_data("ksp", brand, model, storage, ram, price, url, pid) for
            (storage, ram), (price, url, pid) in lowest_prices.items()]


def get_item_properties(tags, brand):
    model = tags.get('דגם', '')
    storage = tags.get('נפח אחסון', '')
    ram = tags.get('גודל זכרון', '')
    return [format_model_name(brand, model), storage if storage else None, ram if ram else add_apple_ram(brand, model)]


def get_json_data(context, url):
    soup = playwright_fetch(context, url)
    return json.loads(soup.find('pre').string).get('result', {})


def get_ksp_items(brand, model):
    with sync_playwright() as pw:
        browser, context = launch_playwright(pw)

        json_data = get_json_data(context, f'{JSON_URL}category/{"272..573"}')
        model_url = get_ksp_url(json_data, brand, model, '02261')

        json_data = get_json_data(context, f'{JSON_URL}category/{model_url}')
        products = get_items(json_data, brand)
        check_discount(context, products)

        close_playwright(browser, context)

    return json.dumps(products, indent=4, ensure_ascii=False)
