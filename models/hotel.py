class HotelModel:
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome,
        self.estrelas = estrelas
        self.diaria = diaria,
        self.cidade = cidade

    # TODO: Corrigir: nome e diaria estão recebendo tuplas
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome[0],
            'estrelas': self.estrelas,
            'diaria': self.diaria[0],
            'cidade': self.cidade
        }
