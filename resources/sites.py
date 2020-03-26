from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
    def get(self, url):
        site = SiteModel.encontrar_site(url)
        if site:
            return site.json()
        return {'message': 'Site não encontrado.'}, 404

    def post(self, url):
        if SiteModel.encontrar_site(url):
            return {'message': f'O site {url} já exite.'}, 400
        site = SiteModel(url)
        try:
            site.salvar_site()
        except:
            return {'message': 'Ocorreu um erro interno.'}, 500
        return site.json()

    def delete(self, url):
        site = SiteModel.encontrar_site(url)
        if site:
            site.remover_site()
            return {'message': 'Site removido.'}
        return {'message': 'Site não encontrado'}, 404
