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
        
        # Améliorer le prompt pour forcer le JSON
        json_instruction = """
IMPORTANT: Tu DOIS répondre UNIQUEMENT avec un tableau JSON contenant EXACTEMENT 5 suggestions.
Format STRICT attendu (exemple):
[
  {"title": "Jeu 1", "reason": "Explication courte"},
  {"title": "Jeu 2", "reason": "Explication courte"},
  {"title": "Jeu 3", "reason": "Explication courte"},
  {"title": "Jeu 4", "reason": "Explication courte"},
  {"title": "Jeu 5", "reason": "Explication courte"}
]

Ne mets RIEN d'autre que ce tableau JSON. Pas de texte avant, pas de texte après.

"""
        full_prompt = json_instruction + prompt
        
        payload = {
            "model": model,
            "prompt": full_prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.7,
                "num_predict": 2000
            }
        }
        
        print(f"🔧 Ollama request to: {endpoint}")
        print(f"🔧 Model: {model}")
        print(f"🔧 Prompt length: {len(prompt)} chars")
        
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
            try:
                response = await client.post(endpoint, json=payload)
                
                print(f"🔧 Ollama response status: {response.status_code}")
                
                if response.status_code != 200:
                    error_text = response.text[:500]  # Limiter la taille
                    print(f"❌ Ollama error response: {error_text}")
                    raise ValueError(f"Erreur Ollama HTTP {response.status_code}: {error_text}")
                
                data = response.json()
                llm_response = data.get("response", "")
                
                print(f"🔧 LLM response length: {len(llm_response)} chars")
                print(f"🔧 LLM response preview: {llm_response[:200]}...")
                
                # Parser le JSON de la réponse
                cleaned = OllamaService._clean_json_response(llm_response)
                
                print(f"🔧 Cleaned response: {cleaned[:200]}...")
                
                suggestions = json.loads(cleaned)
                
                # Si c'est un objet avec une clé contenant le tableau (ex: {"titles": [...]} ou {"suggestions": [...]})
                if isinstance(suggestions, dict):
                    print(f"⚠️ Réponse est un dict, recherche du tableau...")
                    # Chercher une clé qui contient un tableau
                    for key in ['titles', 'suggestions', 'games', 'results', 'items']:
                        if key in suggestions and isinstance(suggestions[key], list):
                            print(f"✅ Tableau trouvé dans la clé '{key}'")
                            suggestions = suggestions[key]
                            break
                    else:
                        # Si aucune clé connue, essayer de convertir l'objet unique en liste
                        print(f"⚠️ Aucune clé connue trouvée, conversion dict en liste")
                        suggestions = [suggestions]
                
                # Valider que c'est bien une liste maintenant
                if not isinstance(suggestions, list):
                    raise ValueError(f"La réponse n'est pas une liste mais: {type(suggestions)}")
                
                print(f"✅ Parsed {len(suggestions)} suggestions")
                return suggestions
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                print(f"❌ Problematic response: {llm_response[:500]}")
                raise ValueError(f"Impossible de parser le JSON: {str(e)}")
            except Exception as e:
                print(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
                raise
    
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
        
        cleaned = cleaned.strip()
        
        # Si ça commence par du texte avant le JSON, essayer de l'extraire
        if not cleaned.startswith('[') and not cleaned.startswith('{'):
            # Chercher le premier [ ou {
            start_bracket = cleaned.find('[')
            start_brace = cleaned.find('{')
            
            if start_bracket != -1:
                cleaned = cleaned[start_bracket:]
            elif start_brace != -1:
                cleaned = cleaned[start_brace:]
        
        return cleaned.strip()