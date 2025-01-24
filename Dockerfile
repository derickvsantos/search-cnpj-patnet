FROM python:3.10-slim

# Define variáveis de ambiente para o Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/src

# Instalações de dependências e configurações locais
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar o projeto para o diretório do contêiner
COPY . /src/

# Define o diretório de trabalho
WORKDIR /src

# Instalar dependências com Pipenv
RUN pip install --no-cache-dir pipenv
RUN pipenv install --deploy --system

# Expor a porta padrão do Uvicorn
EXPOSE 8000

# Comando para iniciar o Uvicorn
CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]