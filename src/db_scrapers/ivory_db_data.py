from database.db_operations import add_brand, add_model, add_product
from util.text_formatter import format_model_name, extract_english_text
from util.data_handler import fetch_and_parse, add_apple_ram

IVORY_URL = 'https://www.ivory.co.il/cellphones.html'

def extract_items_data(div, class_name):
    items = div.find_all('a', class_name)
    items_data = []

    for item in items:
        item_data = {
            'name': item.text.strip(),
            'href': item['href'],
        }
        items_data.append(item_data)
    return items_data


def find_items(url, filter_name):
    soup = fetch_and_parse(url, driver=None)
    filter_divs = soup.find_all('div', class_='col-12 filtercatalog')
    filter_div = find_filter(filter_divs, filter_name)

    if filter_div:
        return extract_items_data(filter_div, 'select-toggle-cut')
    elif filter_name == "דגם סלולר":
        return handle_model_missing(soup)
    else:
        return []


def find_filter(filter_div, text):
    for div in filter_div:
        filter_name = div.find('h5', class_='catalog_sortBy_title')
        if filter_name and filter_name.text.strip() == text:
            return div
    return None


def scrape_ivory_data():
    brands_data = find_items(IVORY_URL, 'מותג טלפון סלולרי')

    for brand in brands_data:
        brand['models'] = find_items(brand['href'], "דגם סלולר")

        for model in brand['models']:
            model['storages'] = find_items(model['href'], "נפח כולל")

            for storage in model['storages']:
                storage['ram'] = find_items(storage['href'], "זכרון RAM סלולר")

    return brands_data


def handle_model_missing(soup):
    product_class = 'row product-anchor'
    products_models = extract_items_data(soup, product_class)
    for model in products_models:
        model['name'] = extract_english_text(model['name'])
    return products_models


def update_ivory_data():
    brands_data = scrape_ivory_data()

    for brand in brands_data:
        brand_name = brand['name']
        if brand_name == 'Poco':
            brand_name = 'xiaomi'
        add_brand(brand_name)

        for model in brand['models']:
            update_ivory_brand_models(brand_name, model)


def update_ivory_brand_models(brand_name, model):
    model_storage = None
    model_ram = None
    model_name = format_model_name(brand_name, model['name'])
    model_url = model['href']

    if model['storages']:
        for storage in model['storages']:
            update_ivory_storage(brand_name, model_name, storage, model_ram)
    else:
        add_ivory_data(brand_name, model_name, model_storage, model_ram, model_url)


def update_ivory_storage(brand, model, storage, ram):
    storage_name = storage['name']
    if brand.lower() == 'apple':
        ram = add_apple_ram(model)
    if storage['ram']:
        for ram in storage['ram']:
            add_ivory_data(brand, model, storage_name, ram['name'], ram['href'])
    else:
        add_ivory_data(brand, model, storage_name, ram, storage['href'])


def add_ivory_data(brand_name, model_name, model_storage, model_ram, model_url):
    add_model(brand_name, model_name)
    add_product(brand_name, model_url, "ivory", model_name, model_storage, model_ram)


if __name__ == "__main__":
    update_ivory_data()
