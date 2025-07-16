# Étape 1 : image Playwright officielle avec Python
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Étape 2 : répertoire de travail
WORKDIR /app

# Étape 3 : copie des fichiers
COPY requirements.txt requirements.txt
COPY app.py app.py

# Étape 4 : installation des dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Étape 5 : exposer le port 80 (et non 8080)
EXPOSE 80

# Étape 6 : démarrage du serveur avec Gunicorn sur le port 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]
