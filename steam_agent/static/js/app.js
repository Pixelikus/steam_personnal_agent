/**
 * Steam Deck Agent - JavaScript principal
 * Gestion de la bibliothèque Steam, suggestions et interactions LLM
 */

// Variables globales
let fullLibrary = [];
let protonCache = {};
let genresCache = {};
let currentSuggestions = null;
let currentCategory = null;

/**
 * Charge la bibliothèque Steam d'un utilisateur
 */
async function loadLibrary() {
    const steamId = document.getElementById('steamInput').value.trim() || 'default';
    document.getElementById('status').innerHTML = '⏳ Chargement...';

    try {
        // Récupérer la bibliothèque (avec cache automatique)
        const res = await fetch(`/api/steam/library/${steamId}`);
        const data = await res.json();
        fullLibrary = data.games || [];
        
        // Vérifier si les données sont déjà enrichies (depuis le cache)
        const isEnriched = fullLibrary.length > 0 && 
                          fullLibrary[0].hasOwnProperty('protondb_score') &&
                          fullLibrary[0].hasOwnProperty('genres');
        
        if (isEnriched) {
            // Les données sont déjà complètes (depuis ma_librairie.json)
            console.log('✅ Données enrichies chargées depuis le cache');
            
            // Construire les caches pour l'interface
            protonCache = {};
            genresCache = {};
            fullLibrary.forEach(g => {
                protonCache[g.appid] = g.protondb_score;
                genresCache[g.appid] = g.genres;
            });
            
            // Afficher un message si c'est depuis le cache
            if (data.from_cache) {
                document.getElementById('status').innerHTML = '📦 Cache';
                setTimeout(() => {
                    document.getElementById('status').innerHTML = `✅ ${fullLibrary.length} jeux`;
                }, 1000);
            } else {
                document.getElementById('status').innerHTML = `✅ ${fullLibrary.length} jeux`;
            }
        } else {
            // Les données ne sont pas enrichies, récupérer ProtonDB et SteamSpy
            console.log('🌐 Enrichissement des données...');
            const appids = fullLibrary.map(g => g.appid);
            const [protonRes, genresRes] = await Promise.all([
                fetch('/api/protondb/bulk', { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify(appids) 
                }),
                fetch('/api/steamspy/genres/bulk', { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify(appids) 
                })
            ]);
            
            protonCache = await protonRes.json();
            genresCache = await genresRes.json();
            document.getElementById('status').innerHTML = `✅ ${fullLibrary.length} jeux`;
        }
        
        // Mettre à jour l'interface
        populateGenreFilter();
        renderGames();
        document.getElementById('actionButtons').style.display = 'flex';
        document.getElementById('askAnythingSection').style.display = 'block';
        
    } catch(e) {
        document.getElementById('status').innerHTML = '❌ Erreur';
        console.error('Erreur chargement bibliothèque:', e);
    }
}

/**
 * Remplit le filtre de genres avec tous les genres disponibles
 */
function populateGenreFilter() {
    const allGenres = new Set();
    Object.values(genresCache).forEach(genres => 
        genres.forEach(g => allGenres.add(g))
    );
    
    const sortedGenres = Array.from(allGenres).sort();
    const select = document.getElementById('filterGenre');
    select.innerHTML = '<option value="all">🎮 Tous les genres</option>' + 
        sortedGenres.map(g => `<option value="${g}">${g}</option>`).join('');
}

/**
 * Affiche les jeux en appliquant les filtres et le tri
 */
function renderGames() {
    const container = document.getElementById('results');
    const filter = document.getElementById('filterName').value.toLowerCase();
    const protonFilter = document.getElementById('filterProton').value;
    const genreFilter = document.getElementById('filterGenre').value;
    const sortBy = document.getElementById('sortOrder').value;

    // Filtrage
    let filtered = fullLibrary.filter(g => {
        const matchName = g.name.toLowerCase().includes(filter);
        const matchProton = protonFilter === 'all' || (protonCache[g.appid] === protonFilter);
        let matchGenre = genreFilter === 'all';
        if (!matchGenre && genresCache[g.appid]) {
            matchGenre = genresCache[g.appid].includes(genreFilter);
        }
        return matchName && matchProton && matchGenre;
    });

    // Tri
    if (sortBy === 'playtime') {
        filtered.sort((a, b) => b.playtime_h - a.playtime_h);
    } else {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
    }

    // Affichage
    container.innerHTML = filtered.map(g => {
        const score = protonCache[g.appid] || "unknown";
        const genres = genresCache[g.appid] || [];
        const genreTags = genres.slice(0, 3)
            .map(genre => `<span class="genre-tag">${genre}</span>`)
            .join('');
        
        return `
            <div class="game-card" data-appid="${g.appid}">
                <span class="proton-badge ${score}">${score}</span>
                <img src="${g.header_image}" 
                     onerror="this.src='https://via.placeholder.com/300x140/1a1f3a/00ff88?text=${encodeURIComponent(g.name)}'">
                <div class="game-card-content">
                    <h4>${g.name}</h4>
                    <div class="genre-tags">${genreTags}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px">
                        <span style="color:#00ff88; font-weight:bold">${g.playtime_h}h</span>
                    </div>
                </div>
            </div>`;
    }).join('');
}

