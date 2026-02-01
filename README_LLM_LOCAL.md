# Steam Deck Agent - Guide d'utilisation du LLM Local

## Nouveautés

Votre application Steam Deck Agent dispose désormais d'une option **LLM Local** qui permet d'interroger directement un modèle de langage local via Ollama, sans avoir à copier-coller le JSON manuellement.

## Fonctionnalités ajoutées

### 1. Case à cocher "LLM local"
- Une nouvelle option apparaît dans l'interface : **🤖 Utiliser LLM local (Ollama)**
- Lorsqu'elle est cochée, elle affiche les paramètres de configuration Ollama

### 2. Configuration Ollama
Deux champs de configuration sont disponibles :
- **URL Ollama** : Par défaut `http://localhost:11434`
- **Modèle** : Par défaut `llama3.2` (vous pouvez utiliser `mistral`, `llama2`, `codellama`, etc.)

### 3. Fonctionnement
Lorsque le mode LLM local est activé :
1. Vous cliquez sur "🆕 Nouveaux jeux" ou "🎮 Jeux déjà à jouer"
2. L'application envoie automatiquement la requête à votre Ollama local
3. Les suggestions s'affichent directement dans l'interface
4. Vous pouvez les sauvegarder comme avant

## Installation et configuration d'Ollama

### Étape 1 : Installer Ollama

**Linux :**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS :**
```bash
brew install ollama
```

**Windows :**
Téléchargez l'installateur sur https://ollama.com/download

### Étape 2 : Lancer Ollama

```bash
ollama serve
```

Par défaut, Ollama démarre sur `http://localhost:11434`

### Étape 3 : Télécharger un modèle

```bash
# Modèle recommandé pour cette tâche (léger et efficace)
ollama pull llama3.2

# Alternatives
ollama pull mistral
ollama pull llama2
ollama pull codellama
```

### Étape 4 : Tester

```bash
ollama run llama3.2
```

## Utilisation dans l'application

1. **Lancez votre serveur FastAPI** :
   ```bash
   python main.py
   ```

2. **Accédez à l'interface** : `http://localhost:8000`

3. **Chargez votre bibliothèque Steam**

4. **Cochez "🤖 Utiliser LLM local (Ollama)"**

5. **Vérifiez la configuration** :
   - URL : `http://localhost:11434`
   - Modèle : `llama3.2` (ou votre modèle préféré)

6. **Cliquez sur un des boutons de suggestion** :
   - 🆕 Nouveaux jeux
   - 🎮 Jeux déjà à jouer

7. **Attendez la génération** (un spinner s'affiche)

8. **Les suggestions apparaissent automatiquement !**

9. **Sauvegardez-les** avec le bouton "SAUVEGARDER"

## Modèles recommandés

| Modèle | Taille | Performance | Recommandation |
|--------|--------|-------------|----------------|
| `llama3.2` | ~2GB | Rapide | ⭐ Recommandé pour usage quotidien |
| `mistral` | ~4GB | Très bon | ⭐ Excellent équilibre |
| `llama2` | ~4GB | Bon | Alternative stable |
| `llama3.1` | ~5GB | Excellent | Si vous avez la RAM |
| `codellama` | ~4GB | Spécialisé code | Pour suggestions techniques |

## Avantages du mode LLM local

✅ **Pas de copier-coller** : Tout est automatique
✅ **Privé** : Vos données restent sur votre machine
✅ **Gratuit** : Pas de coût d'API
✅ **Rapide** : Réponse en quelques secondes
✅ **Personnalisable** : Choisissez votre modèle préféré
✅ **Hors ligne** : Fonctionne sans internet (après téléchargement du modèle)

## Dépannage

### Erreur de connexion
**Problème** : `Impossible de se connecter à Ollama`

**Solutions** :
1. Vérifiez qu'Ollama est lancé : `ollama serve`
2. Vérifiez l'URL dans la config (par défaut : `http://localhost:11434`)
3. Testez manuellement : `curl http://localhost:11434/api/version`

### Timeout
**Problème** : `Timeout lors de la requête`

**Solutions** :
1. Utilisez un modèle plus léger (ex: `llama3.2` au lieu de `llama3.1`)
2. Réduisez la taille de votre bibliothèque Steam (filtrez avant)
3. Augmentez le timeout dans `main.py` (ligne avec `timeout=120.0`)

### Réponse invalide
**Problème** : `Impossible de parser la réponse JSON`

**Solutions** :
1. Le modèle n'a peut-être pas respecté le format JSON
2. Essayez un autre modèle (Mistral est généralement très bon pour du JSON)
3. Regardez les logs du serveur FastAPI pour voir la réponse brute

### Modèle non trouvé
**Problème** : `Model not found`

**Solution** :
```bash
ollama pull llama3.2
```

## Comparaison des modes

| Fonctionnalité | Mode Manuel | Mode LLM Local |
|----------------|-------------|----------------|
| Copier-coller | ✅ Requis | ❌ Automatique |
| Internet requis | ✅ Oui (pour le LLM externe) | ❌ Non |
| Coût | Variable selon LLM | ✅ Gratuit |
| Vitesse | Dépend du LLM externe | ⚡ Rapide (local) |
| Confidentialité | Données envoyées | ✅ 100% local |
| Configuration | Aucune | Installation Ollama |

## Exemple de workflow complet

```bash
# 1. Installer et lancer Ollama
ollama serve

# 2. Dans un autre terminal, télécharger le modèle
ollama pull llama3.2

# 3. Lancer votre serveur
python main.py

# 4. Ouvrir le navigateur
# http://localhost:8000

# 5. Dans l'interface :
#    - Charger la bibliothèque Steam
#    - Cocher "LLM local"
#    - Cliquer sur "Nouveaux jeux"
#    - Attendre les suggestions
#    - Sauvegarder !
```

## Architecture technique

### Nouveau endpoint FastAPI
```python
@app.post("/api/ollama/generate")
async def ollama_generate(request: OllamaRequest):
    # Envoie la requête à Ollama
    # Parse la réponse JSON
    # Retourne les suggestions
```

### Frontend JavaScript
```javascript
async function queryLocalLLM(prompt) {
    // Appelle l'endpoint /api/ollama/generate
    // Affiche le spinner
    // Récupère et affiche les suggestions
}
```

## Notes importantes

1. **Premier lancement** : Le premier appel peut être lent (chargement du modèle en mémoire)
2. **Mémoire RAM** : Assurez-vous d'avoir assez de RAM pour le modèle (2-8GB selon le modèle)
3. **Format JSON** : Les modèles récents (Llama 3.2, Mistral) sont très bons pour générer du JSON valide
4. **Bibliothèque volumineuse** : Si vous avez beaucoup de jeux (>500), le prompt peut être long. Filtrez d'abord !

## Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs du serveur FastAPI
2. Vérifiez les logs d'Ollama : `ollama logs`
3. Testez Ollama directement : `ollama run llama3.2`

Bon gaming ! 🎮
