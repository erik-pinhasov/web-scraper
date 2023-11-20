import re


def get_price_num(text):
    return text.replace(',', '').replace('₪', '').strip()


def remove_properties(text, to_remove):
    special_chars = ['-', ':', ' 4g', ' 5g', 'ram']
    to_remove = [prop.lower() for prop in to_remove]
    to_remove.extend(special_chars)

    non_properties = text.lower().strip()
    for prop in to_remove:
        non_properties = non_properties.replace(prop, ' ').strip()

    return non_properties


def format_model_name(brand, model):
    model = remove_properties(model, [brand])
    patterns = [r'\d+(?:tb|gb)?\+\d+(?:tb|gb)?', r'\b\d+(?:tb|gb)\b', r'בצבע\s+(\b\w+\b)', r'[\u0590-\u05FF]+']
    for pattern in patterns:
        model = re.sub(pattern, '', model).strip()
    if '+' in model:
        model = model.replace('+', '') + ' plus'
    return model.strip()


def define_storage_ram(brand, model, text):
    text = remove_properties(text, [brand, model])
    pattern = r'\d+(?:\+\d+)?(?=(?:tb|gb))'
    matches = re.findall(pattern, text)
    if any('tb' in item for item in matches):
        storage = next((match for match in matches if 'tb' in match), None)
        ram = next((match + 'gb' for match in matches if 'tb' not in match
                    and int(match) <= 16), None)

    else:
        storage = next((match + 'gb' for match in matches if int(match) > 16), None)
        ram = next((match + 'gb' for match in matches if int(match) <= 16), None)
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
