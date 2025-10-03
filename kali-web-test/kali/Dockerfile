FROM kalilinux/kali-rolling

# Instalar herramientas clave
RUN apt update && apt install -y \
    nmap \
    nikto \
    sqlmap \
    metasploit-framework \
    hydra \
    john \
    dirb \
    gobuster \
    wfuzz \
    curl \
    wget \
    net-tools \
    iputils-ping \
    dnsutils \
    python3-pip \
    git \
    vim \
    sudo \
    ttyd \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Instalar herramientas modernas (opcional)
RUN pip3 install requests beautifulsoup4

# Crear usuario kali
RUN useradd -m -s /bin/bash kali && \
    echo "kali:kali" | chpasswd && \
    adduser kali sudo

# Permitir sudo sin contraseña (solo para lab)
RUN echo 'kali ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Exponer puerto ttyd
EXPOSE 7681

# Iniciar ttyd al arrancar
CMD ["ttyd", "-p", "7681", "bash"]