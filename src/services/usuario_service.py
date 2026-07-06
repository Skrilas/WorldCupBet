from sqlmodel import Session
from decimal import Decimal

from repository.usuario_repository import UsuarioRepository
from models.usuario import Usuario
from database import engine

class UsuarioService:

    @staticmethod
    def busca_usuario(id: int):
        with Session(engine) as session:
            repo = UsuarioRepository(session)
            usuario = repo.buscar_por_id(id)
            if not usuario:
                raise ValueError("Usuário não encontrado.")
            return usuario