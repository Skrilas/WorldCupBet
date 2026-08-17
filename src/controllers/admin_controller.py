from fastapi import APIRouter, Depends

from src.services.sync_partidas_service import SyncPartidasService
from src.services.usuario_admin_service import UsuarioAdminService
from src.services.aposta_admin_service import ApostasAdminService
from src.config.security import obter_admin
from src.models.usuario import Usuario

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/usuarios")
def listar_usuarios(usuario: Usuario = Depends(obter_admin)):

    return UsuarioAdminService.listar_usuarios()


@router.get("/usuario/{cpf}")
def buscar_usuario(cpf: str, usuario: Usuario = Depends(obter_admin)):

    return UsuarioAdminService.buscar_usuario_por_cpf(cpf)

@router.post("/partida/sincronizar")
def sincronizar_partidas(usuario: Usuario = Depends(obter_admin)):
    SyncPartidasService.sincronizar_partidas()

    return {"detail": "Partidas sincronizadas com sucesso."}

@router.get("/partida/{id_partida}/times")
def buscar_times_da_partida(id_partida: int, usuario: Usuario = Depends(obter_admin)):
    
    return ApostasAdminService.buscar_times_da_partida(id_partida)

@router.post("/aposta/{id_partida}/liberar")
def liberar_aposta(id_partida: int, usuario: Usuario = Depends(obter_admin)):
    ApostasAdminService.liberar_aposta(id_partida)

    return {"detail": "Partida liberada para apostas."}

@router.get("/aposta/{id_partida}/overview")
def overview_apostas_da_partida(id_partida: int, usuario: Usuario = Depends(obter_admin)):
    return ApostasAdminService.overview_apostas_da_partida(id_partida)