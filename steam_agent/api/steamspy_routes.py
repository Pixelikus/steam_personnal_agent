"""
Routes pour l'API SteamSpy
"""
from fastapi import APIRouter, HTTPException
from typing import List
from ..services import SteamSpyService

router = APIRouter(prefix="/api/steamspy", tags=["steamspy"])
steamspy_service = SteamSpyService()


@router.get("/genres/{appid}")
async def get_game_genres(appid: int):
    """
    Récupère les genres d'un jeu via SteamSpy
    
    Args:
        appid: ID Steam du jeu
        
    Returns:
        Dictionnaire avec la liste des genres
    """
    try:
        genres = await steamspy_service.get_genres(appid)
        return {"genres": genres}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur SteamSpy: {str(e)}"
        )


@router.post("/genres/bulk")
async def get_genres_bulk(appids: List[int]):
    """
    Récupère les genres pour plusieurs jeux
    
    Args:
        appids: Liste d'IDs Steam
        
    Returns:
        Dictionnaire {appid: [genres]}
    """
    try:
        results = await steamspy_service.get_genres_bulk(appids)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur SteamSpy bulk: {str(e)}"
        )