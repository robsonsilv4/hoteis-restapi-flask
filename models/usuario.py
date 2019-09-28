from sql_alchemy import banco


class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'
    usuario_id = banco.Column(banco.Integer, primary_key=True)
    email = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    @classmethod
    def encontrar_usuario(cls, usuario_id):
        usuario = cls.query.filter_by(usuario_id=usuario_id).first()
        if usuario:
            return usuario
        return None

    @classmethod
    def encontrar_por_email(cls, email):
        usuario = cls.query.filter_by(email=email).first()
        if usuario:
            return usuario
        return None

    def salvar_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    def remover_usuario(self):
        banco.session.delete(self)
        banco.session.commit()

    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'email': self.email,
        }
