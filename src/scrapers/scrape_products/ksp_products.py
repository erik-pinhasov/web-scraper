import json
from playwright.sync_api import sync_playwright
from src.util.text_formatter import add_apple_ram, format_model_name
from src.util.data_handler import *

JSON_URL = 'https://ksp.co.il/m_action/api'
WEB_URL = 'https://ksp.co.il/web/cat'


def get_filtered_url(json_data, storage, ram):
    # Prepare URL of wanted model page (Regular website - not API)
    storage_url = get_ksp_url(json_data, None, storage, '012066')
    ram_url = get_ksp_url(json_data, None, ram, '029')

    if ram_url:
        return f"{WEB_URL}/{storage_url}..{ram_url.split('.')[-1]}?sort=1"
    elif storage_url:
        return f"{WEB_URL}/{storage_url}?sort=1"
    else:
        return None


def compare_type(param, brand, model):
    # Check for matching param (model name or storage/RAM).
    if any(unit in param.casefold() for unit in ['gb', 'tb']):
        return param == model
    else:
        param = format_model_name(brand, param)
        return param == model


def get_ksp_url(json_data, brand, param, cat_id):
    # Get the matching filtered URL for given param (model name or storage/RAM).
    # compare between item.name and param scraped (both of them: model name or storage/RAM)
    filtered_items = json_data.get('filter', {}).get(cat_id, {}).get('tags', {})
    try:
        model = next((item for item in filtered_items.values() if
                      compare_type(item.get('name'), brand, param)), None)
    except Exception as e:
        print(f"An error occurred: {e}")
        model = None
    return model['action'] if model else None


def check_discount(context, items):
    # Check for a discount - price appears in different URL.
    items_pids = ','.join(item['pid'] for item in items)
    items_prices = get_json_data(context, f'{JSON_URL}/bms/{items_pids}')

    for item in items:
        discount = items_prices.get(item['pid'], {}).get('discount')
        item['price'] = discount.get('value') if discount else item['price']


def get_product_items(model_data, brand, model_url):
    # Finds the cheapest item for each storage version of the model.
    items = model_data.get('items', [])
    lowest_prices = {}

    for item in items:
        model, storage, ram = get_item_properties(item.get('tags', {}), brand)
        pid = str(item.get('uin', ''))
        price = item.get('price', '')
        url = get_filtered_url(model_data, storage, ram) or model_url
        update_lowest_price(storage, ram, price, url, lowest_prices, pid)

    return [pack_data("ksp", brand, model, storage, ram, price, url, pid) for
            (storage, ram), (price, url, pid) in lowest_prices.items()]


def get_item_properties(tags, brand):
    # Get product properties and return formatted details.
    model = tags.get('דגם', '')
    storage = tags.get('נפח אחסון', '')
    ram = tags.get('גודל זכרון', '')

    storage = None if 'MB' in storage else storage
    ram = ram if ram else add_apple_ram(brand, model)
    return [format_model_name(brand, model), storage, ram]


def get_json_data(context, url):
    # Scrape KSP whole url page (getting json from it API url).
    soup = playwright_fetch(context, url)
    return json.loads(soup.find('pre').string).get('result', {})


def get_ksp_products(brand, model):
    # Get product information for a model with all storage versions available from the KSP website.
    try:
        with sync_playwright() as pw:
            browser, context = launch_playwright(pw)

            json_data = get_json_data(context, f'{JSON_URL}/category/{"272..573"}')
            model_id = get_ksp_url(json_data, brand, model, '02261')

            json_data = get_json_data(context, f'{JSON_URL}/category/{model_id}')
            products = get_product_items(json_data, brand, f'{WEB_URL}/{model_id}')
            check_discount(context, products)

        return json.dumps(products, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Error in get_ksp_products: {str(e)}")
        return json.dumps([], indent=4, ensure_ascii=False)
