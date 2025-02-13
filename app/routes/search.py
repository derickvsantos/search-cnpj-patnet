from fastapi import APIRouter
from app.modules.patnet import Patnet
from app.schemas.cnpj import CNPJInput, CNPJOutput, CNPJInputAsync
import asyncio
from typing import List

router = APIRouter(prefix='/search', tags=['Search'])

@router.post('', response_model=CNPJOutput, description='Procura informacoes de um CNPJ no sistema PATNET')
def search(data: CNPJInput):
    cnpj = data.cnpj
    patnet = Patnet(cnpj)
    result = patnet.start()
    return result

@router.post('/async', response_model=List[CNPJOutput], description='Procura informacoes de varios CNPJ async')
async def search_async(data: CNPJInputAsync):
    lista_cnpjs = data.list_cnpjs.split(',')
    async def process_cnpj(cnpj, delay):
        await asyncio.sleep(delay)
        patnet = Patnet(cnpj)
        return await asyncio.to_thread(patnet.start)
    tasks = [process_cnpj(cnpj, i * 0.1) for i, cnpj in enumerate(lista_cnpjs)]

    results = await asyncio.gather(*tasks)
    return results