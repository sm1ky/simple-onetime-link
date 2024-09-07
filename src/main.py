from flask import Flask, request, jsonify, redirect, Response
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

web = Flask(__name__)

web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
web.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(web)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

with web.app_context():
    db.create_all()
    
@web.route('/', methods=['GET', 'POST'])
def global_answer():
    placeholder_text = """
    <html>
        <head>
            <title>Temporary Placeholder</title>
        </head>
        <body>
            <h1>Under Construction</h1>
            <p>This route is currently under development. Please come back later!</p>
        </body>
    </html>
    """
    return Response(placeholder_text, mimetype='text/html')

@web.route('/generate-token', methods=['POST'])
def generate_token():
    token_str = str(uuid.uuid4())
    redirect_domain = request.json.get('domain')
    base_url = request.json.get('url')

    if not base_url:
        return jsonify({'status': 400, 'message': 'Base URL is required'}), 400
    
    existing_token = Token.query.filter_by(url=base_url).first()
    if existing_token:
        return jsonify({
            'status': 409,
            'message': 'Token for this URL already exists', 
            'token': existing_token.token, 
            'url': f"{redirect_domain}/use-token/{existing_token.token}",
            'created_at': existing_token.created_at.isoformat()  
        }), 200

    one_time_url = f"{redirect_domain}/use-token/{token_str}"
    token = Token(token=token_str, url=base_url)

    db.session.add(token)
    db.session.commit()

    return jsonify({
        'status': 200,
        'token': token_str, 
        'url': one_time_url,
        'created_at': token.created_at.isoformat() 
    }), 201

@web.route('/use-token/<token>', methods=['GET'])
def use_token(token):
    token_entry = Token.query.filter_by(token=token).first()

    if not token_entry:
        return jsonify({
            'status': 404,
            'message': 'Invalid token',
            'details': f'Token {token} not found. Please check the URL or generate a new token.'
        }), 404

    if token_entry.used:
        return jsonify({
            'status': 400,
            'message': 'Token already used',
            'details': f'Token {token} has already been used at {token_entry.used_at}. It cannot be reused.',
            'created_at': token_entry.created_at.isoformat() 
        }), 400

    token_entry.used = True
    token_entry.used_at = datetime.now()
    db.session.commit()

    return redirect(token_entry.url, code=302)