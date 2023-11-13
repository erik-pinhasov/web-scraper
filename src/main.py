import threading
import json
import time

from data_scrapers.scrape_ksp import get_ksp_items
from data_scrapers.scrape_ivory import get_ivory_items
from data_scrapers.scrape_bug import get_bug_items
from pandas import DataFrame


def scrape_and_store(brand, model, result_dict, website):
    is_ksp = (website == 'ksp')
    is_ivory = (website == 'ivory')
    is_bug = (website == 'bug')
    try:
        if is_ksp:
            products = json.loads(get_ksp_items(brand, model))
        elif is_ivory:
            products = json.loads(get_ivory_items(brand, model))
        elif is_bug:
            products = json.loads(get_bug_items(brand, model))
        for product in products:
            storage = product.get('storage', 'N/A')
            ram = product.get('ram', 'N/A')
            price = product.get('price', 'N/A')
            url = product.get('url', 'N/A')

            key = f"{storage} + {ram}"
            if key not in result_dict:
                result_dict[key] = {'ksp_link': 'N/A', 'ivory_link': 'N/A', 'bug_link': 'N/A'}
            if (is_ksp or is_ivory or is_bug) and key in result_dict:
                result_dict[key][f'{website}_link'] = f"{price}#{url}"
    except Exception:
        pass


def make_clickable_both(val):
    if val == "N/A":
        return val
    else:
        price, url = val.split('#')
        return f'<a href="{url}">{price}</a>'


def main(brand, model, websites):
    result_dict = {}

    def run_threads():
        threads = []

        for website in websites:
            thread = threading.Thread(target=scrape_and_store, args=(brand, model, result_dict, website))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    run_threads()

    data = []
    for key, values in result_dict.items():
        ksp_link = values['ksp_link']
        ivory_link = values['ivory_link']
        bug_link = values['bug_link']
        data.append([f'{key}', f'{ksp_link}', f'{ivory_link}', f'{bug_link}'])
    df = DataFrame(data, columns=['Storage + RAM', 'KSP Price', 'Ivory Price', 'BUG Price'])

    df['KSP Price'] = df['KSP Price'].apply(make_clickable_both)
    df['Ivory Price'] = df['Ivory Price'].apply(make_clickable_both)
    df['BUG Price'] = df['BUG Price'].apply(make_clickable_both)

    html_table = df.to_html(escape=False, classes='table table-striped')

    with open('results.html', 'w') as file:
        file.write(html_table)


if __name__ == "__main__":
    start = time.time()
    brand = 'samsung'
    model = 'galaxy s23 ultra'

    websites_to_scrape = ['bug', 'ivory', 'ksp']

    main(brand, model, websites_to_scrape)
    end = time.time()
    print(end - start)
