from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app, supports_credentials=True)

# MySQL veritabanı bağlantı ayarları
db_config = {
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': 'your_db_host',
    'database': 'your_db_name',
    'raise_on_warnings': True
}

# Veritabanı bağlantısı kurma
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Kullanıcıları veritabanından al
def get_user(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

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

    # Kullanıcıyı veritabanında kontrol et
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "E-posta zaten kayıtlı!"})

    # Yeni kullanıcıyı ekle
    cursor.execute(
        'INSERT INTO users (email, password, address, phone) VALUES (%s, %s, %s, %s)',
        (email, password, address, phone)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"success": True, "message": "Hesap başarıyla oluşturuldu!"})

# Giriş yapma
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = get_user(email)
    if user and user['password'] == password:
        session['user_email'] = email
        return jsonify({"success": True, "message": "Giriş başarılı!"})
    else:
        return jsonify({"success": False, "message": "Giriş başarısız!"})

# Kullanıcı bilgilerini alma
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({"success": False, "message": "Kullanıcı oturumu yok!"})

    user = get_user(user_email)
    if user:
        return jsonify({
            "success": True,
            "email": user["email"],
            "address": user["address"],
            "phone": user["phone"]
        })
    else:
        return jsonify({"success": False, "message": "Kullanıcı bulunamadı!"})

# Çıkış yapma
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_email', None)
    return jsonify({"success": True, "message": "Çıkış yapıldı!"})

if __name__ == '__main__':
    app.run(debug=True)

