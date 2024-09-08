from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS paketini import edin
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://sapphire-algae-9ajt.squarespace.com"}})

# Veritabanı bağlantı ayarları
DATABASE_URL = os.getenv('DATABASE_URL')

@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    email = request.args.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'E-posta sağlanmalı!'}), 400

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT email, address, phone FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return jsonify({'success': True, 'email': user[0], 'address': user[1], 'phone': user[2]})
        else:
            return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı!'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not password:
        return jsonify({'success': False, 'message': 'E-posta ve şifre sağlanmalı!'}), 400

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password, address, phone) VALUES (%s, %s, %s, %s)", 
                    (email, password, address, phone))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Hesap başarıyla oluşturuldu!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

