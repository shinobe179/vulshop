
import os

import pymysql
from flask import Flask, render_template, request

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASS = os.getenv('DB_PASS', '12345')
DB_NAME = os.getenv('DB_NAME', 'vulshop')


def connect_db():
    connection = pymysql.connect(host=DB_HOST,
                                    user=DB_USER,
                                    password=DB_PASS,
                                    database=DB_NAME,
                                    cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    return cursor


@app.route('/')
def index():
    return render_template('index.html', title='index')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/products')
def products():
    q = request.args.get('q', '')
    query = 'SELECT id, name, price, stock FROM products '
    if q:
        query += f" WHERE name LIKE '%{q}%' AND active = true;"
    else:
        query += 'WHERE active = true;'
    print(query)
    cursor.execute(query)
    products = cursor.fetchall()
    cnt = len(products)
    return render_template('products.html', products=products, cnt=cnt, q=q)


@app.route('/product/<product_id>')
def product(product_id):
    query = f"SELECT id, name, price, description, stock FROM products WHERE id = {product_id};"
    cursor.execute(query)
    product = cursor.fetchone()
    print(product)
    return render_template('product.html', product=product)


@app.route('/purchase')
def purchase():
    pass


@app.route('/login')
def login():
    pass


def run():
    global cursor
    cursor = connect_db()

    app.run(host='0.0.0.0', port=3000, debug=True, threaded=True)


if __name__ == '__main__':
    run()
