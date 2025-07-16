# Étape 1 : Utiliser une image Python officielle
FROM python:3.12-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers nécessaires
COPY requirements.txt requirements.txt

# Étape 4 : Installer les dépendances système pour Playwright
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libxshmfence1 \
    libgbm1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Étape 5 : Installer les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Étape 6 : Installer les navigateurs Playwright
RUN playwright install --with-deps

# Étape 7 : Copier le code source
COPY . .

# Étape 8 : Lancer gunicorn avec app.py
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
