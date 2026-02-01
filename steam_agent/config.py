"""
Configuration centralisée de l'application Steam Deck Agent
"""
import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Configuration Steam API (à surcharger avec config.py local)
try:
    from config_local import STEAM_API_KEY, DEFAULT_STEAM_ID
except ImportError:
    STEAM_API_KEY = os.getenv("STEAM_API_KEY", "")
    DEFAULT_STEAM_ID = os.getenv("DEFAULT_STEAM_ID", "")
    if not STEAM_API_KEY:
        print("AVERTISSEMENT: STEAM_API_KEY non configuré. Créez un fichier config_local.py")

# URLs des APIs externes
STEAM_API_BASE = "https://api.steampowered.com"
PROTONDB_API_BASE = "https://www.protondb.com/api/v1"
STEAMSPY_API_BASE = "https://steamspy.com/api.php"

# Fichiers de cache
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)
PROTON_CACHE_FILE = CACHE_DIR / "proton_cache.json"
GENRES_CACHE_FILE = CACHE_DIR / "genres_cache.json"

# Dossier de sauvegarde des suggestions
SUGGESTIONS_DIR = BASE_DIR / "suggestions"
SUGGESTIONS_DIR.mkdir(exist_ok=True)

# Configuration serveur
HOST = "0.0.0.0"
PORT = 8000

# Configuration Ollama par défaut
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "mistral"
OLLAMA_TIMEOUT = 120.0