
import os
import time
import uvicor
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from PIL import Image
from pathlib import Path

app = FastAPI()

# Répertoire des icônes organisés par catégorie
ICON_DIR = Path("police")
CAPTURE_PATH = Path("capture/latest.jpg")
MATCH_THRESHOLD = 0.8  # Seuil de reconnaissance visuelle

def load_icons():
    icons_by_category = {}
    for category in ICON_DIR.iterdir():
        if category.is_dir():
            icons = []
            for file in category.glob("*"):
                if file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                    image = cv2.imread(str(file))
                    if image is not None:
                        icons.append(image)
            icons_by_category[category.name] = icons
    return icons_by_category

def scan_image_for_icons(capture_image, icons_by_category):
    alerts_found = []

    for category, icons in icons_by_category.items():
        for icon in icons:
            result = cv2.matchTemplate(capture_image, icon, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val >= MATCH_THRESHOLD:
                h, w, _ = icon.shape
                alert_info = {
                    "type": category,
                    "confidence": round(float(max_val), 2),
                    "position": {
                        "x": int(max_loc[0] + w // 2),
                        "y": int(max_loc[1] + h // 2)
                    }
                }
                alerts_found.append(alert_info)
                break  # Une seule détection par catégorie

    return alerts_found

@app.get("/scan")
def scan():
    if not CAPTURE_PATH.exists():
        return JSONResponse(content={"error": "No screenshot found at 'capture/latest.jpg'"}, status_code=404)

    capture_image = cv2.imread(str(CAPTURE_PATH))
    if capture_image is None:
        return JSONResponse(content={"error": "Failed to read the screenshot."}, status_code=500)

    icons_by_category = load_icons()
    results = scan_image_for_icons(capture_image, icons_by_category)

    return JSONResponse(content={"alerts": results})
