from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Çevresel değişkenleri yükle
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
CORS(app, supports_credentials=True)

# Airtable API ayarları
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

# GitHub OAuth ayarları
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Airtable'a kayıt ekleme
@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.get_json()
    name = data.get('name')
    order = data.get('order')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')

    airtable_url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }
    record = {
        "fields": {
            "Name": name,
            "Order": order,
            "Email": email,
            "Phone": phone,
            "Address": address
        }
    }
    response = requests.post(airtable_url, json=record, headers=headers)
    return jsonify(response.json())

# Airtable'dan kayıtları alma
@app.route('/get_records', methods=['GET'])
def get_records():
    airtable_url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(airtable_url, headers=headers)
    return jsonify(response.json())

# GitHub OAuth login
@app.route('/login')
def login():
    return redirect(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={REDIRECT_URI}")

# GitHub OAuth callback
@app.route('/callback')
def callback():
    code = request.args.get('code')
    response = requests.post(
        'https://github.com/login/oauth/access_token',
        headers={'Accept': 'application/json'},
        data={
            'client_id': GITHUB_CLIENT_ID,
            'client_secret': GITHUB_CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
    )
    data = response.json()
    session['access_token'] = data.get('access_token')
    return redirect(url_for('profile'))

# GitHub profile
@app.route('/profile')
def profile():
    access_token = session.get('access_token')
    headers = {'Authorization': f'token {access_token}'}
    user_info = requests.get('https://api.github.com/user', headers=headers).json()
    return jsonify(user_info)

if __name__ == '__main__':
    app.run(debug=True)
