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
        endpoint = f"{url}/api/generate"
        
        # Le secret ici est de demander de lister d'abord les noms pour "préparer" l'attention du modèle
        json_instruction = """
Tu es un expert en recommandation de jeux vidéo.
Étape 1: Choisis 5 jeux correspondant à la demande.
Étape 2: Réponds UNIQUEMENT avec un tableau JSON contenant ces 5 jeux.

FORMAT REQUIS:
[
  {"title": "Jeu 1", "reason": "Explication"},
  {"title": "Jeu 2", "reason": "Explication"},
  {"title": "Jeu 3", "reason": "Explication"},
  {"title": "Jeu 4", "reason": "Explication"},
  {"title": "Jeu 5", "reason": "Explication"}
]

INTERDICTION de mettre du texte avant ou après le tableau JSON.
"""
        full_prompt = json_instruction + prompt
        
        # --- DEBUG SYSTÉMATIQUE : PROMPT COMPLET ---
        print("\n" + "="*60)
        print("🚀 DEBUG: FULL PROMPT SENT TO OLLAMA")
        print(full_prompt)
        print("="*60 + "\n")
        
        payload = {
            "model": model,
            "prompt": full_prompt,
            "stream": False,
            # On commente le format strict qui bride le modèle à 1 seul item
            # "format": "json", 
            "options": {
                "temperature": 0.8,
                "num_predict": 2000
            }
        }
        
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
            try:
                response = await client.post(endpoint, json=payload)
                
                if response.status_code != 200:
                    raise ValueError(f"Erreur Ollama HTTP {response.status_code}")
                
                data = response.json()
                llm_response = data.get("response", "")
                
                # --- DEBUG SYSTÉMATIQUE : RETOUR COMPLET ---
                print("\n" + "╔" + "═"*58 + "╗")
                print(f"║ 📥 DEBUG: RAW LLM RESPONSE ({model})")
                print("╠" + "═"*58 + "╣")
                print(llm_response)
                print("╚" + "═"*58 + "╝\n")
                
                # Nettoyage robuste pour extraire le tableau
                cleaned = OllamaService._clean_json_response(llm_response)
                suggestions = json.loads(cleaned)
                
                # Normalisation en liste
                if isinstance(suggestions, dict):
                    for key in ['suggestions', 'titles', 'games', 'items']:
                        if key in suggestions and isinstance(suggestions[key], list):
                            suggestions = suggestions[key]
                            break
                    else:
                        suggestions = [suggestions]
                
                print(f"✅ Succès : {len(suggestions)} suggestions extraites.")
                return suggestions
                
            except Exception as e:
                print(f"❌ Erreur lors de l'extraction : {str(e)}")
                # Retourne une liste vide au lieu de faire crash l'app
                return []
    
    @staticmethod
    def _clean_json_response(response: str) -> str:
        """Nettoyage pour isoler le JSON même si le modèle a ajouté du texte"""
        cleaned = response.strip()
        
        # Supprime les blocs de code Markdown
        if "```" in cleaned:
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0]
            else:
                cleaned = cleaned.split("```")[1].split("```")[0]
        
        cleaned = cleaned.strip()
        
        # Trouve le début du tableau ou de l'objet
        start_idx = cleaned.find('[')
        if start_idx == -1:
            start_idx = cleaned.find('{')
            
        if start_idx != -1:
            cleaned = cleaned[start_idx:]
            
        # Trouve la fin correspondante
        end_idx = cleaned.rfind(']')
        if end_idx == -1:
            end_idx = cleaned.rfind('}')
            
        if end_idx != -1:
            cleaned = cleaned[:end_idx+1]
            
        return cleaned