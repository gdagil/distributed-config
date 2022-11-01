# Создание сети для postgres-db
docker network create postgres-database

# Запуск postgres и pgadmin
docker compose -f docker-compose.db.yaml up -d

# Запуск API
docker compose -f docker-compose.yaml up --build 