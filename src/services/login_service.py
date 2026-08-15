from argon2.exceptions import VerifyMismatchError 
from sqlmodel import Session

from src.repository.usuario_repository import UsuarioRepository
from src.config.hash import password_hasher
from src.models.usuario import Usuario
from src.database import engine

class LoginService:
    
    @staticmethod
    def autenticar(login: str, senha: str) -> Usuario:
        with Session(engine) as session:
            repo = UsuarioRepository(session)

            usuario = repo.buscar_por_login(login)
            if not usuario:
                raise ValueError("Login ou senha inválidos.")
            if not usuario.ativo:
                raise ValueError("Conta inativa.")
            
            try:
                password_hasher.verify(usuario.senha_hash, senha)
            except VerifyMismatchError:
                raise ValueError("Login ou senha inválidos.")
            
            return usuario
        
    
    @staticmethod
    def verificar_admin(usuario: Usuario) -> None:
        if not usuario.admin:
            raise PermissionError("Apenas administradores podem acessar esta funcionalidade.")
