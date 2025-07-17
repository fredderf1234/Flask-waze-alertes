from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from threading import Thread
import asyncio
import time
import os
from playwright.sync_api import sync_playwright

app = FastAPI()

# Autoriser toutes les origines (utile pour développement)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []
count = 0

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.waze.com/fr/live-map")
        page.wait_for_timeout(5000)
        os.makedirs("captures", exist_ok=True)
        page.screenshot(path="captures/screenshot.png")
        browser.close()

async def screenshot_loop():
    global count
    while True:
        take_screenshot()
        count += 1
        for ws in clients:
            try:
                await ws.send_json({"count": count})
            except:
                pass
        await asyncio.sleep(15)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)

@app.get("/screenshot")
def get_screenshot():
    return FileResponse("captures/screenshot.png")

# ❌ Partie supprimée : plus besoin ici
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", host="0.0.0.0", port=5000)
