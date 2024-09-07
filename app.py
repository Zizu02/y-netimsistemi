from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app, supports_credentials=True)

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

    # Kullanıcıyı kontrol et
    if any(u['email'] == email for u in users):
        return jsonify({"success": False, "message": "E-posta zaten kayıtlı!"})

    # Kullanıcıyı ekle
    users.append({
        "email": email,
        "password": password,
        "address": address,
        "phone": phone
    })
    
    return jsonify({"success": True, "message": "Hesap başarıyla oluşturuldu!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Eğer oturum açıksa, kullanıcıyı bilgilendir
    if 'user_email' in session:
        return jsonify({"success": False, "message": "Oturum zaten açık!"})

    user = next((u for u in users if u['email'] == email and u['password'] == password), None)
    if user:
        session['user_email'] = email
        return jsonify({"success": True, "message": "Giriş başarılı!"})
    else:
        return jsonify({"success": False, "message": "Giriş başarısız!"})

@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({"success": False, "message": "Kullanıcı oturumu yok!"})

    user = next((u for u in users if u['email'] == user_email), None)
    if user:
        return jsonify({
            "success": True,
            "email": user["email"],
            "address": user["address"],
            "phone": user["phone"]
        })
    else:
        return jsonify({"success": False, "message": "Kullanıcı bulunamadı!"})

if __name__ == '__main__':
    app.run(debug=True)

