#Importação das dependência necessárias
from flask import Flask , request, jsonify

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#Modelagem do banco de dados(id,nome,preço,descrição)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)

# Definição das rotas e funções

#Rota para add os produtos

@app.route('/api/products/add' , methods=["POST"])

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

    return jsonify({"message":"Dados actualizados"})





app.run(debug=True)