"""
Routes pour l'API Ollama
"""
from fastapi import APIRouter, HTTPException
import httpx
import json
from .models import OllamaRequest
from ..services import OllamaService

router = APIRouter(prefix="/api/ollama", tags=["ollama"])


@router.post("/generate")
async def ollama_generate(request: OllamaRequest):
    """
    Génère une réponse via Ollama (LLM local)
    
    Args:
        request: Requête contenant l'URL, le modèle et le prompt
        
    Returns:
        Dictionnaire avec les suggestions générées
        
    Raises:
        HTTPException: En cas d'erreur de connexion, timeout ou parsing
    """
    try:
        suggestions = await OllamaService.generate(
            url=request.url,
            model=request.model,
            prompt=request.prompt
        )
        
        return {"suggestions": suggestions}
        
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Timeout lors de la requête vers Ollama. Le modèle met trop de temps à répondre."
        )
    
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Impossible de se connecter à Ollama sur {request.url}. "
                   f"Vérifiez que Ollama est bien lancé."
        )
    
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Impossible de parser la réponse JSON du LLM: {str(e)}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la requête Ollama: {str(e)}"
        )