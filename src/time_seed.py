from repository.apostas_repository import ApostasRepository
from services.gerenciador_api_historico import GerenciadoApiHistorico
from services.sync_partidas_service import SyncPartidasService
from services.time_service import TimeService
from sqlmodel import Session
from database import engine

if __name__ == "__main__":
    # with Session(engine) as session:
        # repo = ApostasRepository(session)
        # resultado = repo.obter_estatisticas_aposta(2)
        # print(resultado)
    # time = TimeService.buscar_historico_copas(9)

    # print(time)
    SyncPartidasService.sincronizar_partidas()