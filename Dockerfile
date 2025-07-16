FROM mcr.microsoft.com/playwright/python:v1.43.1

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]