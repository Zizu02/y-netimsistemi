from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# CORS ayarları
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://sapphire-algae-9ajt.squarespace.com"}})

# Airtable API bilgileri
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

# Airtable API URL
AIRTABLE_API_URL = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

# Kök rotası
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API is live and working!"})

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

    if not email:
        return jsonify({"success": False, "message": "E-posta sağlanmalı!"})
    if not password:
        return jsonify({"success": False, "message": "Şifre sağlanmalı!"})
    if not address:
        return jsonify({"success": False, "message": "Adres sağlanmalı!"})
    if not phone:
        return jsonify({"success": False, "message": "Telefon numarası sağlanmalı!"})

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

# Kullanıcı bilgilerini getiren endpoint
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    email = request.args.get('email')
    
    if not email:
        return jsonify({"success": False, "message": "E-posta sağlanmalı!"})

    # Airtable'dan kullanıcı bilgilerini al
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(AIRTABLE_API_URL + f"?filterByFormula={{Email}}='{email}'", headers=headers)
    data = response.json()

    # Eğer kullanıcı mevcutsa döndür
    if data.get('records'):
        user_info = data['records'][0]['fields']
        return jsonify({"success": True, "user_info": user_info})
    else:
        return jsonify({"success": False, "message": "Kullanıcı bulunamadı."})

if __name__ == '__main__':
    app.run(debug=True)

