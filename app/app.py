import base64
import hashlib
import logging
import os
import sys
from datetime import datetime, timedelta

import pymysql
from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASS = os.getenv('DB_PASS', '12345')
DB_NAME = os.getenv('DB_NAME', 'vulshop')

TITLE = 'VulShop'

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
handler = logging.StreamHandler(sys.stdout)
fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%dT%H:%M:%S")
handler.setFormatter(fmt)
logger.addHandler(handler)


def connect_db():
    """
    データベースへ接続してconnectionを得る。
    """
    connection = pymysql.connect(host=DB_HOST,
                                user=DB_USER,
                                password=DB_PASS,
                                database=DB_NAME,
                                cursorclass=pymysql.cursors.DictCursor)

    return connection


@app.route('/')
def index():
    session_user = get_user_info_from_session(request)
    return render_template('index.html', title=f'トップ | {TITLE}', session_user=session_user)


@app.route('/admin')
def admin():
    return render_template('admin.html', title=f'管理者ページ | {TITLE}')


@app.route('/products')
def products():
    session_user = get_user_info_from_session(request)
    q = request.args.get('q', '')

    query = 'SELECT id, name, price, stock FROM products '
    if q:
        query += f" WHERE name LIKE '%{q}%' AND active = true;"
    else:
        query += 'WHERE active = true;'

    logger.info(query)
    cursor = connection.cursor()
    cursor.execute(query)
    products = cursor.fetchall()
    cnt = len(products)

    return render_template('products.html', products=products, cnt=cnt, q=q, title=f'商品一覧 | {TITLE}', session_user=session_user)


@app.route('/product/<product_id>')
def product(product_id):
    query = f"SELECT id, name, price, description, stock FROM products WHERE id = {product_id};"
    cursor = connection.cursor()
    cursor.execute(query)
    product = cursor.fetchone()
    return render_template('product.html', product=product, title=f'product["name"] | {TITLE}')


@app.route('/purchase', methods=['POST'])
def purchase():
    pass
    #session_user = get_user_info_from_session(request)
    #session = session_user['session']
    #query = f"SELECT * FROM carts WHERE session = '{session}';"
    #cursor = connection.cursor()
    #cursor.execute(query)
    #products = cursor.fetchall()
    #for prd in products:
    #    product_id = prd['product_id']
    #    number = prd['number']
    #    query = f"SELECT * FROM products WHERE id = {product_id} AND stock < {number};"


@app.route('/signup', methods=['GET'])
def get_signup():
    session_user = get_user_info_from_session(request)
    logger.info(session_user)
    # ログイン済みの場合はトップへリダイレクト
    if session_user:
        return redirect('/')

    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def post_signup():
    session_user = get_user_info_from_session(request)
    # ログイン済みの場合はトップへリダイレクト
    if session_user:
        logger.info('User already signed in. Redirect to top.')
        return redirect('/')

    name = request.form['name']
    password_hash = hashlib.sha256(request.form['password'].encode()).hexdigest()
    logger.info(name, password_hash)
    query = f"INSERT INTO users (name, password_hash, active) VALUES ('{name}', '{password_hash}', true);"
    logger.info(query)
    cursor = connection.cursor()
    cursor.execute(query)
    result = connection.commit()
    logger.info(result)
    return render_template('signup-is-done.html')


@app.route('/signin', methods=['GET'])
def get_signin():
    session_user = get_user_info_from_session(request)
    # ログイン済みの場合はトップへリダイレクト
    if session_user:
        return redirect('/')

    return render_template('signin.html')


@app.route('/signin', methods=['POST'])
def post_signin():
    # ログイン済みの場合はトップへリダイレクト
    if get_user_info_from_session(request):
        return redirect('/')

    name = request.form['name']
    password_hash = hashlib.sha256(request.form['password'].encode()).hexdigest()
    query = f"SELECT id FROM users WHERE name = '{name}' AND password_hash = '{password_hash}';"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 1:
        user_id = result[0]['id']
        max_age = 60 * 60
        now = datetime.now()
        expires = now + timedelta(seconds=max_age)
        session = base64.b64encode((str(user_id) + '.' + str(now.timestamp())).encode()).decode()
        query = f"INSERT INTO sessions (user_id, session, created_at, expired_at, active) VALUES ('{user_id}', '{session}', '{now}', '{expires}', true);"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        response = make_response()
        response.set_cookie('session', value=session, max_age=max_age, expires=expires.timestamp())
        http_host = request.headers.get('host', None)
        logger.info(http_host)
        response.headers['location'] = f'http://{http_host}/'
        return response, 303
    else:
        return render_template('signin.html', error_message='ユーザーが存在しないか、パスワードが間違っています。')


@app.route('/signout')
def signout():
    session = request.cookies['session']
    query = f"UPDATE sessions SET active = false WHERE session = '{session}';"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return redirect('/')


@app.route('/cart', methods=['GET'])
def get_cart():
    session_user = get_user_info_from_session(request)
    logger.info(session_user)
    # 未ログインの場合はトップへリダイレクト
    if not session_user:
        return redirect('/')

    session = session_user['session']
    query = f"SELECT * FROM carts JOIN products ON carts.product_id = products.id WHERE session = '{session}';"
    cursor = connection.cursor()
    cursor.execute(query)
    products = cursor.fetchall()
    logger.info(products)
    total = 0
    for prd in products:
        total += prd['price'] * prd['number']
    logger.info('total: %s', total)
    return render_template('cart.html', products=products, session_user=session_user, total=total)


@app.route('/cart', methods=['POST'])
def post_cart():
    session_user = get_user_info_from_session(request)
    logger.info(session_user)
    # 未ログインの場合はトップへリダイレクト
    if not session_user:
        return redirect('/')

    product_id = request.form['product_id']
    number = request.form['number']
    session = session_user['session']
    query = f"""
    INSERT INTO
        carts (session, product_id, number)
    VALUES
        ('{session}', {product_id}, {number})
    ON DUPLICATE KEY UPDATE
        number = number+{number};
    """
    logger.info('query: %s', query)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

    return render_template('cart.html', session_user=session_user)




def get_user_info_from_session(request):
    """
    Cookieが設定されていて、かつexpired_atに達していなければ、該当するuser情報を返す。
    それ以外の場合はNoneを返す。
    """
    cookie = request.cookies.get('session', None)
    if cookie:
        now = int(datetime.now().timestamp())
        cursor = connection.cursor()
        query = f"SELECT user_id FROM sessions WHERE session = '{cookie}' AND expired_at > {now} AND active = true;"
        cursor.execute(query)
        session = cursor.fetchone()
        logger.info(session)
        if session:
                user_id = session['user_id']
                query = f"SELECT * FROM users WHERE id = '{user_id}';"
                cursor.execute(query)
                user_info = cursor.fetchone()
                user_info['session'] = cookie
                return user_info

    return None


def run():
    global connection
    connection = connect_db()

    app.run(host='0.0.0.0', port=3000, debug=True, threaded=True)


if __name__ == '__main__':
    run()
