import os
import uvicorn
import asyncio
from app import screenshot_loop

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    # Démarre la boucle de screenshot dans un thread parallèle
    loop = asyncio.get_event_loop()
    loop.create_task(screenshot_loop())

    # Démarre le serveur web
    uvicorn.run("app:app", host="0.0.0.0", port=port)
