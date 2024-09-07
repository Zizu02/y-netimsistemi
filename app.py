from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Veritabanı simülasyonu
users = []

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not password or not address or not phone:
        return jsonify({"success": False, "message": "Tüm alanları doldurun!"})

    # E-posta ve telefon numarası kontrolü
    for user in users:
        if user['email'] == email:
            return jsonify({"success": False, "message": "Bu e-posta adresi ile zaten bir hesap mevcut!"})
        if user['phone'] == phone:
            return jsonify({"success": False, "message": "Bu telefon numarası ile zaten bir hesap mevcut!"})

    # Kullanıcıyı ekle
    users.append({
        "email": email,
        "password": password,
        "address": address,
        "phone": phone
    })
    
    return jsonify({"success": True, "message": "Hesap başarıyla oluşturuldu!"})

@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    data = request.get_json()
    email = data.get('email')

    # Kullanıcı bilgilerini çek
    for user in users:
        if user['email'] == email:
            return jsonify(user)
    
    return jsonify({"success": False, "message": "Kullanıcı bulunamadı!"})

if __name__ == '__main__':
    app.run(debug=True)



