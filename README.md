# steam_personnal_agent
this interface retrieves your steam library, ask protondb for steamdeck compatibility and steamspy for metadata

steam_agent/
│
├── 📄 main.py                      # Point d'entrée (90 lignes)
├── 📄 config.py                    # Configuration centralisée
├── 📄 config_local.py.example      # Template de configuration
├── 📄 requirements.txt             # Dépendances Python
├── 📄 README.md                    # Documentation complète
├── 📄 .gitignore                   # Fichiers à ignorer
│
├── 📁 api/                         # Routage HTTP (6 fichiers)
│   ├── __init__.py
│   ├── models.py                   # Modèles Pydantic (validation)
│   ├── steam_routes.py             # Routes API Steam
│   ├── protondb_routes.py          # Routes API ProtonDB
│   ├── steamspy_routes.py          # Routes API SteamSpy
│   ├── ollama_routes.py            # Routes LLM local
│   └── suggestions_routes.py       # Routes gestion suggestions
│
├── 📁 services/                    # Logique métier (6 fichiers)
│   ├── __init__.py
│   ├── cache_service.py            # Gestion cache JSON
│   ├── steam_service.py            # Interactions Steam API
│   ├── protondb_service.py         # Interactions ProtonDB
│   ├── steamspy_service.py         # Interactions SteamSpy
│   ├── ollama_service.py           # Interactions Ollama
│   └── suggestions_service.py      # Gestion suggestions
│
├── 📁 static/                      # Assets frontend
│   ├── css/
│   │   └── style.css               # Styles CSS (120 lignes)
│   └── js/
│       └── app.js                  # JavaScript (300 lignes)
│
├── 📁 templates/                   # Templates HTML
│   └── index.html                  # HTML pur (120 lignes)
│
├── 📁 cache/                       # Cache (auto-créé)
│   ├── proton_cache.json
│   └── genres_cache.json
│
└── 📁 suggestions/                 # Suggestions sauvegardées
    └── (fichiers JSON horodatés)
