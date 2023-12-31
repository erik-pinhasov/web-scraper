import re

SPECIAL_CHARS = ['-', ':', 'ram', 'RAM', '‏', 'Dual', 'SIM']
PATTERNS = [r'\b\d+(?:\s*TB|\s*GB)?\s*\+\s*\d+(?:\s*TB|\s*GB)?\b', r'\b\d+(?:\s*TB|\s*GB)\b', r'\d+G', r'\b\d+/', r'\"',
            r"\'\'", r'\b\d+\.\d+\b', r'בצבע\s+(.+)', r'\bSM\s+(.+)\b', r'[\u0590-\u05FF]+', r'\d+W$', r'20[0-9]{2}$',
            r'\b(?:4G|5G)\b', r'\b(?:4g|5g)\b']


def extract_storage_text(text):
    # Extracts and returns the numerical storage capacity
    pattern = r'\b\d+(?:\.\d+)?(?:GB|TB)\b'
    match = re.search(pattern, text)

    if match:
        return match.group()


def get_price_num(text):
    # Extracts and returns the numerical price from the given text.
    return text.replace(',', '').replace('₪', '').strip()


def remove_properties(text, to_remove):
    # Removes specified properties from the given text.
    to_remove.extend(SPECIAL_CHARS)
    non_properties_text = text.strip()
    for prop in to_remove:
        non_properties_text = re.sub(re.escape(prop), ' ', non_properties_text, flags=re.IGNORECASE).strip()

    return non_properties_text


def remove_duplicates(model):
    # Removes duplicated words and chars from a given model.
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
    # Formats the model name by removing properties and patterns.
    # Formatting in purpose of making one structure for all websites products names.
    model = remove_properties(model, [brand])
    for pattern in PATTERNS:
        model = re.sub(pattern, '', model).strip()

    if '+' in model:
        model = model.replace('+', '') + ' Plus'

    model = remove_duplicates(model)
    return model.strip()


def define_storage_ram(brand, model, text):
    # Process text for getting storage and RAM information.
    try:
        text = remove_properties(text, [brand, model])
        for pattern in PATTERNS[4:]:  # Without 'TB' and 'GB' patterns
            text = re.sub(pattern, '', text).strip()
        matches = find_storage_and_ram(text)

        if not matches:
            return None, None

        storage_and_ram_matches = [
            match + 'GB' if re.match(r'\d+$', match) else match
            for match in matches
        ]

        storage, ram = extract_storage_and_ram(storage_and_ram_matches)
        if 'MB' in storage:
            storage = None
        if brand == 'Apple':
            ram = add_apple_ram(brand, model)
        return storage, ram

    except Exception as e:
        print(f"Error in define_storage_ram function: {e}")
        return None, None


def find_storage_and_ram(text):
    # Finds storage and RAM storage with regular expressions.
    pattern = r'(\d+(?:TB|GB)?|\d+\+\d+(?:TB|GB)?)'
    return re.findall(pattern, text)


def extract_storage_and_ram(matches):
    # Extracts storage and RAM information from the given text.
    if any('TB' in item for item in matches):
        storage = next((match for match in matches if 'TB' in match), None)
        ram = next((match for match in matches if 'TB' not in match and int(match[:-2]) <= 16), None)
    else:
        storage = next((match for match in matches if int(match[:-2]) > 16), None)
        ram = next((match for match in matches if int(match[:-2]) <= 16), None)

    return storage.upper() if storage else None, ram.upper() if ram else None


def add_apple_ram(brand, model):
    # Only for apple models - adds RAM manually
    if brand.lower() != 'apple':
        return None
    if model.lower() in ['iphone 11', 'iphone 12', 'iphone 13', 'iphone 13 mini']:
        return '4GB'
    elif model.lower() in ['iphone 15 pro', 'iphone 15 pro max']:
        return '8GB'
    else:
        return '6GB'
