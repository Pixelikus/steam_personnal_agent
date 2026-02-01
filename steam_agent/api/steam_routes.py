"""
Routes pour l'API Steam
"""
from fastapi import APIRouter, HTTPException
from ..services import SteamService, ProtonDBService, SteamSpyService

router = APIRouter(prefix="/api/steam", tags=["steam"])


@router.get("/library/{steam_id}")
async def get_steam_library(steam_id: str = None, force_refresh: bool = False):
    """
    Récupère la bibliothèque Steam d'un utilisateur
    Utilise le cache ma_librairie.json si disponible
    
    Args:
        steam_id: ID Steam, vanity URL, ou "default"
        force_refresh: Force le rechargement (ignore le cache)
        
    Returns:
        Dictionnaire avec la liste des jeux enrichis
    """
    try:
        # Résoudre l'ID Steam
        search_id = steam_id if steam_id and steam_id != "undefined" else "default"
        real_id = await SteamService.resolve_steam_id(search_id)
        
        if not real_id:
            raise HTTPException(
                status_code=400, 
                detail="Impossible de résoudre l'ID Steam"
            )
        
        # Récupérer la bibliothèque (avec cache)
        library = await SteamService.get_owned_games(real_id, force_refresh)
        
        # Si c'est depuis le cache, on retourne directement
        if library.get("from_cache"):
            return library
        
        # Sinon, enrichir avec ProtonDB et SteamSpy
        games = library.get("games", [])
        if games:
            appids = [g["appid"] for g in games]
            
            # Services
            protondb_service = ProtonDBService()
            steamspy_service = SteamSpyService()
            
            # Récupérer les données en parallèle
            import asyncio
            proton_data, genres_data = await asyncio.gather(
                protondb_service.get_scores_bulk(appids),
                steamspy_service.get_genres_bulk(appids)
            )
            
            # Enrichir chaque jeu
            for game in games:
                str_id = str(game["appid"])
                game["protondb_score"] = proton_data.get(str_id, "unknown")
                game["genres"] = genres_data.get(str_id, ["Unknown"])
            
            # Sauvegarder dans le cache complet
            SteamService._save_library_cache(real_id, games)
        
        return {"games": games, "total": len(games), "from_cache": False}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération de la bibliothèque: {str(e)}"
        )