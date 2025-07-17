FROM python:3.11-slim

# Installation des dépendances système nécessaires à Playwright
RUN apt-get update && apt-get install -y \
    wget curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 \
    libxss1 libasound2 libatk1.0-0 libcups2 libdbus-1-3 \
    libxcomposite1 libxrandr2 libgbm1 libgtk-3-0 libdrm2 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers dans le conteneur
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installer les navigateurs Playwright
RUN playwright install --with-deps

# Lancer le serveur
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
