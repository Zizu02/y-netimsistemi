from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Bu satır tüm kökenlere izin verir

# Veritabanı bağlantı ayarları (örnek)
DATABASE_CONFIG = {
    'dbname': 'depo',
    'user': 'depo_user',
    'password': 'fyL02LkCj6DJnyf2oE7rLTvgGa2mSVOC',
    'host': 'dpg-cretkstsvqrc73fmrhp0-a.frankfurt-postgres.render.com',
}

@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is missing'}), 400

    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT email, address, phone FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({'success': True, 'email': user[0], 'address': user[1], 'phone': user[2]})
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500

@app.route('/create_payment', methods=['POST'])
def create_payment():
    data = request.json
    email = data.get('email')
    payment_amount = data.get('payment_amount')
    user_name = data.get('user_name')
    user_address = data.get('user_address')
    user_phone = data.get('user_phone')
    merchant_oid = data.get('merchant_oid')

    if not all([email, payment_amount, user_name, user_address, user_phone, merchant_oid]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    try:
        # Burada ödeme işlemi başlatma kodu eklenmelidir
        # Örnek olarak bir token oluşturalım
        token = str(uuid.uuid4())

        return jsonify({'success': True, 'token': token})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)

