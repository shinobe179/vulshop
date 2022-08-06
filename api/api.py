import os

import pymysql
import uvicorn
from fastapi import FastAPI

app = FastAPI()

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASS = os.getenv('DB_PASS', '12345')
DB_NAME = os.getenv('DB_NAME', 'vulshop')


def connect_db():
    connection = pymysql.connect(host=DB_HOST,
                                user=DB_USER,
                                password=DB_PASS,
                                database=DB_NAME,
                                cursorclass=pymysql.cursors.DictCursor,
                                charset='utf8mb4')
    cursor = connection.cursor()
    return cursor


@app.get('/api/v1/products')
def list_products(q=''):
    query = 'SELECT id, name, price, stock FROM products '
    if q:
        query += f" WHERE (name LIKE '%{q}%' OR description LIKE '%{q}%') AND active = true;"
    else:
        query += 'WHERE active = true;'
    print(query)
    cursor.execute(query)
    products = cursor.fetchall()
    print(products)
    ret = {
        'response': {
            'products': products
        }
    }

    return ret


@app.get('/api/v1/product/{product_id}')
def product(product_id):
    query = f"SELECT id, name, price, description, stock FROM products WHERE id = {product_id};"
    cursor.execute(query)
    product = cursor.fetchone()
    ret = {
        'response': {
            'product': product
        }
    }

    return ret


@app.route('/purchase')
def purchase():
    pass


@app.route('/login')
def login():
    pass


def run():
    global cursor
    cursor = connect_db()

    uvicorn.run(app, host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    run()
