from util.data_handler import requests_fetch
from util.text_formatter import format_model_name

IVORY_URL = 'https://www.ivory.co.il/cellphones.html'
BRAND_FILTER = 'מותג טלפון סלולרי'
MODEL_FILTER = 'דגם סלולר'


def extract_items_data(div, class_name):
    # Extracts name and href (of brand/model) of items found in given div.
    return [{'name': item.text.strip(), 'href': item['href']} for item in div.find_all('a', class_name)]


def find_filter(filter_div, text):
    # Finds a filter section within the filter div (for brand/model).
    return next(
        (div for div in filter_div if (title := div.find('h5', class_='catalog_sortBy_title')) and
         title.text.strip() == text), None)


def get_filtered_items(url, filter_name):
    # Scrape URL, finds and extracts items names from a filter section.
    soup = requests_fetch(url)
    filter_divs = soup.find_all('div', class_='col-12 filtercatalog')
    filter_div = find_filter(filter_divs, filter_name)

    return extract_items_data(filter_div, 'select-toggle-cut') if filter_div else (
        extract_items_data(soup, 'row product-anchor') if filter_name == MODEL_FILTER else []
    )


def find_constraints(result_dict):
    # Apply specific constraints to the result dictionary in order to match results to ksp format.
    if 'EasyPhone' in result_dict:
        del result_dict['EasyPhone']

    if 'Samsung' in result_dict:
        result_dict['Samsung'] = [model for model in result_dict['Samsung'] if 'Z' not in model and 'A04E' not in model]

    if 'Poco' in result_dict and 'Xiaomi' in result_dict:
        result_dict['Xiaomi'].extend(['Poco ' + model for model in result_dict.pop('Poco')])

    if 'OPPO' in result_dict:
        result_dict['Oppo'] = [model.replace('Reno10', 'Reno 10') for model in result_dict['OPPO']]
        result_dict.pop('OPPO')

    if 'Nothing' in result_dict:
        result_dict['Nothing'] = [model.replace("NOTHING ", "").strip() for model in result_dict['Nothing']]

    if 'Phoneline' in result_dict and any('Fhoneline' in model for model in result_dict['Phoneline']):
        result_dict['Phoneline'] = [model.replace("Fhoneline", "").strip() for model in result_dict['Phoneline']]

    return result_dict


def get_ivory_models():
    # Get brands and models names from Ivory website.
    brands_data = get_filtered_items(IVORY_URL, BRAND_FILTER)
    result_dict = {}

    for brand in brands_data:
        brand_name = brand['name']
        brand_models = get_filtered_items(brand['href'], MODEL_FILTER)
        result_dict[brand_name] = [format_model_name(brand_name, model['name']) for model in brand_models]

    return find_constraints(result_dict)
