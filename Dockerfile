FROM python:3.11-slim

WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ana dosyayı kopyala
COPY main.py .

# Tokeni doğrudan yaz (GEÇİCİ!)
ENV DISCORD_TOKEN=MTUzMzQ2NDk2Mjg4MDc3MDIwOQ.GPkodu.5KwkUqhRaCKk1hPJU9Q7qXDR2XoKmm60R01icA

# Botu başlat
CMD ["python", "main.py"]
