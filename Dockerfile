FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY ../cashia-core /app/cashia-core
COPY ../cashia-model /app/cashia-model
COPY ../cashia-credit-engine /app/cashia-credit-engine
COPY . /app/cashia-api

RUN pip install --upgrade pip

RUN pip install -e /app/cashia-core
RUN pip install -e /app/cashia-model
RUN pip install -e /app/cashia-credit-engine
RUN pip install -r /app/cashia-api/requirements.txt
RUN pip install -e /app/cashia-api

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "cashia_api.main:app", "--bind", "0.0.0.0:8000"]