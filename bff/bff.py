import os

import requests
from flask import Flask, render_template, request
from requests.exceptions import ConnectionError

app = Flask(__name__)

API_HOST = os.getenv('API_HOST', '127.0.0.1')
API_PORT = os.getenv('API_PORT', '3001')
API_URL = f'http://{API_HOST}:{API_PORT}'


@app.route('/')
def index():
    return render_template('index.html', title='index')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/products')
def products():
    q = request.args.get('q', '')
    params = {'q': q}

    try:
        api_response = requests.get(API_URL + '/api/v1/products', params=params)
    except ConnectionError as e:
        return render_template('error.html', msg='API request is failed.')
    products = api_response.json()['response']['products']
    cnt = len(products)
    return render_template('products.html', products=products, cnt=cnt, q=q)


@app.route('/product/<product_id>')
def product(product_id):
    api_response = requests.get(API_URL + f'/api/v1/product/{product_id}')
    product = api_response.json()['response']['product']
    print(product)
    return render_template('product.html', product=product)


@app.route('/purchase')
def purchase():
    pass


@app.route('/login')
def login():
    pass


def error_handler(msg):
    return render_template('error.html', msg=msg)


def run():
    app.run(host='0.0.0.0', port=3000, debug=True, threaded=True)


if __name__ == '__main__':
    run()
