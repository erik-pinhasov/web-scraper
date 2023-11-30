import json
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from scrapers.scrape_ksp import get_ksp_items
from scrapers.scrape_ivory import get_ivory_items
from scrapers.scrape_bug import get_bug_items


WEBSITES = ['bug', 'ivory', 'ksp']
SCRAPE_FUNCTIONS = {
    'ksp': get_ksp_items,
    'ivory': get_ivory_items,
    'bug': get_bug_items,
}


def sort_dict(result_dict):
    keys = sorted(result_dict.keys(), key=lambda x: (float('inf') if 'TB' in x else float(x.split('GB')[0]), x))
    sorted_dict = {i: result_dict[i] for i in keys}
    return sorted_dict


def scrape(website, brand, model):
    try:
        products = json.loads(SCRAPE_FUNCTIONS[website](brand, model))
        return products
    except Exception:
        pass


def process_product(product, result_dict, website):
    storage = product.get('storage', 'N/A')
    ram = product.get('ram', 'N/A')
    price = product.get('price', 'N/A')
    url = product.get('url', 'N/A')

    key = f"{storage} + {ram}"
    result_dict[key][f'{website}_price'] = price
    result_dict[key][f'{website}_url'] = url


def store_results(brand, model, website, result_dict):
    products = scrape(website, brand, model)
    for product in products:
        process_product(product, result_dict, website)


def scrape_websites(brand, model):
    result_dict = defaultdict(lambda: {})

    with ThreadPoolExecutor() as executor:
        threads = [executor.submit(store_results, brand, model, website, result_dict) for website in WEBSITES]

        for thread in concurrent.futures.as_completed(threads):
            try:
                thread.result()
            except Exception:
                pass

    return sort_dict(result_dict)
