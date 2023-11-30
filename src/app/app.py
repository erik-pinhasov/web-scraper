import json
from flask import Flask, render_template, jsonify, request
from scrapers.main_scraper import scrape_websites


def read_phones_file():
    with open('phones.json', 'r') as file:
        return json.load(file)


app = Flask(__name__)
phones_data = read_phones_file()
app.json.sort_keys = False


@app.route('/')
def index():
    return render_template('index.html', phones_data=phones_data)


@app.route('/get_models', methods=['GET'])
def get_models():
    brand = request.args.get('brand')
    models = phones_data.get(brand, [])
    return jsonify({'models': models})


@app.route('/get_comparison', methods=['GET'])
def get_comparison():
    brand = request.args.get('brand')
    model = request.args.get('model')
    result = scrape_websites(brand.lower(), model.lower())
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)


# TODO:
# 1. models update file
# 2. design
# 3. deploy
