from util.data_handler import requests_fetch
from util.text_formatter import format_model_name

IVORY_URL = 'https://www.ivory.co.il/cellphones.html'
BRAND_FILTER = 'מותג טלפון סלולרי'
MODEL_FILTER = 'דגם סלולר'

def extract_items_data(div, class_name):
    """
    Extracts data from the given HTML div based on the specified class name.

    Args:
        div (soup element): HTML div element.
        class_name (str): Class name to filter elements.

    Returns:
        list: List of dictionaries containing 'name' and 'href' for each item.
    """
    return [{'name': item.text.strip(), 'href': item['href']} for item in div.find_all('a', class_name)]

def find_filter(filter_div, text):
    """
    Finds a specific filter within the filter div.

    Args:
        filter_div (list): List of HTML div elements containing filters.
        text (str): Text to match for the filter.

    Returns:
        soup element or None: Matching filter div or None if not found.
    """
    return next(
        (div for div in filter_div if (title := div.find('h5', class_='catalog_sortBy_title')) and
         title.text.strip() == text), None)


def find_items(url, filter_name):
    """
    Finds items based on the given URL and filter name.

    Args:
        url (str): URL to scrape.
        filter_name (str): Name of the filter.

    Returns:
        list: List of dictionaries containing 'name' and 'href' for each item.
    """
    soup = requests_fetch(url)
    filter_divs = soup.find_all('div', class_='col-12 filtercatalog')
    filter_div = find_filter(filter_divs, filter_name)

    return extract_items_data(filter_div, 'select-toggle-cut') if filter_div else (
        extract_items_data(soup, 'row product-anchor') if filter_name == MODEL_FILTER else []
    )

def find_constraints(result_dict):
    """
    Apply specific constraints to the result dictionary.

    Args:
        result_dict (dict): Dictionary containing brands and their models.

    Returns:
        dict: Result dictionary with applied constraints.
    """
    if 'EasyPhone' in result_dict:
        del result_dict['EasyPhone']

    if 'Samsung' in result_dict:
        result_dict['Samsung'] = [model for model in result_dict['Samsung'] if 'Z' not in model]

    if 'Poco' in result_dict and 'Xiaomi' in result_dict:
        result_dict['Xiaomi'].extend(['Poco ' + model for model in result_dict.pop('Poco')])

    if 'OPPO' in result_dict:
        result_dict['Oppo'] = result_dict.pop('OPPO')

    return result_dict

def get_ivory_models():
    """
    Retrieves brands and models names from Ivory website.

    Returns:
        dict: Dictionary containing brands (key) and models (values).
    """
    brands_data = find_items(IVORY_URL, BRAND_FILTER)
    result_dict = {}

    for brand in brands_data:
        brand_name = brand['name']
        brand_models = find_items(brand['href'], MODEL_FILTER)
        result_dict[brand_name] = [format_model_name(brand_name, model['name']) for model in brand_models]

    return find_constraints(result_dict)
