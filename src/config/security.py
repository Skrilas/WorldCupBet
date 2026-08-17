from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, UTC
import jwt

from src.services.usuario_service import UsuarioService
from src.models.usuario import Usuario
from src.config.settings import settings

ALGORITHM = "HS256"
SECRET_KEY = settings.secret_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def criar_token_acesso(usuario_id: int) -> str:
    payload = {
        "sub": str(usuario_id),
        "exp":(datetime.now(UTC) + timedelta(hours=1))
    }

    return jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        return UsuarioService.buscar_usuario(int(usuario_id))
    except(jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

def obter_admin(usuario: Usuario = Depends(obter_usuario_atual)):
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Área restrita"
        )
    return usuario