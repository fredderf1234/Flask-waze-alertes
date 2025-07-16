from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# 👇 Monte le dossier "capture" pour qu'il soit accessible en statique
app.mount("/capture", StaticFiles(directory="capture"), name="capture")

@app.get("/")
def read_root():
    return {"message": "API Waze Alerte OK"}

@app.get("/ping")
def ping():
    return {"message": "pong"}
