#Importação das dependência necessárias
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY__DATABASE__URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#Modelagem do banco de dados(id,nome,preço,descrição)


# Definição das rotas e funções

@app.route('/')

def hello_world():
    return "hello world"

if __name__ == "__main__":

    app.run(debug=True)