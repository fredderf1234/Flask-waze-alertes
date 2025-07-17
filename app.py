import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright

app = FastAPI()
clients = set()
screenshot_count = 0

# Autoriser tous les domaines (ou restreindre à InfinityFree si besoin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        clients.remove(websocket)

@app.get("/screenshot")
async def get_screenshot():
    return FileResponse("captures/screenshot.png")

async def screenshot_loop():
    global screenshot_count
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.waze.com/live-map")

        while True:
            await page.screenshot(path="captures/screenshot.png")
            screenshot_count += 1
            print(f"Screenshot {screenshot_count} pris")

            # Notifie tous les clients WebSocket
            data = json.dumps({"count": screenshot_count})
            disconnected = set()
            for client in clients:
                try:
                    await client.send_text(data)
                except:
                    disconnected.add(client)
            clients.difference_update(disconnected)

            await asyncio.sleep(15)

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(screenshot_loop())
