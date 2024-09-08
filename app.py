from flask import Flask, request, jsonify, session
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
CORS(app, supports_credentials=True)

# Airtable API bilgileri
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

# Airtable API URL
AIRTABLE_API_URL = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

# Airtable'a veri gönder
def send_to_airtable(email, password, address, phone):
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "fields": {
            "Email": email,
            "Password": password,  # Şifreyi hash'lemeniz daha güvenli olabilir.
            "Address": address,
            "Phone": phone
        }
    }
    response = requests.post(AIRTABLE_API_URL, headers=headers, json=data)
    return response.json()

# Hesap oluşturma
@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not password or not address or not phone:
        return jsonify({"success": False, "message": "Tüm alanları doldurun!"})

    # Airtable'a veri gönder
    response = send_to_airtable(email, password, address, phone)

    # Airtable'dan gelen yanıtı kontrol et
    if response.get('error'):
        error_message = response['error'].get('message', 'Hata oluştu')
        if 'Duplicate' in error_message:
            return jsonify({"success": False, "message": "E-posta veya telefon ile başka hesap mevcut!"})
        else:
            return jsonify({"success": False, "message": error_message})

    return jsonify({"success": True, "message": "Hesap başarıyla oluşturuldu!"})

if __name__ == '__main__':
    app.run(debug=True)

