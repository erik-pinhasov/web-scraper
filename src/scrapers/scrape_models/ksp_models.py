from scrapers.scrape_products.ksp_products import get_json_data
from src.util.text_formatter import format_model_name

KSP_URL = 'https://ksp.co.il/m_action/api'


def scrape_ksp_url(cat_id, url):
    # Scrape KSP whole url page (getting json from API URL).
    json_data = get_json_data(f'{KSP_URL}/category/{url}')
    return json_data.get('filter', {}).get(cat_id, {}).get('tags', {})


def scrape_brand_models(brand):
    # Get models for a specific brand.
    brand_name = brand.get('name')
    brand_url = brand.get('action')

    brand_models = scrape_ksp_url('02261', brand_url)
    return [format_model_name(brand_name, model.get('name')) for model in brand_models.values()]


def get_ksp_models():
    # Get brands and models names from KSP website with Playwright browser scraper.
    result_data = {}

    brands = scrape_ksp_url('021', "272..573")
    for brand in brands.values():
        brand_models = scrape_brand_models(brand)
        result_data[brand.get('name')] = brand_models

    return result_data
