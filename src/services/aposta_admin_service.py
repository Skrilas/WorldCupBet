from sqlmodel import Session
from decimal import Decimal
from src.exceptions.business import BusinessRuleError, NotFoundError
from src.repository.partida_repository import PartidaRepository
from src.repository.apostas_repository import ApostasRepository
from src.repository.time_repository import TimeRepository
from src.schemas.overview_apostas import OverviewApostas
from src.schemas.times_da_partida import TimesDaPartida
from src.database import engine

class ApostasAdminService:
    
    @staticmethod
    def liberar_aposta(id_partida: int) -> None:
        """Libera uma partida para que os usuários possam realizar apostas."""
        with Session(engine) as session:
            repo = PartidaRepository(session)
            partida = repo.buscar_por_id(id_partida)
            
            if not partida:
                raise NotFoundError("Partida não encontrada.")
            partida.aposta_ativa = True
            
            session.commit()
    
    @staticmethod
    def buscar_times_da_partida(id_partida: int) -> TimesDaPartida:
        """Retorna os dois times associados a uma partida."""
        with Session(engine) as session:
            partida_repo = PartidaRepository(session)
            time_repo = TimeRepository(session)
            
            partida = partida_repo.buscar_por_id(id_partida)
            if not partida:
                raise NotFoundError("Partida não encontrada.")
            
            return TimesDaPartida(
                away_team = time_repo.buscar_por_id(partida.away_team_id),
                home_team = time_repo.buscar_por_id(partida.home_team_id)
            )
            
        
    @classmethod
    def overview_apostas_da_partida(cls, id_partida: int) -> OverviewApostas:
        """Retorna um resumo das apostas realizadas em uma partida, agrupado por time."""
        times = cls.buscar_times_da_partida(id_partida)
        
        with Session(engine) as session:
            repo = ApostasRepository(session)
            dados = repo.obter_estatisticas_aposta(id_partida) #Retorna uma lista pra cada time
            
            if not dados:
                raise BusinessRuleError("Ainda não há apostas nesta partida.")
            
            #inicializar variáveis pra evitar erro por falta de aposta em um time
            total_apostadores_home = 0
            total_pontos_home = Decimal("0")
            total_apostadores_away = 0
            total_pontos_away = Decimal("0")
            
            for time in dados: #Nomeia cada dado de acordo com o shcema de OverviewApostas
                if time.time_id == times.away_team.id:
                    total_apostadores_away = time.total_apostadores
                    total_pontos_away = time.total_pontos
                elif time.time_id == times.home_team.id:
                    total_apostadores_home = time.total_apostadores
                    total_pontos_home = time.total_pontos
                else:
                    raise BusinessRuleError(f"Foi encontrada uma aposta para um time inválido na partida {id_partida}.")
                
                    
                
        return OverviewApostas(
            total_apostadores=(total_apostadores_away+total_apostadores_home),
            total_pontos=(total_pontos_away+total_pontos_home),
            away_team_name=times.away_team.nome,
            home_team_name=times.home_team.nome,
            total_pontos_away=total_pontos_away,
            total_pontos_home=total_pontos_home
        )