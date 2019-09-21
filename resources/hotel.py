from flask_restful import Resource

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
