#Importação das dependência necessárias
from flask import Flask , request

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

def add_product():
    dados = request.json
    return dados