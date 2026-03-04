# Système de gestion de collection Lego

Application REST pour gérer une collection de pièces Lego et voir les pièces disponibles.

## Architecture

![Schéma Architecture](Schema%20DrawIO.png)

2 services REST :
- **Service Pieces** (port 5000) : API publique
- **Service Models** (port 5001) : API privée avec authentification

## Installation

```bash
uv sync
```

## Lancer les services

Terminal 1 :
```bash
uv run flask --app service_pieces run --port 5000
```

Terminal 2 :
```bash
uv run flask --app service_models run --port 5001
```

## Tests

```bash
uv run pytest
```

## Utilisation

Voir les pièces disponibles (API publique) :
```bash
curl http://localhost:5000/pieces/available
```

Créer une pièce :
```bash
curl -X POST http://localhost:5000/pieces \
  -H "Content-Type: application/json" \
  -d '{"name":"Brique 2x4","color":"rouge","category":"brique"}'
```
