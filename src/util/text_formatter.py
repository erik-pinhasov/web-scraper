import re

SPECIAL_CHARS = ['-', ':', ' 4g', ' 5g', 'ram', '4G', '5G', 'RAM', '‏']
PATTERNS = [r'\d+(?:TB|GB)?\+\d+(?:TB|GB)?', r'\b\d+(?:TB|GB)\b', r'בצבע\s+(.+)', r'\bsm \w+\s*', r'[\u0590-\u05FF]+',
            r'\d+W$', r'20[0-9]{2}$']


def get_price_num(text):
    return text.replace(',', '').replace('₪', '').strip()


def remove_properties(text, to_remove):
    to_remove = [prop for prop in to_remove]
    to_remove.extend(SPECIAL_CHARS)

    non_properties_text = text.strip()
    for prop in to_remove:
        non_properties_text = non_properties_text.replace(prop, ' ').strip()

    return non_properties_text


def remove_duplicates(model):
    seen_words = set()
    unique_words = []

    words = model.split()
    for word in reversed(words):
        word = word.strip()

        if word not in seen_words:
            seen_words.add(word)
            unique_words.append(word)

    return ' '.join(reversed(unique_words))


def format_model_name(brand, model):
    model = remove_properties(model, [brand])
    for pattern in PATTERNS:
        model = re.sub(pattern, '', model).strip()

    if '+' in model:
        model = model.replace('+', '') + ' Plus'

    model = remove_duplicates(model)
    return model.strip()


def define_storage_ram(brand, model, text):
    try:
        text = remove_properties(text, [brand, model])
        storage_and_ram_matches = find_storage_and_ram_matches(text)

        if not storage_and_ram_matches:
            return None, None

        storage_and_ram_matches = [
            match + 'GB' if re.match(r'\d+$', match) else match
            for match in storage_and_ram_matches
        ]

        storage, ram = extract_storage_and_ram(storage_and_ram_matches)
        if brand == 'Apple':
            ram = add_apple_ram(brand, model)
        return storage, ram

    except Exception as e:
        print(f"An error occurred in define_storage_ram: {e}")
        return None, None


def find_storage_and_ram_matches(text):
    pattern = r'(\d+(?:TB|GB)?|\d+\+\d+(?:TB|GB)?)'
    return re.findall(pattern, text)


def extract_storage_and_ram(matches):
    if any('TB' in item for item in matches):
        storage = next((match for match in matches if 'TB' in match), None)
        ram = next((match for match in matches if 'TB' not in match and int(match[:-2]) <= 16), None)
    else:
        storage = next((match for match in matches if int(match[:-2]) > 16), None)
        ram = next((match for match in matches if int(match[:-2]) <= 16), None)

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
