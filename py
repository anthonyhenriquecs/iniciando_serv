from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Comente a criação do banco de dados aqui
# db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], age=data['age'])
    # Use o contexto de aplicação Flask para adicionar e commitar ao banco de dados
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    # Use o contexto de aplicação Flask para consultar todos os usuários
    with app.app_context():
        users = User.query.all()
        output = []
        for user in users:
            user_data = {'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age}
            output.append(user_data)
    return jsonify({'users': output})

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    # Use o contexto de aplicação Flask para consultar um usuário específico
    with app.app_context():
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user_data = {'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age}
    return jsonify({'user': user_data})

if __name__ == '__main__':
    app.run(debug=True)
