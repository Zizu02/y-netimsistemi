from flask import Flask, request, jsonify

app = Flask(__name__)

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

    # Kullanıcıyı ekle
    users.append({
        "email": email,
        "password": password,
        "address": address,
        "phone": phone
    })
    
    return jsonify({"success": True, "message": "Hesap başarıyla oluşturuldu!"})

if __name__ == '__main__':
    app.run(debug=True)
