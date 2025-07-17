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

@app.route('/api/products/add' , methods=["POST"])

@app.run(debug=True)

def add_produto():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"],price=data["price"],description=data.get("description", "Descrição não encontrada"))
        db.session.add(Product)
        db.session.commit()
        return "Produto cadastrado"
    return jsonify({"message":"Dados inválidos"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])

def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(Product)
        db.session.commit()
        return "Produto removido"
    return jsonify({"message":"Dados não encontrados"}), 404