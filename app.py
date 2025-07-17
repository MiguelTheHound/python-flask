#Importação das dependência necessárias
from flask import Flask , request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user, LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#Criação do Lgin e do Logout
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

#Modelagem do banco de dados(id,nome,preço,descrição)
class Product(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)

# Definição das rotas e funções

@app.route('/login', methods=['POST'])
def log():
    data = request.json

    user = User.query.filter_by(Username=data.get("Username")).first()
    if user and data.get("password") == user.password:
        login_user(user)
        return jsonify({"message":"Login bem sucessido"})  
    return jsonify({"message":"Falha no login"}), 401

#Rota para add os produtos

@app.route('/api/products/add' , methods=["POST"])
@login_required
def add_produto():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"],price=data["price"],description=data.get("description", "Descrição não encontrada"))
        db.session.add(Product)
        db.session.commit()
        return "Produto cadastrado"
    return jsonify({"message":"Dados inválidos"}), 400

#Rota para delete os produtos

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])

def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(Product)
        db.session.commit()
        return "Produto removido"
    return jsonify({"message":"Dados não encontrados"}), 404

#Recuprar detalhes do produto

@app.route('/api/products/<int:product_id>', methods=["GET"])

def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id" : product.id ,
            "name" : product.name,
            "price" : product.price,
            "description" : product.description
        })
    return jsonify({"message":"Dados não encontrados"}), 404

#Actualizar produtos

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])

def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        
       return jsonify({"message":"Dados não encontrados"}), 404
    
    data = request.json
    if 'name' in data :
        product.name = data['name']
    
    if 'price' in data :
        product.price = ['price']
    
    if 'description' in data :
        product.description = ['description']

    db.session.commit()
    return jsonify({"message":"Dados actualizados"})

@app.route('/api/products' , methods=['GET'])

def get_product(product_id):
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data =({
            "id" : product.id ,
            "name" : product.name,
            "price" : product.price,
            "description" : product.description
        })
        product_list.append(product_data)

    return jsonify(product_list)


app.run(debug=True)