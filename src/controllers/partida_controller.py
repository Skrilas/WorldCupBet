from fastapi import APIRouter

from src.services.partida_service import PartidaService

router = APIRouter(
    prefix="/partida",
    tags=["Partidas"]
)

@router.get("")
def listar_partidas():
    return PartidaService.listar_partidas()

@router.get("/{id}")
def mostrar_partida(id: int):
    return PartidaService.mostrar_partida(id)