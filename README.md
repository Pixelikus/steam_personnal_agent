# steam_personnal_agent
this interface retrieves your steam library, ask protondb for steamdeck compatibility and steamspy for metadata

Récupération de la bibliothèque Steam d’un utilisateur

Vérification de la compatibilité Steam Deck / ProtonDB

Enrichissement des jeux via SteamSpy

Analyse et suggestions via un LLM local (Ollama) OU via JSON à copier/coller dans un LLM externe

Cache JSON local pour limiter les appels API

Interface web simple (HTML / CSS / JS)

Sauvegarde des suggestions générées (JSON horodaté)

```text

steam_agent/
├── main.py                      # Point d'entrée
├── config.py                    # Configuration centralisée
├── config_local.py.example      # Template de configuration
├── requirements.txt             # Dépendances Python
├── README.md                    # Documentation
├── .gitignore
│
├── api/                         # API REST
│   ├── __init__.py
│   ├── models.py                # Modèles Pydantic
│   ├── steam_routes.py
│   ├── protondb_routes.py
│   ├── steamspy_routes.py
│   ├── ollama_routes.py
│   └── suggestions_routes.py
│
├── services/                    # Logique métier
│   ├── __init__.py
│   ├── cache_service.py
│   ├── steam_service.py
│   ├── protondb_service.py
│   ├── steamspy_service.py
│   ├── ollama_service.py
│   └── suggestions_service.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── templates/
│   └── index.html
│
├── cache/                       # Cache auto-généré
│   ├── proton_cache.json
│   └── genres_cache.json
│
└── suggestions/                 # Suggestions sauvegardées
    └── *.json
```
