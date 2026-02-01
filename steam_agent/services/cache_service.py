"""
Service de gestion du cache (ProtonDB et genres)
"""
import json
from pathlib import Path
from typing import Dict, Optional


class CacheService:
    """Service pour gérer les caches JSON"""
    
    def __init__(self, cache_file: Path):
        self.cache_file = cache_file
        self._cache: Dict[str, any] = {}
        self._load_cache()
    
    def _load_cache(self) -> None:
        """Charge le cache depuis le fichier"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except json.JSONDecodeError:
                self._cache = {}
    
    def _save_cache(self) -> None:
        """Sauvegarde le cache dans le fichier"""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, ensure_ascii=False, indent=2)
    
    def get(self, key: str) -> Optional[any]:
        """Récupère une valeur du cache"""
        return self._cache.get(str(key))
    
    def set(self, key: str, value: any) -> None:
        """Définit une valeur dans le cache"""
        self._cache[str(key)] = value
        self._save_cache()
    
    def has(self, key: str) -> bool:
        """Vérifie si une clé existe dans le cache"""
        return str(key) in self._cache
    
    def get_all(self) -> Dict[str, any]:
        """Retourne tout le cache"""
        return self._cache.copy()