from pydantic import BaseModel

class HistoricoCopa(BaseModel):
    ano: int
    colocacao: int | None
    jogos: int | None
    vitorias: int | None
    empates: int | None
    derrotas: int | None
    gols_pro: int | None
    gols_contra: int | None
    pontos: int | None