"""
Service pour interagir avec l'API ProtonDB
"""
import httpx
from typing import List, Dict
from .cache_service import CacheService
from ..config import PROTONDB_API_BASE, PROTON_CACHE_FILE


class ProtonDBService:
    """Service pour gérer les interactions avec ProtonDB"""
    
    def __init__(self):
        self.cache = CacheService(PROTON_CACHE_FILE)
    
    async def get_score(self, appid: int) -> str:
        """
        Récupère le score ProtonDB pour un jeu
        
        Args:
            appid: ID Steam du jeu
            
        Returns:
            Tier ProtonDB (platinum, gold, silver, bronze, borked, unknown)
        """
        # Vérifier le cache
        if self.cache.has(appid):
            return self.cache.get(appid)
        
        # Requête vers ProtonDB
        url = f"{PROTONDB_API_BASE}/reports/summaries/{appid}.json"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    tier = response.json().get("tier", "unknown")
                    self.cache.set(appid, tier)
                    return tier
            except Exception as e:
                print(f"Erreur ProtonDB pour {appid}: {e}")
        
        return "unknown"
    
    async def get_scores_bulk(self, appids: List[int]) -> Dict[str, str]:
        """
        Récupère les scores ProtonDB pour plusieurs jeux
        
        Args:
            appids: Liste d'IDs Steam
            
        Returns:
            Dictionnaire {appid: tier}
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
                        url = f"{PROTONDB_API_BASE}/reports/summaries/{appid}.json"
                        resp = await client.get(url, timeout=5.0)
                        tier = (
                            resp.json().get("tier", "unknown") 
                            if resp.status_code == 200 
                            else "unknown"
                        )
                        self.cache.set(str_id, tier)
                        results[str_id] = tier
                    except Exception:
                        results[str_id] = "unknown"
        
        return results