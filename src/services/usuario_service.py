from sqlmodel import Session
from decimal import Decimal
import re

from repository.usuario_repository import UsuarioRepository
from models.usuario import Usuario
from database import engine

class UsuarioService:

    def validar_senha(senha: str):
        erros = []

        if len(senha) < 8:
            erros.append("ter pelo menos 8 caracteres")

        if not re.search(r"[A-Z]", senha):
            erros.append("conter uma letra maiúscula")

        if not re.search(r"[a-z]", senha):
            erros.append("conter uma letra minúscula")

        if not re.search(r"\d", senha):
            erros.append("conter um número")

        if not re.search(r"[^A-Za-z0-9]", senha):
            erros.append("conter um caractere especial")

        if erros:
            raise ValueError(f"A senha deve {', '.join(erros)}.")
        
    def validar_email():
        repo

    def validar_cpf():
        pass

    @classmethod
    def cadastrar_usuario(cls, usuario: Usuario):
        pass


    def busca_usuario(id: int):
        with Session(engine) as session:
            repo = UsuarioRepository(session)
            usuario = repo.buscar_por_id(id)
            if not usuario:
                raise ValueError("Usuário não encontrado.")
            return usuario