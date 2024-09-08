import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, request, jsonify

# .env dosyasını yükle
load_dotenv()

# Flask uygulamasını oluştur
app = Flask(__name__)

# Veritabanı bağlantı bilgilerini al
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    email = request.args.get('email')
    if not email:
        return jsonify({"success": False, "message": "E-posta sağlanmalı!"})

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cursor = conn.cursor()
        cursor.execute("SELECT email, address, phone FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({
                "success": True,
                "email": user[0],
                "address": user[1],
                "phone": user[2]
            })
        else:
            return jsonify({"success": False, "message": "Kullanıcı bulunamadı."})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Veritabanı bağlantı hatası."})

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not password or not address or not phone:
        return jsonify({"success": False, "message": "Tüm alanları doldurmalısınız."})

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        cursor = conn.cursor()
        
        # Şifreyi hash'le
        hashed_password = generate_password_hash(password)
        
        cursor.execute("""
            INSERT INTO users (email, password, address, phone) 
            VALUES (%s, %s, %s, %s)
        """, (email, hashed_password, address, phone))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Hesap başarıyla oluşturuldu!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Hesap oluşturulamadı."})

if __name__ == "__main__":
    app.run(debug=True)
