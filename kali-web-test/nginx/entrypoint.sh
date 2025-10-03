#!/bin/sh
set -e

# Contraseña y hash predefinidos
ADMIN_USER="admin"
ADMIN_PASSWORD="admin*2025"
SALT="7j3H0Y0u"  # Sal fijo para reproducibilidad en laboratorio
ADMIN_PASSWORD_HASH="$apr1$7j3H0Y0u$V8c7w3B9L6W0V9e1Y7z9Q0"

# Función para crear usuario
create_user() {
    echo "Creando usuario: ${ADMIN_USER} ..."
    echo "${ADMIN_USER}:${ADMIN_PASSWORD_HASH}" > /usr/share/nginx/html/.htpasswd
    echo "Usuario creado: ${ADMIN_USER} | Contraseña: ${ADMIN_PASSWORD}"
}

# Si el archivo .htpasswd no existe, creamos el usuario
if [ ! -f /usr/share/nginx/html/.htpasswd ]; then
    create_user
else
    # Verificamos si el usuario existe en el archivo
    if grep -q "^${ADMIN_USER}:" /usr/share/nginx/html/.htpasswd; then
        echo "Usuario ${ADMIN_USER} ya existe. Usando credenciales existentes."
    else
        echo "Agregando usuario ${ADMIN_USER}..."
        echo "${ADMIN_USER}:${ADMIN_PASSWORD_HASH}" >> /usr/share/nginx/html/.htpasswd
        echo "Usuario agregado: ${ADMIN_USER} | Contraseña: ${ADMIN_PASSWORD}"
    fi
fi

# Iniciar Nginx
exec nginx -g "daemon off;"
