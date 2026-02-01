"""
Routes pour la gestion des suggestions
"""
from fastapi import APIRouter, HTTPException
from .models import SaveSuggestionsRequest
from ..services import SuggestionsService

router = APIRouter(prefix="/api/suggestions", tags=["suggestions"])


@router.post("/save")
async def save_suggestions(request: SaveSuggestionsRequest):
    """
    Sauvegarde des suggestions dans un fichier JSON avec timestamp
    
    Args:
        request: Requête contenant la catégorie et les suggestions
        
    Returns:
        Dictionnaire avec le succès et le nom du fichier
    """
    try:
        # Convertir les suggestions en dict
        suggestions_data = [s.dict() for s in request.suggestions]
        
        # Sauvegarder
        filename = SuggestionsService.save(
            category=request.category,
            suggestions=suggestions_data
        )
        
        return {"success": True, "filename": filename}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur sauvegarde: {str(e)}"
        )


@router.get("/list/{category}")
async def list_suggestions_by_category(category: str):
    """
    Liste les fichiers de suggestions filtrés par catégorie et triés par date
    
    Args:
        category: Catégorie à lister (nouveautes, backlog, custom)
        
    Returns:
        Liste de fichiers avec métadonnées
    """
    try:
        files = SuggestionsService.list_by_category(category)
        return files
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur listage: {str(e)}"
        )


@router.get("/load/{filename}")
async def load_suggestion_file(filename: str):
    """
    Charge un fichier de suggestions spécifique
    
    Args:
        filename: Nom du fichier à charger
        
    Returns:
        Liste de suggestions
    """
    try:
        suggestions = SuggestionsService.load(filename)
        return suggestions
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Fichier non trouvé"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur chargement: {str(e)}"
        )