import sqlite3
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
DATABASE = 'database.db'
TOKENS = {}

PRODUCTS = [
    {
        'id': 1,
        'name': '练习生日记T恤',
        'price': 128,
        'image': 'https://via.placeholder.com/400x300?text=T-shirt',
        'member': 'A',
        'description': '暖心练习生日记主题印花T恤。'
    },
    {
        'id': 2,
        'name': '专属棒球帽',
        'price': 98,
        'image': 'https://via.placeholder.com/400x300?text=Cap',
        'member': 'B',
        'description': '青春活力棒球帽，代表色设计。'
    },
    {
        'id': 3,
        'name': '签名写真卡',
        'price': 45,
        'image': 'https://via.placeholder.com/400x300?text=Photo+Card',
        'member': 'C',
        'description': '限量练习生签名写真卡。'
    },
    {
        'id': 4,
        'name': '定制手机壳',
        'price': 88,
        'image': 'https://via.placeholder.com/400x300?text=Phone+Case',
        'member': 'D',
        'description': '多机型适配的练习生主题手机壳。'
    }
]


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                items TEXT,
                total REAL,
                created_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        ''')
    conn.close()


def authorize():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.split(' ', 1)[1]
    return TOKENS.get(token)


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    conn = get_db()
    try:
        with conn:
            conn.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': '用户名已存在'}), 400
    conn.close()
    return jsonify({'message': '注册成功'})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    conn.close()
    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': '用户名或密码错误'}), 401

    token = str(uuid.uuid4())
    TOKENS[token] = {'id': user['id'], 'username': user['username']}
    return jsonify({'token': token, 'username': user['username']})


@app.route('/api/products', methods=['GET'])
def products():
    return jsonify(PRODUCTS)


@app.route('/api/profile', methods=['GET'])
def profile():
    user = authorize()
    if not user:
        return jsonify({'error': '未授权'}), 401
    return jsonify({'username': user['username']})


@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    user = authorize()
    if not user:
        return jsonify({'error': '未授权'}), 401

    data = request.get_json() or {}
    items = data.get('items', [])
    total = data.get('total', 0)
    if not items or total <= 0:
        return jsonify({'error': '购物车不能为空'}), 400

    conn = get_db()
    with conn:
        conn.execute(
            'INSERT INTO orders (user_id, items, total, created_at) VALUES (?, ?, ?, ?)',
            (user['id'], str(items), total, datetime.utcnow().isoformat())
        )
    conn.close()
    return jsonify({'message': '订单已提交', 'order': {'items': items, 'total': total}})


@app.route('/api/orders', methods=['GET'])
def orders():
    user = authorize()
    if not user:
        return jsonify({'error': '未授权'}), 401

    conn = get_db()
    rows = conn.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC', (user['id'],)).fetchall()
    conn.close()
    result = [
        {'id': row['id'], 'items': row['items'], 'total': row['total'], 'created_at': row['created_at']}
        for row in rows
    ]
    return jsonify(result)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
