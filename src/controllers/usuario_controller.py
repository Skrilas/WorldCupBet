from fastapi import APIRouter, Depends

from src.services.usuario_service import UsuarioService
from src.config.security import obter_usuario_atual
from src.schemas.usuario_create import UsuarioCreate
from src.schemas.usuario_read import UsuarioRead
from src.schemas.alterar_senha import AlterarSenha
from src.models.usuario import Usuario

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuario"]
)

@router.get("/me", response_model=UsuarioRead)
def consultar_usuario_atual(usuario: Usuario = Depends(obter_usuario_atual) ):
    return usuario

@router.post("/registrar", response_model=UsuarioRead)
def criar_usuario(usuario: UsuarioCreate):
    user = UsuarioService.cadastrar_usuario(usuario)

    return user

@router.patch("/senha")
def alterar_senha_usuario(dados: AlterarSenha, usuario: Usuario = Depends(obter_usuario_atual)):
    UsuarioService.alterar_senha(id_usuario=usuario.id, senha=dados.senha)

    return {"detail": "Senha alterada com sucesso."}

@router.get("/pontos")
def consultar_pontos(usuario: Usuario = Depends(obter_usuario_atual)):
    return UsuarioService.consultar_pontos(usuario.id)

@router.get("/ranking")
def mostrar_ranking(usuario: Usuario = Depends(obter_usuario_atual)):
    return UsuarioService.mostrar_ranking()

@router.get("/cancelar-participacao")
def cancelar_participacao_no_sistema(usuario: Usuario = Depends(obter_usuario_atual)):
    UsuarioService.cancelar_participacao_no_sistema(usuario.id)

    return {"detail": "Conta inativada com sucesso."}
