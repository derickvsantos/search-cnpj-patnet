FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /src/

WORKDIR /src

RUN pip install --no-cache-dir pipenv
RUN pipenv install --deploy --system

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]