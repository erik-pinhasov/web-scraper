import json
from scrapers.scrape_models.ivory_models import get_ivory_models
from scrapers.scrape_models.ksp_models import get_ksp_models

PHONES_PATH = '../web_app/phones.json'


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
        ksp_models = get_ksp_models()
        ivory_models = get_ivory_models()
        merged_data = merge_brand_models(ksp_models, ivory_models)
        export_to_json(merged_data, PHONES_PATH)
        print('phones.json created successfully.')
    except Exception as e:
        print(f'Error during models scraper: {str(e)}')
