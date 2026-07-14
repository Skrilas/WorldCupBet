from sqlmodel import Session, select
from models.usuario import Usuario

class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, usuario: Usuario):
        self.session.add(usuario)

    def buscar_por_id(self, id: int) -> Usuario | None:
        return self.session.get(Usuario, id)
    
    def buscar_por_id_atualizar(self, id:int) -> Usuario | None:
        statement = select(Usuario).where(Usuario.id == id).with_for_update()
        return self.session.exec(statement).first()

    def listar(self) -> list[Usuario]:
        return self.session.exec(select(Usuario)).all()
    
    def listar_por_palpites(self) -> list[Usuario]:
        return self.session.exec(select(Usuario).order_by(
                                    Usuario.palpites_corretos.desc(), 
                                    Usuario.pontos.desc()
                                )
                            ).all()
    
    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        statement = select(Usuario).where(Usuario.cpf == cpf)
        return self.session.exec(statement).first()
    
    def buscar_por_email(self, email: str) -> Usuario | None:
        statement = select(Usuario).where(Usuario.email == email)
        return self.session.exec(statement).first()