from sqlmodel import Session,SQLModel
from database import engine
from models.time import Time

if __name__ == "__main__":
    # Cria as tabelas caso não existam
    SQLModel.metadata.create_all(engine)

    novo_time = Time(
        nome="Grêmio"
    )

    with Session(engine) as session:
        session.add(novo_time)
        session.commit()
        session.refresh(novo_time)

    print(f"Time criado com ID {novo_time.id}")