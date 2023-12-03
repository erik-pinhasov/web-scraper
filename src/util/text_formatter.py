import re


def get_price_num(text):
    return text.replace(',', '').replace('₪', '').strip()


def remove_properties(text, to_remove):
    special_chars = ['-', ':', ' 4g', ' 5g', 'ram', '4G', '5G', 'RAM', '‏']
    to_remove = [prop for prop in to_remove]
    to_remove.extend(special_chars)

    non_properties = text.strip()
    for prop in to_remove:
        non_properties = non_properties.replace(prop, ' ').strip()

    return non_properties


def format_model_name(brand, model):
    model = remove_properties(model, [brand])
    patterns = [
        r'\d+(?:TB|GB)?\+\d+(?:TB|GB)?',
        r'\b\d+(?:TB|GB)\b',
        r'בצבע\s+(.+)',
        r'\bsm \w+\s*',
        r'[\u0590-\u05FF]+',
        r'\d+W$',
        r'20[0-9]{2}$'
    ]
    for pattern in patterns:
        model = re.sub(pattern, '', model).strip()
    if '+' in model:
        model = model.replace('+', '') + ' Plus'
    return model.strip()


def define_storage_ram(brand, model, text):
    text = remove_properties(text, [brand, model])
    pattern = r'(\d+(?:\+\d+)?(?:TB|GB))'
    matches = re.findall(pattern, text)
    if any('TB' in item for item in matches):
        storage = next((match for match in matches if 'TB' in match), None)
        ram = next((match for match in matches if 'TB' not in match and int(match[:-2]) <= 16), None)

    else:
        storage = next((match for match in matches if int(match[:-2]) > 16), None)
        ram = next((match for match in matches if int(match[:-2]) <= 16), None)
    if brand.lower() == 'apple':
        ram = add_apple_ram(brand, model)
    return storage.upper() if storage else None, ram.upper() if ram else None


def add_apple_ram(brand, model):
    if brand.lower() != 'apple':
        return None
    if model.lower() in ['iphone 11', 'iphone 12', 'iphone 13', 'iphone 13 mini']:
        return '4GB'
    elif model.lower() in ['iphone 15 pro', 'iphone 15 pro max']:
        return '8GB'
    else:
        return '6GB'

