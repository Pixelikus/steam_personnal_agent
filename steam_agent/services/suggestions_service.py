"""
Service pour gérer les suggestions (sauvegarde et chargement)
"""
import json
import glob
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from ..config import SUGGESTIONS_DIR


class SuggestionsService:
    """Service pour gérer la sauvegarde et le chargement des suggestions"""
    
    @staticmethod
    def save(category: str, suggestions: List[Dict]) -> str:
        """
        Sauvegarde des suggestions dans un fichier JSON avec timestamp
        
        Args:
            category: Catégorie (nouveautes, backlog, custom)
            suggestions: Liste de suggestions
            
        Returns:
            Nom du fichier créé
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{category}_{timestamp}.json"
        filepath = SUGGESTIONS_DIR / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(suggestions, f, ensure_ascii=False, indent=2)
        
        return filename
    
    @staticmethod
    def list_by_category(category: str) -> List[Dict]:
        """
        Liste les fichiers de suggestions pour une catégorie
        
        Args:
            category: Catégorie à lister
            
        Returns:
            Liste de fichiers avec métadonnées [{filename, date_display, timestamp}]
        """
        pattern = str(SUGGESTIONS_DIR / f"{category}_*.json")
        files = glob.glob(pattern)
        
        result = []
        for filepath in files:
            filename = Path(filepath).name
            # Format attendu : categorie_YYYYMMDD-HHMMSS.json
            parts = filename.replace(".json", "").split("_")
            
            if len(parts) >= 2:
                timestamp_str = parts[1]
                try:
                    dt = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
                    result.append({
                        "filename": filename,
                        "date_display": dt.strftime("%d/%m/%Y à %H:%M"),
                        "timestamp": dt.isoformat()
                    })
                except ValueError:
                    continue
        
        # Tri du plus récent au plus ancien
        result.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return result
    
    @staticmethod
    def load(filename: str) -> List[Dict]:
        """
        Charge un fichier de suggestions
        
        Args:
            filename: Nom du fichier à charger
            
        Returns:
            Liste de suggestions
            
        Raises:
            ValueError: Si le nom de fichier est invalide
            FileNotFoundError: Si le fichier n'existe pas
        """
        # Sécurité : vérifier le nom de fichier
        if ".." in filename or "/" in filename or "\\" in filename:
            raise ValueError("Nom de fichier invalide")
        
        filepath = SUGGESTIONS_DIR / filename
        
        if not filepath.exists():
            raise FileNotFoundError("Fichier non trouvé")
        
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)