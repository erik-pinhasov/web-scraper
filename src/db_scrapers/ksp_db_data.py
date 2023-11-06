from util.data_handler import playwright_fetch
from util.text_formatter import format_model_name
from database.db_operations import add_brand, add_model, add_product
import json

JSON_URL = 'https://ksp.co.il/m_action/api/category'


def get_ksp_url(json_data, cat_id):
    tags = json_data.get('result', {}).get('filter', {}).get(cat_id, {}).get('tags', {})
    return [item for item in tags.values()]


def get_items(url, class_id):
    soup = playwright_fetch(url)
    json_data = json.loads(soup.find('pre').string)
    return get_ksp_url(json_data, class_id)


def update_brands():
    brands = get_items(f"{JSON_URL}/272..573", '021')
    for brand in brands:
        brand_name, brand_url = brand['name'], brand['action']
        add_brand(brand_name)
    return brands


def update_models(brand):
    if isinstance(brand, str):
        brands = get_items(f"{JSON_URL}/272..573", '021')
        brand = next((br for br in brands if br['name'].lower() == brand), None)

    brand_name = brand['name']
    models = get_items(f"{JSON_URL}/{brand['action']}", '02261')

    for model in models:
        model_name = format_model_name(brand_name, model['name'])
        model_url = f"{JSON_URL}/{model['action']}"
        add_model(brand_name, model_name)
        add_product(brand_name, model_url, "ksp", model_name)


def update_ksp_data():
    brands = update_brands()
    for brand in brands:
        update_models(brand)


if __name__ == "__main__":
    update_ksp_data()
