from repository.apostas_repository import ApostasRepository
from sqlmodel import Session
from database import engine

if __name__ == "__main__":
    with Session(engine) as session:
        repo = ApostasRepository(session)
        resultado = repo.obter_estatisticas_aposta(2)
        print(resultado)