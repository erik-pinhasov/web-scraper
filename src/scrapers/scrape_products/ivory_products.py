from util.data_handler import requests_fetch, pack_data, update_lowest_price, prepare_url, convert_to_json
from util.text_formatter import *
import json

SEARCH_URL = 'https://www.ivory.co.il/catalog.php?act=cat&cuts=2735&orderBy=priceLow&q='
COMP_URL = 'https://www.ivory.co.il/catalog_compare.php?ids='


def get_product_ids(soup, brand, model):
    # Scrape matching products url IDs - used in first scrape.
    unique_prices = {}

    for item in soup.find_all('a', class_='row product-anchor'):
        item_name = item.find('div', class_='col-md-12 col-12 title_product_catalog mb-md-1 main-text-area').text
        if model.lower() == format_model_name(brand, item_name).lower():
            price = item.select_one("span.price, span.print-actual-price").text
            unique_prices.setdefault(price, item['data-product-id'])

    return ','.join(unique_prices.values())


def get_item_properties(soup):
    # Get properties (name, price, storage, ram) of items from the given soup.
    return [soup.select('div.description'), soup.select('span.d-inline-block'),
            soup.select('div.table_row.id1227'), soup.select('div.table_row.id4388')]


def get_items_data(soup, brand, model):
    # Scrape data for items matching the specified brand and model - used in second scrape.
    names, prices, storages, rams = get_item_properties(soup)
    lowest_prices = {}

    for i in range(len(prices)):
        name = names[i].text.strip()
        storage = extract_storage_text(storages[i].text.strip()) if storages else None
        ram = extract_storage_text(rams[i].text.strip()) if rams else add_apple_ram(brand, model)
        try:
            if 'MB' in storage or 'MB' in ram:
                storage = ram = None
            else:
                storage, ram = define_storage_ram(brand, model, name) if storage is None and ram is None \
                                                                      else (storage, ram)
        except Exception as e:
            print(f"Error in get_items_data function (ivory_prods): {str(e)}")
            storage = ram = None
        price = get_price_num(prices[i].text)
        url = names[i].find('a').get('href')
        update_lowest_price(storage, ram, price, url, lowest_prices)

    return [pack_data("ivory", brand, model, storage, ram, price, url) for
            (storage, ram), (price, url) in lowest_prices.items()]


def get_ivory_products(brand, model):
    # Get product information for a model with all storage versions available from the Ivory website.
    try:
        model = model.replace("Fold5", "Fold 5").replace("Flip5", "Flip 5").replace("Reno 10", "Reno10")
        url = prepare_url(SEARCH_URL, f'{brand.replace("Xiaomi", "")} {model.replace("A2 Plus", "A2+")}')
        soup = requests_fetch(url)
        product_ids = get_product_ids(soup, brand, model)
        if not product_ids:
            return convert_to_json([])

        soup = requests_fetch(f'{COMP_URL}{product_ids}')
        products = get_items_data(soup, brand, model)
        return json.dumps(products, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Error in get_ivory_products function: {str(e)}")
        return convert_to_json([])
