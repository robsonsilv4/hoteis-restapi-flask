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

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def encontrar_hotel(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = self.encontrar_hotel(hotel_id)

        if hotel:
            return hotel

        return {'message': 'Hotel não encontrado.'}, 404

    def post(self, hotel_id):
        dados = self.argumentos.parse_args()

        hotel_objeto = HotelModel(hotel_id, **dados)

        novo_hotel = hotel_objeto.json()

        hoteis.append(novo_hotel)

        return novo_hotel, 201

    def put(self, hotel_id):
        dados = self.argumentos.parse_args()

        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()

        hotel = self.encontrar_hotel(hotel_id)

        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200

        hoteis.append(novo_hotel)

        return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis

        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]

        return hoteis
