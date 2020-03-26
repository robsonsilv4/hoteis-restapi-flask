from sql_alchemy import banco


class SiteModel(banco.Model):
    __tablename__ = 'sites'
    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    def __init__(self, url):
        self.url = url

    @classmethod
    def encontrar_site(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None

    @classmethod
    def encontrar_por_id(cls, site_id):
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site
        return None

    def salvar_site(self):
        banco.session.add(self)
        banco.session.commit()

    def remover_site(self):
        [hotel.remover_hotel() for hotel in self.hoteis]
        banco.session.delete(self)
        banco.session.commit()

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis],
        }
