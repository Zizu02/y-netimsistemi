from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# CORS ayarları
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://sapphire-algae-9ajt.squarespace.com"}})

# PostgreSQL bağlantı bilgileri
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

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

    hashed_password = generate_password_hash(password)
    
    # PostgreSQL veritabanına bağlanın
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cursor = conn.cursor()

    try:
        # Kullanıcıyı ekleme
        cursor.execute("INSERT INTO users (email, password, address, phone) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO UPDATE SET password = EXCLUDED.password, address = EXCLUDED.address, phone = EXCLUDED.phone", 
                       (email, hashed_password, address, phone))
        conn.commit()
        return jsonify({"success": True, "message": "Hesap başarıyla oluşturuldu!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Sunucu hatası."})
    finally:
        cursor.close()
        conn.close()

# Kullanıcı bilgilerini getiren endpoint
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    email = request.args.get('email')
    
    if not email:
        return jsonify({"success": False, "message": "E-posta sağlanmalı!"})

    # PostgreSQL veritabanına bağlanın
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cursor = conn.cursor()

    try:
        # Kullanıcıyı bulma
        cursor.execute("SELECT email, address, phone FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            user_info = {
                "email": user[0],
                "address": user[1],
                "phone": user[2]
            }
            return jsonify({"success": True, "user_info": user_info})
        else:
            return jsonify({"success": False, "message": "Kullanıcı bulunamadı."})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Sunucu hatası."})
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)


