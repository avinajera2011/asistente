#!/bin/bash
set -e

echo "********** INICIANDO CONFIGURACIÓN CENTRALIZADA DE BASES DE DATOS **********"

# Nos conectamos a la base de datos de mantenimiento 'postgres', que siempre existe.
# El superusuario '$POSTGRES_USER' (msf) ya fue creado por el entrypoint.
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL

    -- === 1. Base de datos para Metasploit ===
    -- Creamos la base de datos y asignamos la propiedad al superusuario.
    SELECT 'CREATE DATABASE msfdb OWNER $POSTGRES_USER'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'msfdb')\gexec

    
    -- === 2. Usuario y Base de datos para SonarQube ===
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$SONAR_DB_USER') THEN
            CREATE ROLE $SONAR_DB_USER LOGIN PASSWORD '$SONAR_DB_PASSWORD';
            RAISE NOTICE 'Rol "$SONAR_DB_USER" creado.';
        ELSE
            RAISE NOTICE 'Rol "$SONAR_DB_USER" ya existe, omitiendo.';
        END IF;
    END
    \$\$;

    SELECT 'CREATE DATABASE $SONAR_DB_NAME OWNER $SONAR_DB_USER'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$SONAR_DB_NAME')\gexec

EOSQL

echo "[DB-INIT] Concediendo privilegios de schema a SonarQube..."
# Nos conectamos a la nueva base de datos de Sonar para conceder los privilegios necesarios.
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$SONAR_DB_NAME" -c "GRANT ALL ON SCHEMA public TO $SONAR_DB_USER;"

echo "********** CONFIGURACIÓN DE BASES DE DATOS FINALIZADA CON ÉXITO **********"