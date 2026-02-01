# 🚀 Guide d'installation rapide

## Installation en 3 minutes

### Étape 1: Télécharger et extraire
Extrayez tous les fichiers dans un dossier de votre choix.

### Étape 2: Rendre votre profil Steam public

**C'est la seule configuration Steam nécessaire !**

1. Ouvrez Steam
2. Profil → Modifier le profil → Paramètres de confidentialité
3. Rendez **PUBLIC** :
   - Détails du profil
   - **Bibliothèque de jeux** (très important !)
   - Inventaire

### Étape 3: Trouver votre Steam ID ou pseudo

**Option 1 - Utiliser votre pseudo personnalisé (recommandé)**
- Si vous avez configuré un pseudo Steam (ex: "johndoe")
- Vous pouvez l'utiliser directement !

**Option 2 - Utiliser votre Steam ID numérique**
- URL de profil: `steamcommunity.com/profiles/XXXXXXXX`
- Le nombre `XXXXXXXX` est votre Steam ID

**OU** utilisez https://steamid.io avec votre pseudo

### Étape 4: Obtenir votre clé API Anthropic

1. Créez un compte sur: https://console.anthropic.com
2. Créez une clé API
3. Copiez la clé (commence par `sk-ant-`)

### Étape 5: Configurer la clé Anthropic

Ouvrez `static/index.html` avec un éditeur de texte.
Trouvez ligne ~580:
```javascript
const ANTHROPIC_API_KEY = 'VOTRE_CLE_API_ANTHROPIC';
```
Remplacez par votre vraie clé.

### Étape 6: Installer Python (si pas déjà fait)

#### Windows
1. Téléchargez: https://www.python.org/downloads/
2. **IMPORTANT**: Cochez "Add Python to PATH"
3. Installez

#### Linux
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Mac
```bash
# Avec Homebrew
brew install python3
```

### Étape 7: Lancer l'application

#### Windows
Double-cliquez sur `start.bat`

#### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

#### Ou manuellement
```bash
# Créer environnement virtuel
python -m venv venv

# Activer (Windows)
venv\Scripts\activate

# Activer (Linux/Mac)
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt

# Lancer
python main.py
```

### Étape 8: Utiliser l'application

1. Ouvrez votre navigateur
2. Allez sur: http://127.0.0.1:8000
3. Entrez votre Steam ID ou pseudo
4. Cliquez "Sauvegarder"
5. Cliquez "Charger ma bibliothèque"
6. Recherchez des jeux !

## ⚠️ Problèmes courants

### "Python n'est pas reconnu"
- Réinstallez Python en cochant "Add to PATH"
- Ou utilisez `python3` au lieu de `python`

### "Profil Steam privé"
1. Steam → Paramètres → Confidentialité
2. Profil: **Public**
3. Bibliothèque de jeux: **Public** (crucial !)

### "Profil Steam non trouvé"
- Vérifiez l'orthographe de votre Steam ID ou pseudo
- Essayez d'utiliser votre Steam ID numérique (17 chiffres)
- Vérifiez sur https://steamid.io

## 🎮 C'est prêt !

Vous pouvez maintenant:
- ✅ Voir votre bibliothèque Steam automatiquement (sans clé API !)
- ✅ Rechercher les meilleurs jeux Steam Deck
- ✅ Suivre les promotions
- ✅ Filtrer par compatibilité

**Bon gaming !** 🎮
