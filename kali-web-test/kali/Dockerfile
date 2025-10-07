# Usar una imagen base de Kali. Usar un tag específico mejora la reproducibilidad.
FROM kalilinux/kali-rolling

# Evitar que las instalaciones soliciten interacción del usuario (non-interactive frontend)
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar la lista de paquetes e instalar las dependencias necesarias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar las librerías de Python requeridas.
# MODIFICACIÓN CLAVE: Se añade la bandera --break-system-packages para anular
# la protección PEP 668 de Kali Linux en este entorno de construcción controlado.
# También se añade --no-cache-dir como buena práctica para reducir el tamaño de la imagen.
RUN pip3 install --no-cache-dir --break-system-packages requests

# Establecer un directorio de trabajo por defecto para futuros comandos
WORKDIR /root