FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock /src/
RUN pipenv install --system --deploy

COPY . /src/

EXPOSE 8080

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]