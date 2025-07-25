#Importação das dependência necessárias
from flask import Flask , request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user, LoginManager, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.log_view = 'login'
CORS(app)

#Criação do Lgin e do Logout
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True)

#Modelagem do banco de dados(id,nome,preço,descrição)
class Product(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)

# Criação do carrinho
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),nullable=False)

# Definição das rotas e funções
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/login', methods=['POST'])
def log():
    data = request.json

    user = User.query.filter_by(Username=data.get("Username")).first()
    if user and data.get("password") == user.password:
        login_user(user)
        return jsonify({"message":"Login bem sucessido"})  
    return jsonify({"message":"Falha no login"}), 401

@app.route('/logout', methods=['POST'])
#@login_required
def logout_user():
    load_user()
    return jsonify({"message":"Logout bem sucessido"})


#Rota para add os produtos

@app.route('/api/products/add' , methods=["POST"])
#@login_required
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
#@login_required
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
            "description" :product.description
        })
        product_list.append(product_data)

    return jsonify(product_list)

#checkout
@app.route('/api/cart/add/<int:product_id>' , methods=['POST'])
@login_required

def add_to_cart(product_id):
    #usuario
    user = User.query.get(int(current_user.id))
    #produto
    product = Product.query.get(product.id)

    if user and product:
        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify("Produto adicionado ao carrinho")
    return jsonify("Falha ao adicionar produto adicionado ao carrinho")

#remover item

@app.route('/api/cart/remove/<int:product_id>' , methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id= product_id.id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify("Produto removidoddo carrinho")
    return jsonify("Falha ao remover produto do carrinho"), 400

@app.route('/api/cart' , methods=['GET'])
@login_required
def view_cart(product_id):
    #usuario
    user= User.query.get(int(current_user.id))
    cart_items = user.cart
    cart_content = []
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        cart_content.app({

                    "id": cart_item.id,
                    "user_id": cart_item.user_id,
                    "product_id": cart_item.product_id,
                    "product_name" : product.name
                })
    return jsonify(cart_content)

@app.route('/api/cart/checkout', methods=["POST"])
@login_required
def checkout():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    for cart_item in cart_items:

        db.session.delete()
        db.session.commit()
    return jsonify({"message": "Checkout concluído"})










app.run(debug=True)