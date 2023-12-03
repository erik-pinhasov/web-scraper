import json
from concurrent.futures import ThreadPoolExecutor
from scrapers.scrape_models.ivory_models import get_ivory_models
from scrapers.scrape_models.ksp_models import get_ksp_models


def merge_dicts(dict1, dict2):
    result_dict = {brand: list(set(dict1.get(brand, []) + dict2.get(brand, []))) for brand in set(dict1) | set(dict2)}
    return result_dict


def export_json(result_data):
    with open('../app/phones.json', 'w') as json_file:
        json.dump(result_data, json_file, indent=2)


def run_models_scraper():
    try:
        print('running')
        with ThreadPoolExecutor() as executor:
            future_ivory = executor.submit(get_ivory_models)
            future_ksp = executor.submit(get_ksp_models)

            ivory_data, ksp_data = future_ivory.result(), future_ksp.result()

        merged_data = merge_dicts(ivory_data, ksp_data)
        export_json(merged_data)
        print('phones.json created successfully.')
    except Exception as e:
        print(f'Error during models scraper: {str(e)}')