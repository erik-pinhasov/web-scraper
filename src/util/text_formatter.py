import re


def extract_english_text(text):
    words = re.findall(r'[a-zA-Z]+', text)
    return ' '.join(words).lower()


def separate_chars_numbers(text):
    pattern = r'(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])'
    separated_text = re.sub(pattern, ' ', text)
    return separated_text.strip()


def format_model_name(brand, model):
    model = remove_properties(model, [brand])
    if '+' in model:
        model = model.replace('+', ' ') + 'plus'
    return separate_chars_numbers(model)


def remove_properties(text, to_remove):
    special_chars = ['-', ':', '4g', '5g', 'ram']
    to_remove = [prop.lower() for prop in to_remove]
    to_remove.extend(special_chars)

    non_properties = text.lower().strip()
    for prop in to_remove:
        non_properties = non_properties.replace(prop, '').strip()

    return non_properties


def extract_model_name(brand, text):
    text = remove_properties(text, [brand])
    patterns = [r'\d+(?:tb|gb)?\+\d+(?:tb|gb)?', r'\b\d+(?:tb|gb)\b', r'[\u0590-\u05FF]+']
    for pattern in patterns:
        text = re.sub(pattern, '', text).strip()
    return text
