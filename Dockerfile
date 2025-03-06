FROM ubuntu:latest

# Instalar dependencias
RUN apt update && apt install -y python3 python3-pip wget

# Instalar uv
RUN wget -qO- https://astral.sh/uv/install.sh | sh && echo 'export PATH="$HOME/.local/bin:$PATH"' >> /root/.bashrc

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de la aplicación
COPY . /app

# Instalar dependencias de Python directamente
RUN /root/.local/bin/uv sync

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar FastAPI con uv
CMD ["/root/.local/bin/uv", "run", "main.py"]