/**
 * Toggle l'affichage de la configuration LLM local
 */
function toggleLLMMode() {
    const checkbox = document.getElementById('useLocalLLM');
    const config = document.getElementById('llmConfig');
    config.style.display = checkbox.checked ? 'block' : 'none';
}

/**
 * Génère un prompt pour les suggestions de jeux
 * @param {string} type - Type de suggestion ('new' ou 'backlog')
 */
async function generatePrompt(type) {
    currentCategory = (type === 'new') ? "nouveautes" : "backlog";
    const useLocal = document.getElementById('useLocalLLM').checked;
    
    const simplified = fullLibrary.map(g => ({ 
        title: g.name, 
        playtime: g.playtime_h,
        protonDB_score: protonCache[g.appid] || "unknown",
        genres: genresCache[g.appid] || ["Unknown"]
    }));
    const jsonLib = JSON.stringify(simplified);
    
    let prompt = type === 'new' 
        ? `Voici ma bibliothèque Steam (JSON) : ${jsonLib}\n\nSuggère-moi 5 NOUVEAUX jeux parfaits pour le Steam Deck que je ne possède pas encore. Réponds uniquement avec un tableau JSON strict. Format : [{"title": "Nom du jeu", "appid": "123450", "reason": "Explication"}]`
        : `Voici ma bibliothèque Steam : ${jsonLib}\n\nSuggère-moi 5 jeux que je possède (playtime < 10h) excellents sur Steam Deck. Format JSON uniquement : [{"title": "Nom", "reason": "Pourquoi"}]`;
    
    if (useLocal) {
        await queryLocalLLM(prompt);
    } else {
        document.getElementById('promptTextarea').value = prompt;
        document.getElementById('promptBox').style.display = 'block';
        navigator.clipboard.writeText(prompt);
    }
}

/**
 * Interroge Ollama (LLM local) avec un prompt
 * @param {string} prompt - Le prompt à envoyer
 */
async function queryLocalLLM(prompt) {
    const ollamaUrl = document.getElementById('ollamaUrl').value.trim();
    const model = document.getElementById('ollamaModel').value.trim();
    
    if (!ollamaUrl || !model) {
        alert("Veuillez configurer l'URL Ollama et le modèle");
        return;
    }
    
    const statusDiv = document.getElementById('status');
    statusDiv.innerHTML = '<span class="loading-spinner"></span> LLM en cours...';
    
    try {
        const response = await fetch('/api/ollama/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                url: ollamaUrl,
                model: model,
                prompt: prompt
            })
        });
        
        if (!response.ok) {
            throw new Error(`Erreur ${response.status}`);
        }
        
        const data = await response.json();
        
        // Afficher directement les suggestions
        currentSuggestions = data.suggestions;
        await renderSuggestions(currentSuggestions);
        document.getElementById('saveBtn').style.display = 'block';
        statusDiv.innerHTML = '✅ Suggestions générées !';
        
    } catch(e) {
        statusDiv.innerHTML = '❌ Erreur LLM';
        alert(`Erreur lors de la requête Ollama: ${e.message}\n\nVérifiez que Ollama est bien lancé sur ${ollamaUrl}`);
        console.error(e);
    }
}

/**
 * Gère la fonctionnalité "Ask Anything"
 */
async function askAnything() {
    const question = document.getElementById('askAnythingInput').value.trim();
    if (!question) {
        alert("Veuillez poser une question !");
        return;
    }
    
    currentCategory = "custom";
    const useLocal = document.getElementById('useLocalLLM').checked;
    
    const simplified = fullLibrary.map(g => ({ 
        title: g.name, 
        playtime: g.playtime_h,
        protonDB_score: protonCache[g.appid] || "unknown",
        genres: genresCache[g.appid] || ["Unknown"]
    }));
    const jsonLib = JSON.stringify(simplified);
    
    const prompt = `Voici ma bibliothèque Steam complète (JSON) : ${jsonLib}\n\nQuestion de l'utilisateur : ${question}\n\nRéponds UNIQUEMENT avec un tableau JSON contenant tes suggestions/réponses. Format strict : [{"title": "Nom du jeu", "reason": "Explication détaillée"}]. Si le jeu n'est pas dans la bibliothèque, ajoute "appid": "0". Si c'est un jeu de la bibliothèque, ne mets pas d'appid.`;
    
    if (useLocal) {
        await queryLocalLLM(prompt);
    } else {
        // Mode manuel : copier le prompt et afficher la zone de texte
        document.getElementById('promptTextarea').value = prompt;
        document.getElementById('promptBox').style.display = 'block';
        navigator.clipboard.writeText(prompt);
        alert("Prompt copié ! Collez-le dans votre LLM puis importez la réponse JSON ci-dessous.");
    }
}

