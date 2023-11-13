from util.data_handler import get_playwright_page, pack_data, add_apple_ram
import json
from playwright.sync_api import sync_playwright

JSON_URL = 'https://ksp.co.il/m_action/api/category/'
WEB_URL = 'https://ksp.co.il/web/cat'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(HTML, like Gecko) Chrome/94.0.4606.71'


def get_filtered_url(json_data, storage, ram):
    storage_url = get_ksp_url(json_data, storage, '012066')
    ram_url = get_ksp_url(json_data, ram, '029')
    if ram_url:
        return f"{WEB_URL}/{storage_url}..{ram_url.split('.')[-1]}?sort=1"
    elif storage_url:
        return f"{WEB_URL}/{storage_url}?sort=1"
    else:
        return f"{WEB_URL}?sort=1"


def get_ksp_url(json_data, wanted, cat_id):
    tags = json_data.get('result', {}).get('filter', {}).get(cat_id, {}).get('tags', {})
    model = next((item for item in tags.values() if item.get('name').lower() == wanted.lower()), None)
    return model['action'] if model else None


def get_items(model_data, brand):
    items = model_data.get('result', {}).get('items', [])
    lowest_prices = {}

    for item in items:
        item_info = get_item_info(item, model_data, brand)
        key = (item_info['model'], item_info['storage'], item_info['ram'])
        lowest_prices[key] = min(lowest_prices.get(key, item_info), item_info, key=lambda x: x['price'])

    return list(lowest_prices.values())


def get_item_properties(tags):
    return [tags.get('דגם', ''), tags.get('נפח אחסון', ''), tags.get('גודל זכרון', '')]


def get_item_info(item, model_data, brand):
    tags = item.get('tags', {})
    model, storage, ram = get_item_properties(tags)
    price = item.get('price', '')
    url = get_filtered_url(model_data, storage, ram)
    if not ram and brand == 'apple':
        ram = add_apple_ram(brand, model)
    return pack_data("ksp", brand, model.lower(), storage, ram, price, url)


def get_json_data(context, url):
    soup = get_playwright_page(context, url)
    return json.loads(soup.find('pre').string)


def get_ksp_items(brand, model):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent=USER_AGENT)
        json_data = get_json_data(context, f'{JSON_URL}{"272..573"}')
        model_url = get_ksp_url(json_data, model, '02261')
        json_data = get_json_data(context, f'{JSON_URL}{model_url}')
        context.close()
        browser.close()
    return json.dumps(get_items(json_data, brand), indent=4, ensure_ascii=False)
