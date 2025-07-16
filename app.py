from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

import os

app = FastAPI()

# ➕ Monte le dossier "capture" comme dossier statique accessible depuis /capture
app.mount("/capture", StaticFiles(directory="capture"), name="capture")


@app.get("/")
def read_root():
    return {"message": "API Waze Alertes en ligne."}


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/test-image")
def test_image():
    """
    Point de test facultatif pour vérifier l'accès à l'image latest.jpg
    """
    file_path = "capture/latest.jpg"
    if os.path.exists(file_path):
        return {"status": "OK", "url": "/capture/latest.jpg"}
    else:
        return JSONResponse(content={"error": "Image non trouvée."}, status_code=404)
