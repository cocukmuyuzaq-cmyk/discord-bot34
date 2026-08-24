FROM python:3.11-slim

WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ana dosyayı kopyala
COPY main.py .

# Botu başlat
CMD ["python", "main.py"]
