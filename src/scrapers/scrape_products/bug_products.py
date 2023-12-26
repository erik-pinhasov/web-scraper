from util.data_handler import requests_fetch, pack_data, update_lowest_price, prepare_url, convert_to_json
from util.text_formatter import format_model_name, get_price_num, define_storage_ram


BASE_URL = 'https://www.bug.co.il/'
SEARCH_URL = 'https://www.bug.co.il/search?key=&filter=,-2_12_108,&q='


def get_items_data(products, brand, model):
    # Get the data for items matching the specified brand and model.
    lowest_prices = {}
    for product in products:
        name = product.select_one('span.c1').text
        if model.lower() == format_model_name(brand, name).lower():
            storage, ram = define_storage_ram(brand, model, name)
            price = get_price_num(product.select_one('span.c2 span').text)
            update_lowest_price(storage, ram, price, product['href'], lowest_prices)

    return lowest_prices


def get_cheapest_items(products, brand, model):
    # Get the cheapest items of the model for each storage version.
    lowest_prices = get_items_data(products, brand, model)
    return [pack_data("bug", brand, model, storage, ram, price, BASE_URL + url) for
            (storage, ram), (price, url) in lowest_prices.items()]


def scrape_products(search):
    # Scrape products from BUG website with search query.
    url = prepare_url(SEARCH_URL, search)
    soup = requests_fetch(url)
    return soup.find_all('a', class_='bordered-product gray product-cube-inner-2 tpurl')


def get_bug_products(brand, model):
    # Get product information for a model with all storages versions available from BUG website.
    try:
        model = model.replace("Fold5", "Fold 5").replace("Flip5", "Flip 5").replace("Reno7 Z", "Reno 7Z")
        items = scrape_products(f'{brand} {model}')
        if not items:
            return convert_to_json([])

        products = get_cheapest_items(items, brand, model)
        return convert_to_json(products)

    except Exception as e:
        print(f"Error in get_bug_products function: {str(e)}")
        return convert_to_json([])
