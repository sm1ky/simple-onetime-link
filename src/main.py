from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid

web = Flask(__name__)

web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
web.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(web)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)

with web.app_context():
    db.create_all()

@web.route('/generate-token', methods=['POST'])
def generate_token():
    token_str = str(uuid.uuid4())
    redirect_domain = request.json.get('domain')
    base_url = request.json.get('url')

    if not base_url:
        return jsonify({'message': 'Base URL is required'}), 400

    one_time_url = f"{redirect_domain}/use-token/{token_str}"
    token = Token(token=token_str, url=base_url)
    
    db.session.add(token)
    db.session.commit()

    return jsonify({'token': token_str, 'url': one_time_url}), 201

@web.route('/use-token/<token>', methods=['GET'])
def use_token(token):
    token_entry = Token.query.filter_by(token=token).first()

    if not token_entry:
        return jsonify({'message': 'Invalid token'}), 404

    if token_entry.used:
        return jsonify({'message': 'Token already used'}), 400

    # Отметка токена как использованного
    token_entry.used = True
    db.session.commit()

    return redirect(token_entry.url, code=302)