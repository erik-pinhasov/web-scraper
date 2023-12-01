import json
from playwright.sync_api import sync_playwright
from scrapers.scrape_ksp import get_json_data
from util.data_handler import launch_playwright, close_playwright
from util.text_formatter import format_model_name

KSP_URL = 'https://ksp.co.il/m_action/api/'


def scrape_ksp(context, cat_id, url):
    json_data = get_json_data(context, f'{KSP_URL}category/{url}')
    return json_data.get('filter', {}).get(cat_id, {}).get('tags', {})

def get_ksp_items():
    with sync_playwright() as pw:
        browser, context = launch_playwright(pw)
        result_data = {}

        brands = scrape_ksp(context, '021', "272..573")
        for brand in brands.values():
            brand_name = brand.get('name')
            brand_url = brand.get('action')

            models = scrape_ksp(context, '02261', brand_url)
            brand_models = [format_model_name(brand_name, model.get('name')) for model in models.values()]

            result_data[brand_name] = brand_models

        close_playwright(browser, context)

        with open('../app/phones.json', 'w') as json_file:
            json.dump(result_data, json_file, indent=2)

#TODO: add ivory scrape