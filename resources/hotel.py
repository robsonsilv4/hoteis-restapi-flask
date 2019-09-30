import sqlite3

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.hotel import HotelModel


def normalizar_path_params(cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=10000, limit=50, offset=0, **dados):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset
    }


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave]
                         for chave in dados if dados[chave] is not None}
        parametros = normalizar_path_params(**dados_validos)

        if not parametros.get('cidade'):
            consulta = 'SELECT * FROM hoteis \
                WHERE (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) \
                LIMIT ? OFFSET ?'
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = 'SELECT * FROM hoteis \
                WHERE (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) \
                and cidade = ? LIMIT ? OFFSET ?'
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'cidade': linha[3],
                'diaria': linha[4]
            })
        return {'hoteis': hoteis}


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True,
                           help='O campo nome é obrigatório.')
    atributos.add_argument('estrelas', type=float, required=True,
                           help='O campo estrelas é obrigatório.')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel não encontrado.'}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.encontrar_hotel(hotel_id):
            return {'message': f'Hotel com id {hotel_id} não encontrado.'}, 400
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.salvar_hotel()
        except:
            return {'message': 'Ocorreu um erro ao salvar o hotel.'}, 500
        return hotel.json(), 201

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.encontrar_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.atualizar_hotel(**dados)
            hotel_encontrado.salvar_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.salvar_hotel()
        except:
            return {'message': 'Ocorreu um erro ao salvar o hotel.'}, 500
        return hotel.json(), 201

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            try:
                hotel.remover_hotel()
            except:
                return {'message': 'Ocorreu um erro ao remover o hotel.'}, 500
            return {'message': f'Removido hotel com o id {hotel_id}.'}
        return {'message': f'Hotel com id {hotel_id} não encontrado.'}, 404
