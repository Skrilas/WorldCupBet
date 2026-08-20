from sqlmodel import Session
from decimal import Decimal
from datetime import date
import re

from src.exceptions.business import ConflictError, BusinessRuleError, NotFoundError
from src.repository.usuario_repository import UsuarioRepository
from src.schemas.ranking_usuario import RankingUsuario
from src.schemas.usuario_create import UsuarioCreate
from src.config.hash import password_hasher
from src.models.usuario import Usuario
from src.database import engine

class UsuarioService:

    @staticmethod
    def _validar_senha(senha: str):
        """Valida se a senha atende aos requisitos mínimos de segurança."""
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
            raise BusinessRuleError(f"A senha deve {', '.join(erros)}.")

    @staticmethod  
    def _validar_maioridade(data_nascimento: date):
        """Verifica se o usuário possui pelo menos 18 anos."""
        data_atual = date.today()
        idade = data_atual.year - data_nascimento.year

        if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        
        if idade < 18:
            raise BusinessRuleError("O usuário deve ser maior de 18 anos.")

    @staticmethod
    def _validar_nome(nome: str):
        """Valida se o nome possui a quantidade mínima de caracteres."""
        if len(nome.strip()) < 3:
            raise BusinessRuleError("O nome deve ter pelo menos 3 caracteres.")


    @classmethod
    def cadastrar_usuario(cls, usuario_create: UsuarioCreate) -> Usuario:
        """Valida e cadastra um novo usuário no sistema."""
        with Session(engine) as session:
            repo = UsuarioRepository(session)

            if repo.buscar_por_email(usuario_create.email):
                raise ConflictError("E-mail já cadastrado.")
            
            if repo.buscar_por_cpf(usuario_create.cpf):
                raise ConflictError("CPF já cadastrado.")

            if repo.buscar_por_login(usuario_create.login):
                raise ConflictError("Login já cadastrado.")

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
        """Valida e altera a senha de um usuário."""
        with Session(engine) as session:
            repo = UsuarioRepository(session)
            
            usuario = repo.buscar_por_id(id_usuario)
            if not usuario:
                raise NotFoundError("Usuário não encontrado.")
            
            cls._validar_senha(senha)
            usuario.senha_hash = password_hasher.hash(senha)
            session.commit()

    @classmethod
    def consultar_pontos(cls, id_usuario: int) -> Decimal:
        """Retorna o saldo de pontos de um usuário."""
        usuario = cls.buscar_usuario(id_usuario)

        return usuario.pontos

    @staticmethod
    def mostrar_ranking() -> list[RankingUsuario]:
        """Retorna o ranking dos usuários ordenado pelos palpites corretos."""
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
        """Busca um usuário pelo ID."""
        with Session(engine) as session:
            repo = UsuarioRepository(session)
            usuario = repo.buscar_por_id(id)
            if not usuario:
                raise NotFoundError("Usuário não encontrado.")
            return usuario
        
    @staticmethod
    def cancelar_participacao_no_sistema(id_usuario: int) -> None:
        """Inativa a conta do usuário, mantendo seus dados no sistema."""
        with Session(engine) as session:
            repo = UsuarioRepository(session)

            usuario = repo.buscar_por_id(id_usuario)
            if not usuario:
                raise NotFoundError("Usuário não encontrado.")
            if not usuario.ativo:
                raise ConflictError("Usuário já está inativo")
            
            usuario.ativo = False
            session.commit()
