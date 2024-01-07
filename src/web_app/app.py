import json
from flask import Flask, render_template, jsonify, request
from scrapers.compare_scraper import run_compare_scraper
from scrapers.models_scraper import run_models_scraper
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
PHONES_PATH = os.path.join(current_directory, 'phones.json')


def read_phones_file():
    with open(PHONES_PATH, 'r') as file:
        return json.load(file)


def update_models_data():
    # Scrap for models names and store in phones_data, Used for brands and their models menu
    global phones_data
    # run_models_scraper()
    phones_data = read_phones_file()


app = Flask(__name__)
phones_data = None
update_models_data()
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
        result = {'error': 'An error occurred during scraping.'}

    return jsonify(result)


@app.route('/trigger_update', methods=['GET'])
def trigger_update():
    # Trigger to execute scraper for updating models.json
    update_models_data()
    return jsonify({'status': 'complete'})


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
