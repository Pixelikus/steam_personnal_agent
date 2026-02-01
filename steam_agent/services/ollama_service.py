"""
Service pour interagir avec Ollama (LLM local)
"""
import json
import httpx
from typing import List, Dict
from ..config import OLLAMA_TIMEOUT


class OllamaService:
    """Service pour gérer les interactions avec Ollama"""
    
    @staticmethod
    async def generate(
        url: str, 
        model: str, 
        prompt: str
    ) -> List[Dict[str, str]]:
        """
        Génère une réponse via Ollama
        
        Args:
            url: URL de l'instance Ollama
            model: Nom du modèle à utiliser
            prompt: Prompt à envoyer
            
        Returns:
            Liste de suggestions au format [{"title": "", "reason": ""}]
            
        Raises:
            httpx.TimeoutException: Si la requête timeout
            httpx.ConnectError: Si impossible de se connecter
            ValueError: Si la réponse n'est pas un JSON valide
        """
        endpoint = f"{url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
            response = await client.post(endpoint, json=payload)
            
            if response.status_code != 200:
                raise ValueError(f"Erreur Ollama: {response.text}")
            
            data = response.json()
            llm_response = data.get("response", "")
            
            # Parser le JSON de la réponse
            cleaned = OllamaService._clean_json_response(llm_response)
            suggestions = json.loads(cleaned)
            
            # Valider que c'est bien une liste
            if not isinstance(suggestions, list):
                raise ValueError("La réponse n'est pas une liste")
            
            return suggestions
    
    @staticmethod
    def _clean_json_response(response: str) -> str:
        """
        Nettoie la réponse pour extraire le JSON pur
        
        Args:
            response: Réponse brute du LLM
            
        Returns:
            JSON nettoyé
        """
        cleaned = response.strip()
        
        # Retirer les markdown code blocks
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        return cleaned.strip()