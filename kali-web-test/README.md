
# 🎯 Laboratorio de Pruebas de Seguridad Integrado

Este proyecto utiliza Docker Compose para levantar un entorno completo de pentesting y análisis de seguridad, incluyendo múltiples aplicaciones vulnerables como objetivos y herramientas de ataque y análisis.

## ⚠️ Requisito Crítico de Configuración del Anfitrión

**SonarQube requiere una configuración específica del kernel de Linux para poder funcionar. Sin este paso, el contenedor `sonarqube_server` entrará en un bucle de reinicio.**

Este cambio es necesario porque SonarQube depende de Elasticsearch, que necesita una mayor cantidad de "áreas de memoria virtual" de las que la mayoría de los sistemas Linux proporcionan por defecto.

### 1. Aplicar la Configuración (Solución Temporal)

Antes de ejecutar `docker compose up`, debe ejecutar el siguiente comando en la terminal de su máquina anfitriona (local o Codespace). Necesitará privilegios de administrador (`sudo`).

```bash
sudo sysctl -w vm.max_map_count=262144
```

**Nota:** Este ajuste se perderá cada vez que reinicie su máquina.

### 2. Hacer la Configuración Permanente (Recomendado para uso local)

Para evitar tener que ejecutar el comando anterior cada vez que reinicia su máquina, puede hacerlo permanente. Edite el archivo de configuración del sistema `sysctl.conf`:

```bash
# Abrir el archivo de configuración con un editor de texto
sudo nano /etc/sysctl.conf

# Añadir la siguiente línea al final del archivo:
vm.max_map_count=262144

# Guardar y cerrar el archivo (en nano: Ctrl+X, luego Y, luego Enter).
```

Después de guardar el archivo, el cambio se aplicará automáticamente en el próximo reinicio del sistema.

## 🚀 Inicio del Entorno

Una vez que haya realizado la configuración del `vm.max_map_count`, puede levantar todo el entorno con un solo comando:

```bash
docker compose up -d
```