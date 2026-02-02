"""
Service pour interagir avec l'API SteamSpy
"""
import httpx
from typing import List, Dict
from .cache_service import CacheService
from ..config import STEAMSPY_API_BASE, GENRES_CACHE_FILE


class SteamSpyService:
    """Service pour gérer les interactions avec SteamSpy"""
    
    def __init__(self):
        self.cache = CacheService(GENRES_CACHE_FILE)
    
    async def get_genres(self, appid: int) -> List[str]:
        """
        Récupère les genres d'un jeu via SteamSpy
        
        Args:
            appid: ID Steam du jeu
            
        Returns:
            Liste des genres
        """
        # Vérifier le cache
        if self.cache.has(appid):
            return self.cache.get(appid)
        
        # Requête vers SteamSpy
        params = {
            "request": "appdetails",
            "appid": appid
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(STEAMSPY_API_BASE, params=params, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    genre_str = data.get("genre", "Unknown")
                    genres = (
                        [g.strip() for g in genre_str.split(",")] 
                        if genre_str 
                        else ["Unknown"]
                    )
                    self.cache.set(appid, genres)
                    return genres
            except Exception as e:
                print(f"Erreur SteamSpy pour {appid}: {e}")
        
        return ["Unknown"]
    
    async def get_genres_bulk(self, appids: List[int]) -> Dict[str, List[str]]:
        """
        Récupère les genres pour plusieurs jeux
        
        Args:
            appids: Liste d'IDs Steam
            
        Returns:
            Dictionnaire {appid: [genres]}
        """
        results = {}
        
        async with httpx.AsyncClient() as client:
            for appid in appids:
                str_id = str(appid)
                
                # Utiliser le cache si disponible
                if self.cache.has(str_id):
                    results[str_id] = self.cache.get(str_id)
                else:
                    # Sinon, requête API
                    try:
                        params = {"request": "appdetails", "appid": appid}
                        resp = await client.get(
                            STEAMSPY_API_BASE, 
                            params=params, 
                            timeout=10.0
                        )
                        
                        if resp.status_code == 200:
                            genre_str = resp.json().get("genre", "Unknown")
                            genres = (
                                [g.strip() for g in genre_str.split(",")] 
                                if genre_str 
                                else ["Unknown"]
                            )
                            self.cache.set(str_id, genres)
                            results[str_id] = genres
                    except Exception:
                        results[str_id] = ["Unknown"]
        
        return results