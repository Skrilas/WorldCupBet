from src.database import engine
from sqlmodel import Session

from src.services.gerenciador_api_copa import GerenciadorApiCopa
from src.repository.partida_repository import PartidaRepository
from src.services.resultado_partida_service import ResultadoPartidaService
from src.services.partida_service import PartidaService
from src.schemas.api_partida import ApiPartida

class SyncPartidasService:

    @staticmethod
    def sincronizar_partidas() -> None:
        api_partidas = GerenciadorApiCopa.obter_dados_copa("matches")
        
        with Session(engine) as session:
            repo = PartidaRepository(session)
            partidas_banco = {
                partida.api_id: partida
                for partida in repo.listar()
            }

            for p in api_partidas:
                partida_atualizada = ApiPartida.converter_api(p)

                partida_banco = partidas_banco.get(partida_atualizada.api_id)
                if partida_banco is None:
                    continue
                if partida_banco.terminou:
                    continue
                if not partida_atualizada.finished:
                    continue

                if partida_atualizada.home_score > partida_atualizada.away_score:
                    vencedor_id = partida_atualizada.home_team_id
                elif partida_atualizada.away_score > partida_atualizada.home_score:
                    vencedor_id = partida_atualizada.away_team_id
                else:
                    vencedor_id = None

                PartidaService.atualizar_resultado(partida=partida_banco, api_partida=partida_atualizada, vencedor_id=vencedor_id)
                ResultadoPartidaService.processar_resultado(session=session, partida=partida_banco)

            session.commit()
                
