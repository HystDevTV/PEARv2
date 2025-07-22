FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Setze ggf. Umgebungsvariablen, z.B. für Cloud Run
ENV PORT 8080

# Starte das Agenten-Skript
CMD ["python", "run_agents.py"]