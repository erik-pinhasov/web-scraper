from util.data_handler import requests_fetch
from util.text_formatter import format_model_name

IVORY_URL = 'https://www.ivory.co.il/cellphones.html'


def extract_items_data(div, class_name):
    return [
        {'name': item.text.strip(), 'href': item['href']}
        for item in div.find_all('a', class_name)
    ]


def find_filter(filter_div, text):
    return next(
        (div for div in filter_div if div.find('h5', class_='catalog_sortBy_title') and
         div.find('h5', class_='catalog_sortBy_title').text.strip() == text), None
    )


def find_items(url, filter_name):
    soup = requests_fetch(url)
    filter_divs = soup.find_all('div', class_='col-12 filtercatalog')
    filter_div = find_filter(filter_divs, filter_name)

    return extract_items_data(filter_div, 'select-toggle-cut') if filter_div else (
        extract_items_data(soup, 'row product-anchor') if filter_name == "דגם סלולר" else []
    )


def find_constraints(result_dict):
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
    brands_data = find_items(IVORY_URL, 'מותג טלפון סלולרי')
    result_dict = {}

    for brand in brands_data:
        brand_name = brand['name']
        brand_models = find_items(brand['href'], "דגם סלולר")
        result_dict[brand_name] = [format_model_name(brand_name, model['name']) for model in brand_models]

    return find_constraints(result_dict)
