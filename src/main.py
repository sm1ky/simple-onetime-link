from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid
import string 
import random
from flask_cors import CORS

web = Flask(__name__)

web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
web.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(web)

db = SQLAlchemy(web)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)

with web.app_context():
    db.create_all()
    
def generate_random_token(length=6):
    characters = string.ascii_letters + string.digits  
    return ''.join(random.choice(characters) for _ in range(length))

@web.route('/generate-token', methods=['POST'])
def generate_token():
    redirect_domain = request.json.get('domain')
    base_url = request.json.get('url')

    if not base_url:
        return jsonify({'message': 'Base URL is required'}), 400

    # Проверка, существует ли уже токен для этого URL
    existing_token = Token.query.filter_by(url=base_url).first()
    if existing_token:
        one_time_url = f"{redirect_domain}/{existing_token.token}"
        return jsonify({'token': existing_token.token, 'url': one_time_url}), 200

    # Генерация уникального токена
    token_str = generate_random_token()

    # Проверка существования токена
    while Token.query.filter_by(token=token_str).first() is not None:
        token_str = generate_random_token()

    one_time_url = f"{redirect_domain}/{token_str}"

    # Создание нового токена
    token = Token(token=token_str, url=base_url)
    db.session.add(token)
    db.session.commit()

    return jsonify({'token': token_str, 'url': one_time_url}), 201

@web.route('/<token>', methods=['GET'])
def use_token(token):
    token_entry = Token.query.filter_by(token=token).first()

    if not token_entry:
        return jsonify({'message': 'Invalid token'}), 404

    if not token_entry.used:
        token_entry.used = True
        db.session.commit()

    return redirect(token_entry.url, code=302)