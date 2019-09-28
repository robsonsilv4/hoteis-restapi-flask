from flask_restful import Resource, reqparse

from models.usuario import UsuarioModel


class Usuario(Resource):
    def get(self, usuario_id):
        usuario = UsuarioModel.encontrar_usuario(usuario_id=usuario_id)
        if usuario:
            return usuario.json()
        return {'message': 'Usuário não encontrado.'}, 404

    def delete(self):
        usuario = UsuarioModel.encontrar_usuario(usuario_id=usuario_id)
        if usuario:
            usuario.remover_usuario()
            return {'message': 'Usuário removido.'}
        return {'message': 'Usuário não encontrado'}, 404
