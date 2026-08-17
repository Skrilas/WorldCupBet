from fastapi import APIRouter

from src.services.time_service import TimeService

router = APIRouter(
    prefix="/times",
    tags=["Times"]
)

@router.get("")
def listar_times():
    return TimeService.listar_times()

@router.get("/{id}")
def bucar_time_por_id(id: int):
    return TimeService.buscar_time_por_id(id)

@router.get("/{id}/historico")
def buscar_historico_time(id: int):
    return TimeService.buscar_historico_copas(id)