/**
 * Importe les suggestions depuis le champ de texte
 */
async function importLLM() {
    try {
        const inputVal = document.getElementById('llmInput').value;
        currentSuggestions = JSON.parse(inputVal);
        await renderSuggestions(currentSuggestions);
        document.getElementById('saveBtn').style.display = 'block';
    } catch(e) { 
        alert("JSON invalide."); 
    }
}

/**
 * Sauvegarde les suggestions actuelles
 */
async function saveCurrentSuggestions() {
    if (!currentSuggestions) return;
    
    try {
        const res = await fetch('/api/suggestions/save', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                category: currentCategory, 
                suggestions: currentSuggestions 
            })
        });
        
        if (res.ok) { 
            alert("Suggestions sauvegardées !"); 
            updateHistoryLists(); 
        }
    } catch (e) { 
        alert("Erreur sauvegarde."); 
    }
}

/**
 * Affiche les suggestions de jeux
 * @param {Array} sugs - Liste des suggestions
 */
async function renderSuggestions(sugs) {
    const container = document.getElementById('results');
    const isNew = (currentCategory === 'nouveautes');
    const isCustom = (currentCategory === 'custom');
    const color = isCustom ? "#fbbf24" : (isNew ? "#6366f1" : "#f59e0b");
    const title = isCustom ? "Réponse personnalisée" : currentCategory.toUpperCase();
    
    container.innerHTML = `<h2 style="grid-column: 1/-1; color: ${color}; margin-bottom: 20px;">Suggestions : ${title}</h2>`;
    
    for (const s of sugs) {
        const owned = fullLibrary.find(g => g.name.toLowerCase() === s.title.toLowerCase());
        const appId = owned ? owned.appid : (s.appid || 0);
        let score = owned ? (protonCache[owned.appid] || "unknown") : "unknown";
        
        container.innerHTML += `
            <div class="game-card" style="border-color: ${color}">
                <span class="proton-badge ${score}">${score}</span>
                <img src="https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/${appId}/header.jpg" 
                     onerror="this.src='https://via.placeholder.com/300x140/1a1f3a/6366f1?text=${encodeURIComponent(s.title)}'">
                <div class="game-card-content">
                    <h4 style="color: #00ff88">${s.title}</h4>
                    <div class="genre-tags"></div>
                    <p style="font-size: 0.85em; margin-top: 10px; opacity: 0.8;">${s.reason}</p>
                </div>
            </div>`;
    }
}

/**
 * Met à jour les listes d'historique de suggestions
 */
async function updateHistoryLists() {
    const categories = ['nouveautes', 'backlog'];
    
    for (const cat of categories) {
        try {
            const res = await fetch(`/api/suggestions/list/${cat}`);
            const files = await res.json();
            const select = document.getElementById(`select-${cat}`);
            
            select.innerHTML = files.length === 0 
                ? '<option value="">Aucune sauvegarde</option>' 
                : files.map(f => `<option value="${f.filename}">${f.date_display}</option>`).join('');
        } catch (e) { 
            console.error("Erreur historique", e); 
        }
    }
}

/**
 * Charge des suggestions depuis l'historique
 * @param {string} cat - Catégorie (nouveautes ou backlog)
 */
async function loadFromHistory(cat) {
    const filename = document.getElementById(`select-${cat}`).value;
    if (!filename) return;
    
    try {
        const res = await fetch(`/api/suggestions/load/${filename}`);
        currentSuggestions = await res.json();
        currentCategory = cat;
        renderSuggestions(currentSuggestions);
        document.getElementById('saveBtn').style.display = 'none';
    } catch (e) { 
        alert("Erreur chargement"); 
    }
}

/**
 * Nettoie le champ d'import
 */
function clearImport() {
    document.getElementById('llmInput').value = "";
    document.getElementById('saveBtn').style.display = 'none';
}

/**
 * Vide les suggestions et réinitialise les filtres
 */
function clearSuggestions() {
    clearImport();
    document.getElementById('promptBox').style.display = 'none';
    document.getElementById('filterProton').value = "all";
    document.getElementById('filterGenre').value = "all";
    renderGames();
}

/**
 * Exporte la bibliothèque en JSON
 */
function exportJSON() {
    const dataToExport = fullLibrary.map(g => ({
        ...g,
        protondb_score: protonCache[g.appid] || "unknown",
        genres: genresCache[g.appid] || ["Unknown"]
    }));
    
    const blob = new Blob([JSON.stringify(dataToExport, null, 2)], {type: 'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = "ma_librairie_deck.json";
    a.click();
}

// Initialisation au chargement de la page
window.onload = () => { 
    loadLibrary(); 
    updateHistoryLists(); 
};