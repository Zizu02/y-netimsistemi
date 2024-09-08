from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import bcrypt
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
CORS(app, supports_credentials=True)

# MySQL veritabanı bağlantı ayarları
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True
}

# Veritabanı bağlantısı kurma
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

# Kullanıcıları veritabanından al
def get_user(email):
    conn = get_db_connection()
    if conn is None:
        return None

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
    if conn is None:
        return jsonify({"success": False, "message": "Veritabanı bağlantı hatası!"})

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "E-posta zaten kayıtlı!"})

    # Şifreyi hash'le
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Yeni kullanıcıyı ekle
    cursor.execute(
        'INSERT INTO users (email, password, address, phone) VALUES (%s, %s, %s, %s)',
        (email, hashed_password, address, phone)
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
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
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
