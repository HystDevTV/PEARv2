# 1. Basis-Image: Eine schlanke Python-Version
FROM python:3.9-slim

# 2. Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# 3. Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Den gesamten Quellcode kopieren
COPY . .

# 5. Den Port freigeben, auf dem Cloud Run lauscht (Standard: 8080)
EXPOSE 8080

# 6. Der Befehl zum Starten unserer Anwendung
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]