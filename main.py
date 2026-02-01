"""
Application principale Steam Deck Agent
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from steam_agent.config import STATIC_DIR, TEMPLATES_DIR, HOST, PORT
from steam_agent.api import (
    steam_router,
    protondb_router,
    steamspy_router,
    ollama_router,
    suggestions_router,
)

# Créer l'application FastAPI
app = FastAPI(
    title="Steam Deck Agent",
    description="Assistant intelligent pour votre bibliothèque Steam",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Montage du dossier static
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Enregistrement des routers
app.include_router(steam_router)
app.include_router(protondb_router)
app.include_router(steamspy_router)
app.include_router(ollama_router)
app.include_router(suggestions_router)


@app.get("/")
async def read_index():
    """Page d'accueil - retourne index.html"""
    index_path = TEMPLATES_DIR / "index.html"
    return FileResponse(str(index_path))


@app.get("/health")
async def health_check():
    """Endpoint de santé pour vérifier que l'API fonctionne"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "service": "Steam Deck Agent"
    }


if __name__ == "__main__":
    import uvicorn
    
    print(f"""
╔═══════════════════════════════════════════════╗
║     🎮 Steam Deck Agent v2.0.0 🎮            ║
╠═══════════════════════════════════════════════╣
║  Serveur démarré sur http://{HOST}:{PORT}     ║
║                                               ║
║  📚 Documentation API:                        ║
║     http://{HOST}:{PORT}/docs                 ║
║                                               ║
║  ❤️  Santé du serveur:                        ║
║     http://{HOST}:{PORT}/health               ║
╚═══════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info"
    )