from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://sapphire-algae-9ajt.squarespace.com"}})

# Veritabanı URL'nizi buraya ekleyin
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://depo_user:fyL02LkCj6DJnyf2oE7rLTvgGa2mSVOC@dpg-cretkstsvqrc73fmrhp0-a.frankfurt-postgres.render.com/depo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email
        }

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400
    
    new_user = User(email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201

@app.route('/get_user_info', methods=['GET', 'OPTIONS'])
def get_user_info():
    if request.method == 'OPTIONS':
        response = app.make_response('')
        response.headers['Access-Control-Allow-Origin'] = 'https://sapphire-algae-9ajt.squarespace.com'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    email = request.args.get('email')
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
