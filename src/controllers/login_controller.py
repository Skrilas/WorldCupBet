from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.services.login_service import LoginService
from src.config.security import criar_token_acesso

router = APIRouter(
    prefix="/login",
    tags = ["Autenticar"]
)

@router.post("/")
def autenticar_usuario(formData: OAuth2PasswordRequestForm = Depends()):
    try:
        usuario = LoginService.autenticar(
            formData.username,
            formData.password
        )
        token = criar_token_acesso(usuario.id)

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err)
        )
    