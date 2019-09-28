from flask_restful import Resource, reqparse

from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 1,
        'nome': 'Hotel 1',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Fortaleza'
    },
    {
        'hotel_id': 2,
        'nome': 'Hotel 2',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Pacoti'
    },
    {
        'hotel_id': 3,
        'nome': 'Hotel 3',
        'estrelas': 4.3,
        'diaria': 320.20,
        'cidade': 'Quixadá'
    },
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome')
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel não encontrado.'}, 404

    def post(self, hotel_id):
        if HotelModel.encontrar_hotel(hotel_id):
            return {'message': f'Hotel com id {hotel_id} não encontrado.'}, 400
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.salvar_hotel()
        return hotel.json(), 201

    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.encontrar_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.atualizar_hotel(**dados)
            hotel_encontrado.salvar_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        hotel.salvar_hotel()
        return hotel.json(), 201

    def delete(self, hotel_id):
        global hoteis

        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]

        return hoteis
