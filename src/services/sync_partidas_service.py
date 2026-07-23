from database import engine
from sqlmodel import Session

from services.gerenciador_api_copa import GerenciadorApiCopa
from repository.partida_repository import PartidaRepository
from services.resultado_partida_service import ResultadoPartidaService
from services.partida_service import PartidaService
from schemas.api_partida import ApiPartida

class SyncPartidasService:

    @staticmethod
    def sincronizar_partidas() -> None:
        api_partidas = GerenciadorApiCopa.obter_dados_copa("games")
        partidas_atualizadas = [ApiPartida.model_validate(partida_atualizada)
                                for partida_atualizada in api_partidas]

        with Session(engine) as session:
            repo = PartidaRepository(session)
            partidas_banco = {
                partida.api_id: partida
                for partida in repo.listar()
            }

            for partida_atualizada in partidas_atualizadas:
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
                
