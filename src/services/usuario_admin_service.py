from sqlmodel import Session

from src.repository.usuario_repository import UsuarioRepository
from src.exceptions.business import NotFoundError
from src.schemas.usuario_read import UsuarioRead
from src.models.usuario import Usuario
from src.database import engine

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
                raise NotFoundError("Usuário não encontrado.")
            
            return cls._usuario_para_read(usuario)
