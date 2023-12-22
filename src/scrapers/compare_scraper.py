import json
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from src.scrapers.scrape_products.ksp_products import get_ksp_products
from src.scrapers.scrape_products.ivory_products import get_ivory_products
from src.scrapers.scrape_products.bug_products import get_bug_products

WEBSITES = ['bug', 'ivory', 'ksp']
SCRAPE_FUNCTIONS = {
    'ksp': get_ksp_products,
    'ivory': get_ivory_products,
    'bug': get_bug_products,
}


def sort_product_dict(result_dict):
    # Sort the product dictionary based on storage and RAM ascending.
    try:
        keys = sorted(result_dict.keys(), key=lambda x: (float('inf') if 'TB' in x else float(x.split('GB')[0]), x))
        sorted_dict = {i: result_dict[i] for i in keys}
        return sorted_dict

    except Exception as e:
        print(f'Error in sort_product_dict function: {str(e)}')
        return result_dict


def scrape_website(website, brand, model, result_dict):
    # Scrape data from a website and store results of all websites in one dictionary.
    try:
        products = json.loads(SCRAPE_FUNCTIONS[website](brand, model))
        for product in products:
            process_product(product, result_dict, website)
    except Exception as e:
        print(f'Error during scraping from {website}: {str(e)}')


def process_product(product, result_dict, website):
    # Process product information and update the result dictionary with storage+RAM as keys (if exist).
    storage = product.get('storage')
    ram = product.get('ram')
    price = product.get('price')
    url = product.get('url')

    key = f"{storage} + {ram}"
    if storage is None and ram is None:
        key = "---"
    result_dict[key][f'{website}_price'] = price
    result_dict[key][f'{website}_url'] = url


def run_compare_scraper(brand, model):
    # Run the compare scraper for BUG, Ivory and KSP websites, with threads.
    result_dict = defaultdict(lambda: {})

    with ThreadPoolExecutor() as executor:
        threads = [executor.submit(scrape_website, website, brand, model, result_dict) for website in WEBSITES]

        for thread in concurrent.futures.as_completed(threads):
            try:
                thread.result()
            except Exception as e:
                print(f'Error during compare scraper: {str(e)}')

    return sort_product_dict(result_dict)
