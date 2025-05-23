FROM python:3.12-slim

# Instalar dependencias necesarias
RUN apt update && apt install -y \
    ffmpeg \
    libopus0 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta del proyecto
WORKDIR /app

# Copiar todos los archivos
COPY . .

# Instalar paquetes de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar el bot
CMD ["python", "bot.py"]
