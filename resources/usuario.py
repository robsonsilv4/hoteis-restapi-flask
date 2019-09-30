from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from models.usuario import UsuarioModel

atributos = reqparse.RequestParser()
atributos.add_argument('email', type=str, required=True,
                       help='O campo de email é obrigatório.')
atributos.add_argument('senha', type=str, required=True,
                       help='O campo de senha é obrigatório.')


class UsuarioCadastro(Resource):
    def post(self):
        dados = atributos.parse_args()
        if UsuarioModel.encontrar_por_email(dados['email']):
            return {'message': 'O email {} já está sendo utilizado.'.format(dados['email'])}
        usuario = UsuarioModel(**dados)
        usuario.salvar_usuario()
        return {'message': 'Usuário criado com sucesso.'}, 201


class UsuarioLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        usuario = UsuarioModel.encontrar_por_email(dados['email'])
        if usuario and safe_str_cmp(usuario.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=usuario.usuario_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'O email ou senha estão incorretos.'}, 401


class UsuarioLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_required)
        return {'message': 'Deslogado com sucesso.'}, 200


class Usuario(Resource):
    def get(self, usuario_id):
        usuario = UsuarioModel.encontrar_usuario(usuario_id=usuario_id)
        if usuario:
            return usuario.json()
        return {'message': 'Usuário não encontrado.'}, 404

    @jwt_required
    def delete(self, usuario_id):
        usuario = UsuarioModel.encontrar_usuario(usuario_id=usuario_id)
        if usuario:
            usuario.remover_usuario()
            return {'message': 'Usuário removido.'}
        return {'message': 'Usuário não encontrado'}, 404
