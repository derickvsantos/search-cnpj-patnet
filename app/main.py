from fastapi import FastAPI
from routes import search

app = FastAPI()

@app.get('/health-check')
def health_check():
    return True

app.include_router(search.router)