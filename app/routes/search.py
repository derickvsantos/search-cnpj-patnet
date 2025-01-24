from fastapi import APIRouter
from app.modules.patnet import Patnet
from app.schemas.cnpj import CNPJInput, CNPJOutput

router = APIRouter(prefix='/search', tags=['Search'])

@router.post('', response_model=CNPJOutput, description='Procura informacoes de um CNPJ no sistema PATNET')
def search(data: CNPJInput):
    cnpj = data.cnpj
    patnet = Patnet(cnpj)
    result = patnet.start()
    return result
