from sqlmodel import Session

from repository.apostas_repository import ApostasRepository
from repository.partida_repository import PartidaRepository
from schemas.apostas_create import ApostasCreate
from schemas.apostas_read import ApostasRead
from models.apostas import Apostas
from database import engine

class ApostaService:
    def calcular_odd(self):
        pass
    
    def apostar(self):
        pass
    
    def mostrar_status_aposta(self): #Recebe o id de Partida para busca
        pass
    
    def multiplicar_aposta(self):
        pass
    
    def cancelar_aposta(self):
        pass
    
    def mostrar_apostas_ativas(self):
        pass
    
    def mostrar_apostas_usuario(self):
        pass