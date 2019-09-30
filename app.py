from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.hotel import Hoteis, Hotel
from resources.usuario import Usuario, UsuarioCadastro, UsuarioLogin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super_secreta'
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<int:hotel_id>')
api.add_resource(Usuario, '/usuarios/<int:usuario_id>')
api.add_resource(UsuarioCadastro, '/cadastro')
api.add_resource(UsuarioLogin, '/login')

if __name__ == "__main__":
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
