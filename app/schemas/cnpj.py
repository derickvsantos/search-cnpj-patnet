from pydantic import BaseModel, field_validator
from datetime import datetime

class CNPJInput(BaseModel):
    cnpj: str

    @field_validator('cnpj')
    def validate_cnpj(cls, value):
        if len(value) != 14:
            raise ValueError('CNPJ inválido')
        
class CNPJOutput(BaseModel):
    inscricao_pat: str
    cnpj: str
    razao_social: str
    data_inscricao: str
    total_beneficiarios: str
    email: str

    @field_validator('data_inscricao')
    def validate_data_inscricao(cls, value):
        formated_date = datetime.strptime(value, '%Y-%m-%d')
        return formated_date.strftime('%d/%m/%Y')