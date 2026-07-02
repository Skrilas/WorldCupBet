from sqlmodel import Session
from decimal import Decimal
from datetime import datetime, UTC

from repository.apostas_repository import ApostasRepository
from repository.partida_repository import PartidaRepository
from schemas.apostas_create import ApostasCreate
from schemas.apostas_read import ApostasRead
from models.apostas import Apostas
from database import engine

class ApostaService:
    
    @staticmethod
    def calcular_odd(session: Session, id_partida: int, time_apostado_id: int):
            repo = ApostasRepository(session)
            estatistica = repo.estatisticas_aposta_partida(id_partida)

            meu_time = 0
            outro_time = 0

            for coluna in estatistica:
                if time_apostado_id == coluna.time_id:
                    meu_time = coluna.total_apostadores
                else: outro_time = coluna.total_apostadores
            if meu_time == 0 and outro_time == 0: #Para incentivar o 1° usuário a apostar
                return Decimal("2")
            meu_time_calculo = max(meu_time, 1) # Considera o primeiro apostador deste time como base para o cálculo da odd
            odd = Decimal("1") + (Decimal(outro_time) / Decimal(meu_time_calculo))
            return odd

    @classmethod
    def apostar(cls, id_usuario: int, id_partida: int, id_time: int, pontos_apostados: Decimal):
        with Session(engine) as session:
            partida_repo = PartidaRepository(session)
            aposta_repo = ApostasRepository(session)
            partida = partida_repo.buscar_por_id(id_partida)
            if not partida:
                raise ValueError("Partida não encontrada.")

            if not partida.aposta_ativa:
                raise ValueError("Não é possível apostar neste jogo.")
            
            if partida.data_hora <= datetime.now(UTC):
                raise ValueError("Não é possível apostar após o inicio do jogo.")

            if id_time not in (partida.home_team_id, partida.away_team_id):
                raise ValueError("Time inválido para esta partida.")

            if not UsuarioService.valida_pontos(id_usuario, pontos_apostados):
                raise ValueError("Usuário não possui pontos suficientes.")
            
            aposta = ApostasCreate(
                usuario_id= id_usuario,
                partida_id= id_partida,
                time_id= id_time,
                qtd_pontos= pontos_apostados,
                odd= cls.calcular_odd(session=session, id_partida=id_partida, time_apostado_id=id_time)
            )
            aposta_repo.salvar(
                Apostas(**aposta.model_dump())
            )



        
    @staticmethod
    def mostrar_status_aposta(id_usuario, id_partida): #Recebe o id de Partida para busca
        with Session(engine) as session:
            repo = ApostasRepository(session)
            aposta = repo.buscar_por_id_partida(id_partida=id_partida, id_usuario=id_usuario)
            if not aposta:
                raise ValueError("Usuário não fez uma aposta nesta partida")
            return ApostasRead(
                id=aposta.id,
                usuario_id=aposta.usuario_id,
                partida_id=aposta.partida_id,
                time_id=aposta.time_id,
                qtd_pontos=aposta.qtd_pontos,
                odd=aposta.odd,
                status=aposta.status,
                pontos_ganhos=aposta.pontos_ganhos,

            )


    @staticmethod
    def multiplicar_aposta(id_usuario, id_partida):
        with Session(engine) as session:
            repo = ApostasRepository(engine)
            # Em produção

    
    def cancelar_aposta(self):
        pass
    
    def mostrar_apostas_ativas(self):
        pass
    
    def mostrar_apostas_usuario(self):
        pass