FROM python:3.12-slim

WORKDIR /app

# Source packages are copied relative to the repository-root build context.
# The application packages must contain their real src/ and README.md files.
COPY constraints.txt /app/constraints.txt
COPY cashia-api /app/cashia-api
COPY cashia-core /app/cashia-core
COPY cashia-model /app/cashia-model
COPY cashia-credit-engine /app/cashia-credit-engine

# Resolve third-party and local project requirements in ONE pip invocation.
# --no-cache-dir reduces image size; the local projects are not installed editable.
RUN python -m pip install --no-cache-dir \
    -c /app/constraints.txt \
    -r /app/cashia-api/requirements.txt \
    /app/cashia-core \
    /app/cashia-model \
    /app/cashia-credit-engine \
    /app/cashia-api \
 && python -m pip check

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "cashia_api.main:app", "--bind", "0.0.0.0:8000"]
