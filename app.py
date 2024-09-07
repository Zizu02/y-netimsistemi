from flask import Flask, jsonify

app = Flask(__name__)

# Örnek sipariş verisi
orders = [
    {"id": 1, "email": "example1@example.com", "address": "123 Street", "status": "Hazırlanıyor"},
    {"id": 2, "email": "example2@example.com", "address": "456 Avenue", "status": "Kapının Önünde"}
]

@app.route('/get_orders', methods=['GET'])
def get_orders():
    return jsonify({"orders": orders})

@app.route('/get_user_orders/<email>', methods=['GET'])
def get_user_orders(email):
    user_orders = [order for order in orders if order['email'] == email]
    return jsonify({"orders": user_orders})

if __name__ == '__main__':
    app.run(debug=True)
