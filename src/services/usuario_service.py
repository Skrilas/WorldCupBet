from sqlmodel import Session
from decimal import Decimal
from datetime import date
import re

from repository.usuario_repository import UsuarioRepository
from schemas.ranking_usuario import RankingUsuario
from schemas.usuario_create import UsuarioCreate
from config.hash import password_hasher
from models.usuario import Usuario
from database import engine

class UsuarioService:

    @staticmethod
    def _validar_senha(senha: str):
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

    @staticmethod  
    def _validar_maioridade(data_nascimento: date):
        data_atual = date.today()
        idade = data_atual.year - data_nascimento.year

        if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        
        if idade < 18:
            raise ValueError("O usuário deve ser maior de 18 anos.")

    @staticmethod
    def _validar_nome(nome: str):
        if len(nome.strip()) < 3:
            raise ValueError("O nome deve ter pelo menos 3 caracteres.")


    @classmethod
    def cadastrar_usuario(cls, usuario_create: UsuarioCreate) -> Usuario:
        with Session(engine) as session:
            repo = UsuarioRepository(session)

            if repo.buscar_por_email(usuario_create.email):
                raise ValueError("E-mail já cadastrado.")
            
            if repo.buscar_por_cpf(usuario_create.cpf):
                raise ValueError("CPF já cadastrado.")

            cls._validar_nome(usuario_create.nome)
            cls._validar_maioridade(usuario_create.data_nascimento)
            cls._validar_senha(usuario_create.senha)

            usuario = Usuario(
                nome=usuario_create.nome,
                email=usuario_create.email,
                cpf=usuario_create.cpf,
                data_nascimento=usuario_create.data_nascimento,
                login=usuario_create.login,
                senha_hash=password_hasher.hash(usuario_create.senha)
            )
            repo.salvar(usuario)
            session.commit()
            session.refresh(usuario)

            return usuario
    
    @classmethod
    def alterar_senha(cls, id_usuario: int, senha: str) -> None:
        with Session(engine) as session:
            repo = UsuarioRepository(session)
            
            usuario = repo.buscar_por_id(id_usuario)
            if not usuario:
                raise ValueError("Usuário não encontrado.")
            
            cls.validar_senha(senha)
            usuario.senha_hash = password_hasher.hash(senha)
            session.commit()

    @classmethod
    def consultar_pontos(cls, id_usuario: int) -> Decimal:
        usuario = cls.busca_usuario(id_usuario)

        return usuario.pontos

    @staticmethod
    def mostrar_ranking() -> list[RankingUsuario]:
        with Session(engine) as session:
            repo = UsuarioRepository(session)
            usuarios = repo.listar_por_palpites()

            return [RankingUsuario(
                nome=usuario.nome,
                pontos=usuario.pontos,
                palpites_corretos=usuario.palpites_corretos
            )
            for usuario in usuarios]

    @staticmethod
    def buscar_usuario(id: int) -> Usuario:
        with Session(engine) as session:
            repo = UsuarioRepository(session)
            usuario = repo.buscar_por_id(id)
            if not usuario:
                raise ValueError("Usuário não encontrado.")
            return usuario
        
    @staticmethod
    def cancelar_participacao_no_sistema(id_usuario: int) -> None:
        with Session(engine) as session:
            repo = UsuarioRepository(session)

            usuario = repo.buscar_por_id(id_usuario)
            if not usuario:
                raise ValueError("Usuário não encontrado.")
            if not usuario.ativo:
                raise ValueError("Usuário já está inativo")
            
            usuario.ativo = False
            session.commit()
