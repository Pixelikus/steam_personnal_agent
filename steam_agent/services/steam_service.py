"""
Service pour interagir avec l'API Steam
"""
import re
import json
import httpx
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from ..config import STEAM_API_BASE, STEAM_API_KEY, DEFAULT_STEAM_ID, CACHE_DIR


class SteamService:
    """Service pour gérer les interactions avec l'API Steam"""
    
    LIBRARY_CACHE_FILE = CACHE_DIR / "ma_librairie.json"
    CACHE_DURATION_HOURS = 24  # Durée de validité du cache
    
    @staticmethod
    async def resolve_steam_id(identifier: str) -> Optional[str]:
        """
        Résout un identifiant Steam (ID numérique ou vanity URL)
        
        Args:
            identifier: ID Steam (17 chiffres) ou vanity URL
            
        Returns:
            Steam ID résolu ou DEFAULT_STEAM_ID
        """
        if not identifier or identifier == "default": 
            return DEFAULT_STEAM_ID
        
        # Si c'est déjà un ID numérique valide
        if re.match(r"^\d{17}$", identifier): 
            return identifier
        
        # Sinon, résoudre via l'API
        url = f"{STEAM_API_BASE}/ISteamUser/ResolveVanityURL/v0001/"
        params = {
            "key": STEAM_API_KEY,
            "vanityurl": identifier
        }
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, params=params)
                data = resp.json()
                return data.get("response", {}).get("steamid", DEFAULT_STEAM_ID)
            except Exception:
                return DEFAULT_STEAM_ID
    
    @staticmethod
    def _load_library_cache(steam_id: str) -> Optional[Dict]:
        """
        Charge la bibliothèque depuis le cache si valide
        
        Args:
            steam_id: ID Steam de l'utilisateur
            
        Returns:
            Bibliothèque depuis le cache ou None si invalide/absent
        """
        if not SteamService.LIBRARY_CACHE_FILE.exists():
            return None
        
        try:
            with open(SteamService.LIBRARY_CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            
            # Vérifier que c'est le bon Steam ID
            if cache_data.get("steam_id") != steam_id:
                print(f"Cache Steam ID différent ({cache_data.get('steam_id')} vs {steam_id})")
                return None
            
            # Vérifier la date du cache
            cache_date = datetime.fromisoformat(cache_data.get("cached_at", "2000-01-01"))
            now = datetime.now()
            
            if now - cache_date > timedelta(hours=SteamService.CACHE_DURATION_HOURS):
                print(f"Cache expiré ({cache_date} > {SteamService.CACHE_DURATION_HOURS}h)")
                return None
            
            print(f"✅ Cache valide trouvé ({len(cache_data.get('games', []))} jeux)")
            return cache_data
            
        except Exception as e:
            print(f"Erreur lecture cache bibliothèque: {e}")
            return None
    
    @staticmethod
    def _save_library_cache(steam_id: str, games: List[Dict]) -> None:
        """
        Sauvegarde la bibliothèque dans le cache
        
        Args:
            steam_id: ID Steam de l'utilisateur
            games: Liste des jeux avec toutes les données enrichies
        """
        try:
            cache_data = {
                "steam_id": steam_id,
                "cached_at": datetime.now().isoformat(),
                "games": games,
                "total": len(games)
            }
            
            with open(SteamService.LIBRARY_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Cache bibliothèque sauvegardé ({len(games)} jeux)")
            
        except Exception as e:
            print(f"Erreur sauvegarde cache bibliothèque: {e}")
    
    @staticmethod
    async def get_owned_games(steam_id: str, force_refresh: bool = False) -> Dict:
        """
        Récupère la bibliothèque de jeux d'un utilisateur Steam
        Utilise le cache si disponible et valide
        
        Args:
            steam_id: ID Steam de l'utilisateur
            force_refresh: Force le rechargement même si cache valide
            
        Returns:
            Dictionnaire contenant la liste des jeux et le total
        """
        # Vérifier le cache d'abord (sauf si force_refresh)
        if not force_refresh:
            cached = SteamService._load_library_cache(steam_id)
            if cached:
                return {
                    "games": cached.get("games", []),
                    "total": cached.get("total", 0),
                    "from_cache": True
                }
        
        # Sinon, requête vers Steam API
        print(f"🌐 Chargement depuis Steam API...")
        url = f"{STEAM_API_BASE}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            "key": STEAM_API_KEY,
            "steamid": steam_id,
            "format": "json",
            "include_appinfo": True
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                data = response.json()
                games = data.get("response", {}).get("games", [])
                
                # Enrichir les données de chaque jeu
                for game in games:
                    game["header_image"] = (
                        f"https://shared.akamai.steamstatic.com/store_item_assets/"
                        f"steam/apps/{game['appid']}/header.jpg"
                    )
                    game["playtime_h"] = round(
                        game.get("playtime_forever", 0) / 60, 1
                    )
                
                return {"games": games, "total": len(games), "from_cache": False}
            
            except Exception as e:
                print(f"Erreur lors de la récupération de la bibliothèque: {e}")
                return {"games": [], "total": 0, "from_cache": False}