from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)

# CORS yapılandırması
CORS(app, resources={r"/*": {
    "origins": "https://sapphire-algae-9ajt.squarespace.com",
    "supports_credentials": True
}})

# Veritabanı URL'nizi buraya ekleyin
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://depo_user:fyL02LkCj6DJnyf2oE7rLTvgGa2mSVOC@dpg-cretkstsvqrc73fmrhp0-a.frankfurt-postgres.render.com/depo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email
        }

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    email = data.get('email')
    password = data.get('password')  # Şifreyi nasıl yöneteceğiniz önemli
    address = data.get('address')
    phone = data.get('phone')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(email=email, password=password, address=address, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': True}), 201


@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    email = request.args.get('email')
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
