from fastapi import FastAPI, APIRouter
router = APIRouter(prefix='/search', tags=['User'])

@router.get('')
def search():
    return 'search'
