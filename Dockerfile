# Image de base légère avec Python 3.12
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système requises par Playwright
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
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
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers requirements et installer Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Installer les navigateurs nécessaires à Playwright
RUN python -m playwright install --with-deps

# Copier tout le code de l'API
COPY . .

# Lancer gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
