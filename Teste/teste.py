#Flask: Framework web em Python para criar aplicativos web. --- é usado para construir a API.
#jsonify: Converte os dados Python em JSON para serem enviados como resposta HTTP.
#request: Permite acessar dados da solicitação HTTP (EX: corpo de uma requisição POST).
#JWTManager: Responsável por configurar o gerenciamento de tokens JWT no Flask.
#jwt_required: Um decorador que garante que uma rota só seja acessada por usuários com um token JWT válido.
#create_access_token: Função que gera um token JWT com base na identidade do usuário ( normalmente é usado depois do login).

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

#Criando uma instância do Flask, vai ser usado para definir as rotas e iniciar o servidor
app = Flask(__name__)

# Configuração de uma chave secreta para a assinatura do token
app.config["JWT_SECRET_KEY"] = "Pedro"  # Aqui tem que colocar uma chave sua e manter sem segredo, assim garente a segurança do token
jwt = JWTManager(app)                   # Inicia o gerenciamento do JWT nno Flask, assim associa o JWT com o APP

# Dados falsos de tráfego --- Aqui pode ser colocado uma API pra isso, mas deu erro kk
# É esses dados que vão ser mostrados quando acessar com o TOKEN
traffic_data = [
    {"location": "Rua A", "status": "bloqueada"},
    {"location": "Avenida B", "status": "tráfego intenso"},
    {"location": "Rodovia C", "status": "fluindo normalmente"},
]

# Rota para criar um token de acesso (Só estou simulando um login de um usuário)
@app.route("/login", methods=["POST"]) #Isso define uma rota para o POST = http://127.0.0.1:5000/login
def login():
    # Aqui ta mostrando o login, se o usuario e a senha forem diferentes disso aparece o Credenciais Inválidas
    # curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"password\": \"senha\"}" ACESSO NO CMD 
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # Validando o login
    if username != "admin" or password != "senha":
        return jsonify({"msg": "Credenciais inválidas"}), 401

    # Gerando o token depois que é feito o login --OBS: Não foi colocado um TIME no token, então enquanto ta rodadando o server da pra usar o token antigo
    access_token = create_access_token(identity={"user": username})
    return jsonify(access_token=access_token)

# Vai retornar os dados protegidos pelo metodo GET
@app.route("/traffic", methods=["GET"]) #http://127.0.0.1:5000/traffic
@jwt_required()  # Só vai acessar a rota se tiver o TOKEN válido
def get_traffic(): #Retorna os dados em JSON
    return jsonify(traffic_data), 200

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
    
#Agora é linkar isso com os ontros serviços KK
