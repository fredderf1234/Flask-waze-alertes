FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Installe les navigateurs nécessaires à Playwright
RUN playwright install

COPY app.py app.py

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
