import json
from concurrent.futures import ThreadPoolExecutor
from scrapers.scrape_models.ivory_models import get_ivory_models
from scrapers.scrape_models.ksp_models import get_ksp_models


def merge_brand_models(dict1, dict2):
    # Merge two dictionaries: keys sorted descending by values size, values sorted alphabetic.
    merged_data = {brand: sorted(list(set(dict1.get(brand, []) + dict2.get(brand, []))))
                   for brand in set(dict1) | set(dict2)}
    return dict(sorted(merged_data.items(), key=lambda item: len(item[1]), reverse=True))


def export_to_json(data, filename):
    # Export data to a JSON file.
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)


def run_models_scraper():
    # Run the models scraper for Ivory and KSP in threads, merge the results, and export to JSON.
    try:
        with ThreadPoolExecutor() as executor:
            ivory_thread = executor.submit(get_ivory_models)
            ksp_thread = executor.submit(get_ksp_models)

            ivory_data, ksp_data = ivory_thread.result(), ksp_thread.result()

        merged_data = merge_brand_models(ivory_data, ksp_data)
        export_to_json(merged_data, '../app/phones.json')
        print('phones.json created successfully.')
    except Exception as e:
        print(f'Error during models scraper: {str(e)}')
