"""
Routes pour l'API ProtonDB
"""
from fastapi import APIRouter, HTTPException
from typing import List
from ..services import ProtonDBService

router = APIRouter(prefix="/api/protondb", tags=["protondb"])
protondb_service = ProtonDBService()


@router.get("/{appid}")
async def get_proton_score(appid: int):
    """
    Récupère le score ProtonDB pour un jeu spécifique
    
    Args:
        appid: ID Steam du jeu
        
    Returns:
        Dictionnaire avec le tier ProtonDB
    """
    try:
        tier = await protondb_service.get_score(appid)
        return {"tier": tier}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur ProtonDB: {str(e)}"
        )


@router.post("/bulk")
async def get_proton_scores_bulk(appids: List[int]):
    """
    Récupère les scores ProtonDB pour plusieurs jeux
    
    Args:
        appids: Liste d'IDs Steam
        
    Returns:
        Dictionnaire {appid: tier}
    """
    try:
        results = await protondb_service.get_scores_bulk(appids)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur ProtonDB bulk: {str(e)}"
        )