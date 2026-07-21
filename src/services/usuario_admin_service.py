from sqlmodel import Session

from repository.usuario_repository import UsuarioRepository
from schemas.usuario_read import UsuarioRead
from models.usuario import Usuario
from database import engine

class UsuarioAdminService:


    @staticmethod
    def _usuario_para_read(usuario: Usuario) -> UsuarioRead:
        return UsuarioRead(
            id=usuario.id,
            nome=usuario.nome,
            email=usuario.email,
            cpf=usuario.cpf,
            data_nascimento=usuario.data_nascimento,
            pontos=usuario.pontos,
            palpites_corretos=usuario.palpites_corretos,
            ativo=usuario.ativo
        )

    @classmethod
    def listar_usuarios(cls) ->list[UsuarioRead]:
        with Session(engine) as session:
            repo = UsuarioRepository(session)

            usuarios = repo.listar()

            return[cls._usuario_para_read(usuario)
                
                for usuario in usuarios]

    @classmethod
    def buscar_usuario_por_cpf(cls, cpf: str) -> UsuarioRead:
         with Session(engine) as session:
            repo = UsuarioRepository(session)

            usuario = repo.buscar_por_cpf(cpf)
            if not usuario:
                raise ValueError("Usuário não encontrado.")
            
            return cls._usuario_para_read(usuario)
