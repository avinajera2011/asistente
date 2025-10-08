# Usamos la imagen oficial de Nginx como base
FROM nginx:1.25-alpine

# --- INICIO DE LA MODIFICACIÓN ---
# Eliminar la configuración por defecto para evitar el warning de "conflicting server name"
RUN rm -f /etc/nginx/conf.d/default.conf
# --- FIN DE LA MODIFICACIÓN ---

# Copiamos nuestra configuración de servidor personalizada
COPY devsecops.conf /etc/nginx/conf.d/devsecops.conf

# Copiamos el contenido de nuestra carpeta html al directorio raíz web
COPY ./html/ /usr/share/nginx/html/

# Copiamos nuestro script de entrada que crea el usuario 'admin'
COPY entrypoint.sh /docker-entrypoint.d/20-setup-auth.sh

# Nos aseguramos de que el script de entrada sea ejecutable
RUN chmod +x /docker-entrypoint.d/20-setup-auth.sh

EXPOSE 80

