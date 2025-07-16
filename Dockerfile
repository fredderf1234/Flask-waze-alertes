
FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app", "-k", "uvicorn.workers.UvicornWorker"]
