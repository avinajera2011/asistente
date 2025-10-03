FROM nginx:alpine

# Copiar configuración
COPY nginx.conf /etc/nginx/nginx.conf
COPY auth.conf /etc/nginx/auth.conf
COPY entrypoint.sh /entrypoint.sh
COPY html/ /usr/share/nginx/html/

# Dar permisos de ejecución
RUN chmod +x /entrypoint.sh

# Usar entrypoint personalizado
ENTRYPOINT ["/entrypoint.sh"]