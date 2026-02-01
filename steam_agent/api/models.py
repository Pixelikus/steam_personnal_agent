"""
Modèles Pydantic pour la validation des données
"""
from pydantic import BaseModel
from typing import Optional, List


class SuggestionItem(BaseModel):
    """Modèle pour une suggestion de jeu"""
    title: str
    reason: str
    appid: Optional[str] = None


class SaveSuggestionsRequest(BaseModel):
    """Modèle pour la requête de sauvegarde de suggestions"""
    category: str
    suggestions: List[SuggestionItem]


class OllamaRequest(BaseModel):
    """Modèle pour une requête Ollama"""
    url: str
    model: str
    prompt: str