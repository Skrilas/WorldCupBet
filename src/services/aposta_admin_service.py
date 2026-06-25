from sqlmodel import Session

from repository.partida_repository import PartidaRepository
from repository.apostas_repository import ApostasRepository
from models.usuario import Usuario
from database import engine

class ApostasAdminService:
    
    @staticmethod
    def liberar_aposta(id_partida: int, usuario: Usuario):
        if not usuario.admin:
            raise PermissionError("Apenas administradores podem liberar apostas.")
        with Session(engine) as session:
            repo = PartidaRepository(session)
            partida = repo.buscar_por_id(id_partida)
            
            if not partida:
                raise ValueError("Partida não encontrada.")
            partida.aposta_ativa = True
            
            session.commit()
        return True
    
    @staticmethod
    def buscar_aposta_da_partida(id_partida: int): #Recebe o id de Partida para busca
        with Session(engine) as session:
            repo = ApostasRepository(session)
            
            aposta = repo.buscar_por_id_partida(id_partida)
            
            if not aposta:
                raise ValueError("Nenhuma aposta encontrada para esta partida.")
            return aposta