import json
from flask import Flask, render_template, jsonify, request
from playwright.sync_api import sync_playwright

from src.scrapers.compare_scraper import run_compare_scraper

PHONES_PATH = '../web_app/phones.json'


def read_phones_file():
    with open(PHONES_PATH, 'r') as file:
        return json.load(file)


app = Flask(__name__)
phones_data = read_phones_file()
app.json.sort_keys = False


@app.route('/')
def index():
    return render_template('index.html', phones_data=phones_data)


@app.route('/get_models', methods=['GET'])
def get_models():
    # Get phone models for selected brand.
    brand = request.args.get('brand')
    models = phones_data.get(brand, [])
    return jsonify({'models': models})


@app.route('/get_comparison', methods=['GET'])
def get_comparison():
    # Get phone comparison results for selected brand and model.
    brand = request.args.get('brand')
    model = request.args.get('model')

    try:
        result = run_compare_scraper(brand, model)
    except Exception as e:
        app.logger.error(f"Error occurred during scraping: {e}")
        result = {'error': 'Error occurred during scraping.'}

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
