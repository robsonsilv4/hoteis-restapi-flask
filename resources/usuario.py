from flask_restful import Resource, reqparse

from models.usuario import UsuarioModel


class UsuarioCadastro(Resource):
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument(
            'email', type=str, required=True, help='O campo de email é obrigatório.')
        atributos.add_argument(
            'senha', type=str, required=True, help='O campo de senha é obrigatório.')
        dados = atributos.parse_args()
        if UsuarioModel.encontrar_por_email(dados['email']):
            return {'message': 'O email {} já está sendo utilizado.'.format(dados['email'])}
        usuario = UsuarioModel(**dados)
        usuario.salvar_usuario()
        return {'message': 'Usuário criado com sucesso.'}, 201


class Usuario(Resource):
    def get(self, usuario_id):
        usuario = UsuarioModel.encontrar_usuario(usuario_id=usuario_id)
        if usuario:
            return usuario.json()
        return {'message': 'Usuário não encontrado.'}, 404

    def delete(self, usuario_id):
        usuario = UsuarioModel.encontrar_usuario(usuario_id=usuario_id)
        if usuario:
            usuario.remover_usuario()
            return {'message': 'Usuário removido.'}
        return {'message': 'Usuário não encontrado'}, 404
