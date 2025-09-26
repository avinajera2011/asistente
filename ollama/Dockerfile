# Usa una imagen base de Ubuntu
FROM ubuntu:22.04

# Instala curl para descargar el script de Ollama y otras utilidades
RUN apt-get update && apt-get install -y curl

# Descarga y ejecuta el script de instalación de Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expone el puerto por defecto de Ollama
EXPOSE 11434

# El comando a ejecutar al iniciar el contenedor
CMD ["ollama", "serve"]