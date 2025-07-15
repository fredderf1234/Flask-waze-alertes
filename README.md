# API Waze Alertes (Scraper JSON)

Ce serveur Flask interroge les flux non officiels JSON de Waze pour récupérer les alertes routières (accidents, bouchons, police...).

## Utilisation

```
GET /alertes?lat=...&lon=...&rayon=...
```

- `lat` = latitude
- `lon` = longitude
- `rayon` = rayon en kilomètres (optionnel, défaut = 30)

### Exemple

```
https://votre-api.onrender.com/alertes?lat=43.8&lon=-1.3&rayon=30
```

## Déploiement sur Render

1. Crée un dépôt GitHub avec ces fichiers.
2. Va sur [https://render.com](https://render.com)
3. Clique "New Web Service"
4. Connecte ton dépôt GitHub
5. Choisis :
   - Runtime = Python
   - Entrypoint = `app.py`
