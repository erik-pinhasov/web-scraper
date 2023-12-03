import json
from playwright.sync_api import sync_playwright
from scrapers.scrape_products.ksp_products import get_json_data
from util.data_handler import launch_playwright, close_playwright
from util.text_formatter import format_model_name

KSP_URL = 'https://ksp.co.il/m_action/api/'


def scrape_ksp(context, cat_id, url):
    json_data = get_json_data(context, f'{KSP_URL}category/{url}')
    return json_data.get('filter', {}).get(cat_id, {}).get('tags', {})


def scrape_brand_models(context, brand):
    brand_name = brand.get('name')
    brand_url = brand.get('action')

    models = scrape_ksp(context, '02261', brand_url)
    return [format_model_name(brand_name, model.get('name')) for model in models.values()]


def get_ksp_models():
    with sync_playwright() as pw:
        browser, context = launch_playwright(pw)
        result_data = {}

        brands = scrape_ksp(context, '021', "272..573")

        for brand in brands.values():
            brand_models = scrape_brand_models(context, brand)
            result_data[brand.get('name')] = brand_models

        close_playwright(browser, context)

    return result_data
