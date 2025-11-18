# sprint 7/servico-produtos/app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Serviço de Produtos da Vinheria Agnello - Online!"

@app.route('/produtos')
def get_produtos():
    produtos = [
        {"id": 1, "nome": "Vinho Tinto Cabernet", "preco": 85.00},
        {"id": 2, "nome": "Vinho Branco Chardonnay", "preco": 60.00},
        {"id": 3, "nome": "Vinho Rosé Seco", "preco": 70.00}
    ]
    return jsonify(produtos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)