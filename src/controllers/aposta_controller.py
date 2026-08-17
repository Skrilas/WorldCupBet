from fastapi import APIRouter, Depends

from src.config.security import obter_usuario_atual
from src.schemas.requisitos_aposta import RequisitosAposta
from src.schemas.multiplicador_aposta import MultiplicadorAposta
from src.services.aposta_service import ApostaService
from src.models.usuario import Usuario

router = APIRouter(
    prefix="/aposta",
    tags=["Apostas"]
)

@router.post("/apostar")
def apostar(dados: RequisitosAposta, usuario: Usuario = Depends(obter_usuario_atual)):
    ApostaService.apostar(id_usuario=usuario.id, id_partida=dados.id_partida, id_time=dados.id_time, pontos_apostados=dados.pontos_apostados)

    return {"detail": "Aposta criada"}

@router.get("/status-aposta/{id_partida}")
def mostrar_status_aposta(id_partida: int, usuario: Usuario = Depends(obter_usuario_atual)):

    return ApostaService.mostrar_status_aposta(id_usuario=usuario.id, id_partida=id_partida)

@router.post("/multiplicar")
def multiplicar_aposta(dados: MultiplicadorAposta, usuario: Usuario = Depends(obter_usuario_atual)):
    ApostaService.multiplicar_aposta(id_usuario=usuario.id, id_partida=dados.id_partida, multiplicador=dados.multiplicador)

    return {"detail": "Aposta multiplicada com sucesso"}

@router.get("/ativas")
def mostrar_apostas_ativas(usuario: Usuario = Depends(obter_usuario_atual)):

    return ApostaService.mostrar_apostas_ativas()

@router.get("/usuario")
def mostrar_apostas_usuario(usuario: Usuario = Depends(obter_usuario_atual)):

    return ApostaService.mostrar_apostas_usuario(usuario.id)