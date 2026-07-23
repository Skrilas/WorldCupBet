from sqlmodel import Session

from repository.usuario_repository import UsuarioRepository
from repository.apostas_repository import ApostasRepository
from enums.status_aposta import StatusAposta
from models.partida import Partida

class ResultadoPartidaService:
    """Processa o resultado de uma partida encerrada.
    Atualiza o status das apostas, distribui os pontos aos usuários e incrementa o ranking de palpites quando houver vencedores."""
    
    @staticmethod
    def processar_resultado(session:Session, partida: Partida) -> None:
        usu_repo = UsuarioRepository(session)
        aposta_repo = ApostasRepository(session)

        if not partida.terminou:
            raise ValueError("Não é possível processar uma partida que ainda não terminou.")

        apostas_banco = aposta_repo.listar_por_id_partida(partida.id)

        for aposta_banco in apostas_banco:

            usuario = usu_repo.buscar_por_id(aposta_banco.usuario_id)
            if not usuario:
                raise ValueError(f"Usuário {aposta_banco.usuario_id} não encontrado.")

            if partida.vencedor_id is None:
                ganho = aposta_banco.qtd_pontos
                    
                aposta_banco.status = StatusAposta.EMPATOU
                aposta_banco.pontos_ganhos = ganho
                usuario.pontos += ganho

                continue
            
            if partida.vencedor_id == aposta_banco.time_id:
                ganho = (aposta_banco.qtd_pontos * aposta_banco.odd)

                aposta_banco.status = StatusAposta.GANHOU
                aposta_banco.pontos_ganhos = ganho
                usuario.palpites_corretos += 1
                usuario.pontos += ganho

                continue

            
            aposta_banco.status = StatusAposta.PERDEU
            aposta_banco.pontos_ganhos = 0