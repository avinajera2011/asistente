#!/bin/bash
set -e

# Realiza la creación del usuario y la base de datos para SonarQube
# Las variables de entorno SONAR_DB_USER, etc., son pasadas desde el docker-compose.yml
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $SONAR_DB_USER WITH PASSWORD '$SONAR_DB_PASSWORD';
    CREATE DATABASE $SONAR_DB_NAME;
    GRANT ALL PRIVILEGES ON DATABASE $SONAR_DB_NAME TO $SONAR_DB_USER;
EOSQL