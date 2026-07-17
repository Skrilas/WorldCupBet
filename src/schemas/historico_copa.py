from pydantic import BaseModel

class HistoricoCopa(BaseModel):
    ano: int
    colocacao: int | None
    jogos: int
    vitorias: int
    empates: int
    derrotas: int
    gols_pro: int
    gols_contra: int
    pontos: int