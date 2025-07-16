from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Waze Alertes !"}

@app.get("/refresh")
def refresh_data():
    # Tu pourras appeler ta fonction de screenshot ici plus tard
    return JSONResponse(content={"status": "Capture déclenchée (exemple)"})
