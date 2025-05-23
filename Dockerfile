FROM python:3.12-slim

RUN apt update && apt install -y \
    ffmpeg \
    libopus0 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
