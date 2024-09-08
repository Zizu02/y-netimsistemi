from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

# Çevresel değişkenleri yükle
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# CORS ayarları
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://sapphire-algae-9ajt.squarespace.com"}})

# PostgreSQL bağlantı bilgileri
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Tablo oluşturma
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(20),
            address TEXT,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Hesap oluşturma
@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not password or not address or not phone:
        return jsonify({"success": False, "message": "Eksik bilgi!"})

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO users (email, password_hash, address, phone)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
        ''', (email, password, address, phone))
        conn.commit()
        return jsonify({"success": True, "message": "Hesap başarıyla oluşturuldu!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)})
    finally:
        cur.close()
        conn.close()

# Kullanıcı bilgilerini getirme
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    email = request.args.get('email')
    
    if not email:
        return jsonify({"success": False, "message": "E-posta sağlanmalı!"})

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT email, phone, address FROM users WHERE email = %s
    ''', (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({"success": True, "user_info": {
            "email": user[0],
            "phone": user[1],
            "address": user[2]
        }})
    else:
        return jsonify({"success": False, "message": "Kullanıcı bulunamadı."})

# Test fonksiyonu
def test_create_table():
    create_table()
    print("Tablo oluşturuldu.")

# Testi çalıştırın
if __name__ == "__main__":
    test_create_table()
    app.run(debug=True)

