#Importação das dependência necessárias
from flask import Flask

app = Flask(__name__)

# Definição das rotas e funções

@app.route('/')

def hello_world():
    return "hello world"

if __name__ == "__main__":

    app.run(debug=True)