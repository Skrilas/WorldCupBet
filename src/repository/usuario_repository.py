from sqlmodel import Session, select
from models.usuario import Usuario

class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, usuario: Usuario):
        self.session.add(usuario)

    def buscar_por_id(self, id: int):
        return self.session.get(Usuario, id)

    def listar(self):
        return self.session.exec(select(Usuario)).all()
    
    def buscar_por_email(self, email: str):
        statement = select(Usuario).where(Usuario.email == email)
        return self.session.exec(statement).first()