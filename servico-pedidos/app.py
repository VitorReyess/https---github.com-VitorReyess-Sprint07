# sprint 7/servico-pedidos/app.py
from flask import Flask, jsonify, request, abort
import requests

app = Flask(__name__)

# Simulação de autenticação JWT - Para fins de demonstração
# Em produção, você validaria o token criptograficamente
VALID_AUTH_TOKEN = "MEU_TOKEN_SECRETO_VINHERIA_AGNELLO_123"

@app.before_request
def check_auth():
    # Proteger a rota de criar pedido com token
    if request.path == '/criar-pedido' and request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(401, description="Autenticação necessária. Cabeçalho Authorization ausente.")
        
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            abort(401, description="Formato de token inválido. Use 'Bearer <token>'.")
        
        token = parts[1]
        if token != VALID_AUTH_TOKEN:
            abort(403, description="Token JWT inválido ou expirado.")
        print("Autenticação JWT simulada bem-sucedida para /criar-pedido.")

@app.route('/')
def home():
    return "Serviço de Pedidos da Vinheria Agnello - Online!"

@app.route('/criar-pedido', methods=['POST'])
def criar_pedido():
    dados_pedido = request.get_json()
    if not dados_pedido:
        return jsonify({"status": "erro", "mensagem": "Dados de pedido ausentes ou inválidos"}), 400

    produto_id = dados_pedido.get('produto_id')
    quantidade = dados_pedido.get('quantidade')

    if not produto_id or not quantidade:
        return jsonify({"status": "erro", "mensagem": "produto_id e quantidade são obrigatórios"}), 400

    # Simulando uma chamada para o serviço de produtos
    # 'servico-produtos' é o nome do serviço no Docker Compose!
    try:
        # Nota: Em um cenário real, você passaria o mesmo token JWT ou um novo token
        # para a comunicação entre microsserviços, mas para simplificar aqui,
        # estamos chamando o serviço de produtos sem um token (já que ele não o valida na rota /produtos)
        response = requests.get(f"http://servico-produtos:5001/produtos")
        if response.status_code == 200:
            produtos = response.json()
            produto_encontrado = next((p for p in produtos if p['id'] == produto_id), None)
            if produto_encontrado:
                return jsonify({
                    "status": "pedido criado com sucesso",
                    "id_pedido": "PED-" + str(produto_id) + "-" + str(quantidade), # ID simulado
                    "detalhes": {
                        "produto": produto_encontrado['nome'],
                        "preco_unitario": produto_encontrado['preco'],
                        "quantidade": quantidade,
                        "total": produto_encontrado['preco'] * quantidade
                    }
                }), 201
            else:
                return jsonify({"status": "erro", "mensagem": f"Produto com ID {produto_id} não encontrado"}), 404
        else:
            return jsonify({"status": "erro", "mensagem": "Não foi possível conectar ou obter produtos do serviço de produtos"}), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"status": "erro", "mensagem": "Serviço de produtos indisponível ou inacessível"}), 503
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": f"Erro inesperado ao criar pedido: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)