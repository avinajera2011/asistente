# Usar una imagen base ligera y específica para Nginx
FROM nginx:1.25-alpine

# Copiar el archivo de configuración principal de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar el script de punto de entrada que crea el usuario de autenticación
# Se copia a /docker-entrypoint.d/ para que se ejecute automáticamente antes de que Nginx inicie
COPY entrypoint.sh /docker-entrypoint.d/20-setup-auth.sh

# Otorgar permisos de ejecución al script
RUN chmod +x /docker-entrypoint.d/20-setup-auth.sh

# El directorio html/ no contiene nada, pero si tuviera un index.html,
# se copiaría de la siguiente manera:
# COPY ./html/ /usr/share/nginx/html/