# biblioteca para trabalhar com json
import json

from flask import Flask, Response, request

# conexão com o database
from flask_sqlalchemy import SQLAlchemy

# criação do app database carros
app = Flask('carros')

# haverá modificações no database
# por padrão, em aplicações em Produção, isso: 'app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False' is False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# configurações do database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/aula_25_09_24_database'

# declaração/configuracao da 'variável' que recebera o database
mybd = SQLAlchemy(app)

# definição da estrutura da tabela de carros
class Carros(mybd.Model):
    id =     mybd.Column(mybd.Integer, primary_key = True)
    marca =  mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor =  mybd.Column(mybd.Float)
    cor =    mybd.Column(mybd.String(20))
    numero_vendas =  mybd.Column(mybd.Float)
    ano =    mybd.Column(mybd.String())

# convertendo a tabela em JSON
def to_json(self):
    return{'id': self.id, 
           'marca': self.marca,
           'modelo': self.modelo,
           'valor': self.valor,
           'cor': self.cor,
           'numero_vendas': self.numero_vendas,
           'ano': self.ano}

# ****** API ******
# selecionar tudo (GET)
@app.route('/carros', methods=['GET'])
def selecionar_carros():
    # executa uma consulta no database para obter todos (all) os registros da tabela carros
    # o método query.all() retorna uma lista de objetos 'carros'
    carro_objetos = Carros.query.all()
    carro_json = [carro.to_json() for carro in carro_objetos]
    return gera_response(200, 'carros', carro_json)


# seleção individual (por id/atributo)
@app.route('/carros/<id>', methods=['GET'])
def seleciona_carro_id(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    carro_json = carro_objetos.to_json()
    return gera_response(200, 'carros', carro_json)

# cadastrar no database
@app.route('/carros', methods=['POST'])
def cadastrar_carro():
    body = request.get_json()

    try:
        carro = Carros(id=body['id'],
                       marca=body['marca'],
                       modelo=body['modelo'],
                       valor=body['valor'],
                       cor=body['cor'],
                       numero_vendas=body['numero_vendas'],
                       ano=body['ano'])

        mybd.session.add(carro)
        mybd.session.commit()
        return gera_response(201, 'carros', carro.to_json(), 'Cadastrado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_response(400, 'carros', {}, 'Erro ao cadastrar!')
    
# atualizar database
@app.route('/carros/<id>', methods=['PUT'])
def atualizar_carro(id):

    # consulta por id 
    carro_objetos = Carros.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if 'marca' in body:
            carro_objetos.marca = body['marca']






def gera_response(status, nome_database, conteudo_database, mensagem = False):
    body = {}
    body[nome_database] = conteudo_database

    if mensagem:
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')   