from enum import Enum

class StatusAposta(str, Enum):
    PENDENTE = "PENDENTE"
    GANHOU = "GANHOU"
    PERDEU = "PERDEU"
    EMPATOU = "EMPATOU"