from pydantic import BaseModel, EmailStr, field_validator
from validate_docbr import CPF
from datetime import date

cpf_validator = CPF()

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    cpf: str
    data_nascimento: date
    login: str
    senha: str

    @field_validator("email")
    @classmethod #Método padrão do validator 
    def formatar_email(cls, value: EmailStr):
        return value.strip().lower()
        

    @field_validator("cpf")
    @classmethod #Método padrão do validator 
    def validar_cpf(cls, value: str):
        if not cpf_validator.validate(value):
            raise ValueError("CPF inválido.")
        return value