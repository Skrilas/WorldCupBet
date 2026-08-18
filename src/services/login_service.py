from argon2.exceptions import VerifyMismatchError 
from sqlmodel import Session

from src.exceptions.business import AuthenticationError, AuthorizationError
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
                raise AuthenticationError("Login ou senha inválidos.")
            if not usuario.ativo:
                raise AuthenticationError("Conta inativa.")
            
            try:
                password_hasher.verify(usuario.senha_hash, senha)
            except VerifyMismatchError:
                raise AuthenticationError("Login ou senha inválidos."
                ) from None   
            return usuario
        
    
    @staticmethod
    def verificar_admin(usuario: Usuario) -> None:
        if not usuario.admin:
            raise AuthorizationError("Apenas administradores podem acessar esta funcionalidade.")
