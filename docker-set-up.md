# Cashia Installation Instructions with Docker

## Installation

1 Create EC2 (See [server-set-up.md](server-set-up.md))

2 Create the bucket (See [server-set-up.md](server-set-up.md))

3 Install Docker 

```bash
sudo apt update
sudo apt install docker.io docker-compose-v2 -y
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ubuntu
```

4 Clone repositories (See [server-set-up.md](server-set-up.md))

5 Go out of your server and reconnect

6 Create the file `docker-compose.yml` with the following content:

```bash
services:
  cashia-api:
    build:
      context: .
      dockerfile: cashia-api/Dockerfile
    container_name: cashia-api
    ports:
      - "8000:8000"
    environment:
      STORAGE_BACKEND: s3
      S3_BUCKET: cashia-prod-data
      S3_PREFIX: cashia
    restart: unless-stopped

  cashia-credit-engine:
    build:
      context: .
      dockerfile: cashia-api/Dockerfile
    container_name: cashia-credit-engine
    environment:
      STORAGE_BACKEND: s3
      S3_BUCKET: cashia-prod-data
      S3_PREFIX: cashia
      DB_HOST: ${DB_HOST}
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    command: ["cc-engine"]
    restart: unless-stopped
```

Adapt the lines:

```bash
      S3_BUCKET: cashia-prod-data
      S3_PREFIX: cashia
```

According to your bucket

7 Run:

 `docker compose up --build -d`

## After installation

### 1. Stop services

- **All services**

docker compose down

- **A specific service (e.g. cashia-credit-engine)**

docker compose stop cashia-credit-engine

---

### 2. Restart services

- **All services**

docker compose up -d

- **A specific service**

docker compose restart cashia-credit-engine

---

### 3. Launching `cce-db`

Run the database manager inside the container:

docker compose exec cashia-credit-engine cce-db

---

## Rebuild after changes

docker compose up --build -d

---

## Notes

If a service name does not work, run:

docker compose config --services
