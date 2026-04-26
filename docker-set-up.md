# Cashia Installation Instructions with Docker

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

5 Go out of your server and reconect

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