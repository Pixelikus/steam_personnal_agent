"""
Routes API de l'application Steam Deck Agent
"""
from .steam_routes import router as steam_router
from .protondb_routes import router as protondb_router
from .steamspy_routes import router as steamspy_router
from .ollama_routes import router as ollama_router
from .suggestions_routes import router as suggestions_router

__all__ = [
    "steam_router",
    "protondb_router",
    "steamspy_router",
    "ollama_router",
    "suggestions_router",
]