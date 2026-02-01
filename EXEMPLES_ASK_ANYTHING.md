# Exemples de Questions "Ask Anything" - Steam Deck Agent

## 📖 Guide pratique avec exemples réels

Ce document contient des exemples concrets de questions que vous pouvez poser et les réponses attendues.

---

## 🎮 EXEMPLE 1 : Analyse simple

### Question
```
Quel est mon jeu le plus joué et pourquoi devrais-je essayer un jeu similaire ?
```

### Réponse JSON attendue
```json
[
  {
    "title": "Elden Ring",
    "reason": "C'est votre jeu le plus joué avec 180 heures. Vu votre investissement dans les Souls-like, vous devriez essayer Lies of P qui est dans votre bibliothèque avec seulement 2h de jeu. C'est un excellent Souls-like avec des mécaniques similaires mais dans un univers steampunk unique."
  },
  {
    "title": "Lies of P",
    "reason": "Vous avez seulement 2h dessus mais c'est un Souls-like de qualité AAA. Vu vos 180h sur Elden Ring, vous allez adorer le combat technique et la difficulté bien dosée. Score Platinum ProtonDB."
  }
]
```

### Affichage dans l'interface
- **Titre** : "Réponse personnalisée" (en orange/doré)
- **Carte 1** : Elden Ring avec explication
- **Carte 2** : Lies of P avec explication
- **Badges ProtonDB** affichés si disponibles

---

## 🔍 EXEMPLE 2 : Découverte de genre

### Question
```
Trouve-moi des roguelikes dans ma bibliothèque que j'ai ignorés mais qui ont un excellent score ProtonDB
```

### Réponse JSON attendue
```json
[
  {
    "title": "Hades",
    "reason": "Score Platinum ProtonDB, 2h de jeu seulement. C'est LE roguelike de référence : combat fluide, progression permanente, narration exceptionnelle. Parfait sur Steam Deck avec des sessions de 20-30min."
  },
  {
    "title": "Dead Cells",
    "reason": "Score Platinum, 1h de jeu. Roguelike/Metroidvania addictif. Combat ultra-responsive, parfait pour le Steam Deck. Vous l'avez à peine lancé mais c'est une perle."
  },
  {
    "title": "Slay the Spire",
    "reason": "Score Gold, 0.5h de jeu. Le deck-building roguelike par excellence. Stratégie pure, rejouabilité infinie. Idéal pour les sessions courtes."
  },
  {
    "title": "Risk of Rain 2",
    "reason": "Score Platinum, 3h de jeu. Roguelike 3D action-packed. Multijoueur possible, progression satisfaisante, excellent sur Steam Deck."
  },
  {
    "title": "Enter the Gungeon",
    "reason": "Score Gold, jamais lancé. Bullet hell roguelike avec des tonnes d'armes créatives. Contrôles parfaits pour le Steam Deck."
  }
]
```

---

## 🎯 EXEMPLE 3 : Recommandation personnalisée

### Question
```
J'ai adoré Hollow Knight (100h) et Celeste (80h). Que me conseilles-tu dans ma bibliothèque ?
```

### Réponse JSON attendue
```json
[
  {
    "title": "Ori and the Will of the Wisps",
    "reason": "Vous avez 5h dessus mais c'est injuste pour ce chef-d'œuvre. Comme Hollow Knight, c'est un metroidvania avec une exploration magnifique, des boss épiques et une OST incroyable. Plateforme précise comme Celeste. Score Platinum ProtonDB."
  },
  {
    "title": "Blasphemous",
    "reason": "Metroidvania sombre avec combat technique. 8h de jeu mais il mérite beaucoup plus. Si vous avez aimé l'atmosphère de Hollow Knight et la difficulté de Celeste, c'est parfait."
  },
  {
    "title": "Shovel Knight",
    "reason": "Plateforme rétro exigeante comme Celeste. 12h de jeu mais vous pouvez aller beaucoup plus loin avec tous les DLC. Contrôles ultra-précis, parfait sur Steam Deck."
  },
  {
    "title": "Gris",
    "reason": "Jamais lancé, mais si vous avez aimé l'aspect artistique de Hollow Knight et Celeste, c'est une expérience visuelle magnifique. Plateforme contemplative, 3-4h pour finir."
  },
  {
    "title": "Salt and Sanctuary",
    "reason": "2h de jeu. Metroidvania + Souls-like 2D. Combat technique et exploration comme Hollow Knight mais avec des mécaniques RPG plus poussées."
  }
]
```

---

## 📊 EXEMPLE 4 : Analyse de backlog

### Question
```
Liste-moi mes jeux avec moins de 1h de jeu qui ont un score Gold ou Platinum sur ProtonDB et explique pourquoi je leur ai pas donné leur chance
```

### Réponse JSON attendue
```json
[
  {
    "title": "Hades",
    "reason": "0.5h de jeu, Score Platinum. Vous avez probablement arrêté après la première run qui est difficile. Mais c'est normal ! Le jeu devient addictif quand vous comprenez la progression permanente. Chaque mort vous rend plus fort."
  },
  {
    "title": "Vampire Survivors",
    "reason": "0.2h de jeu, Score Platinum. Vous avez peut-être trouvé ça simpliste au début, mais c'est le jeu parfait pour le Steam Deck : sessions de 15-30min ultra addictives. Essayez 2-3 runs et vous ne pourrez plus arrêter."
  },
  {
    "title": "Stardew Valley",
    "reason": "0.8h de jeu, Score Platinum. Le début peut sembler lent, mais c'est un jeu qui se bonifie avec le temps. Parfait pour des sessions détente sur Steam Deck. Donnez-lui 5h et vous serez accro."
  },
  {
    "title": "Inscryption",
    "reason": "0.3h de jeu, Score Gold. Le jeu démarre lentement mais devient WTF rapidement. Deck-building + meta-narrative incroyable. Vous avez arrêté trop tôt, continuez jusqu'au premier twist !"
  },
  {
    "title": "Loop Hero",
    "reason": "0.6h de jeu, Score Platinum. Concept unique qui prend 2-3h pour cliquer. C'est un idle-game stratégique parfait pour multitasker sur Steam Deck."
  }
]
```

---

## 🏆 EXEMPLE 5 : Optimisation Steam Deck

### Question
```
Montre-moi mes meilleurs jeux multijoueurs avec un score Platinum ProtonDB parfaits pour une session de 2h
```

### Réponse JSON attendue
```json
[
  {
    "title": "Deep Rock Galactic",
    "reason": "Score Platinum, 45h de jeu. Co-op PvE parfait : sessions de 20-30min, 4 joueurs, classes variées. Excellent sur Steam Deck en multijoueur local ou online."
  },
  {
    "title": "Risk of Rain 2",
    "reason": "Score Platinum, 3h de jeu. Co-op jusqu'à 4 joueurs, runs de 30-60min. Parfait pour 2h de jeu avec des potes. Chaos satisfaisant."
  },
  {
    "title": "Overcooked 2",
    "reason": "Score Platinum, 8h de jeu. Co-op chaotique local ou online. Sessions courtes de 10-15min par niveau. Fun garanti avec 2-4 joueurs."
  },
  {
    "title": "Among Us",
    "reason": "Score Platinum, jamais lancé. Parties de 10-15min, 4-10 joueurs. Parfait pour des sessions sociales rapides sur Steam Deck."
  },
  {
    "title": "Left 4 Dead 2",
    "reason": "Score Platinum, 120h (classique !). Co-op 4 joueurs, campagnes de 30-60min. Toujours aussi fun, contrôles parfaits sur Steam Deck."
  }
]
```

---

## 🌟 EXEMPLE 6 : Découverte de perles cachées

### Question
```
Trouve-moi des jeux indépendants sous-estimés dans ma bibliothèque que personne ne connaît mais qui sont géniaux
```

### Réponse JSON attendue
```json
[
  {
    "title": "Outer Wilds",
    "reason": "2h de jeu, Score Gold. CE JEUX EST UN CHEF-D'ŒUVRE méconnu. Exploration spatiale + puzzle temporel + mystère. Ne lisez RIEN sur internet, juste jouez. Top 10 des jeux de la décennie pour beaucoup."
  },
  {
    "title": "A Short Hike",
    "reason": "Jamais lancé, Score Platinum. Jeu de 1-2h absolument charmant. Exploration relaxante, pixel art magnifique, OST parfaite. Expérience zen parfaite pour le Steam Deck."
  },
  {
    "title": "Disco Elysium",
    "reason": "15h de jeu. RPG narratif unique, zéro combat, 100% dialogues et choix. Écriture exceptionnelle. Beaucoup l'abandonnent au début car c'est dense, mais c'est un chef-d'œuvre littéraire."
  },
  {
    "title": "Return of the Obra Dinn",
    "reason": "3h de jeu, Score Gold. Puzzle game d'enquête unique. Graphismes 1-bit, gameplay original, mystère captivant. Lucas Pope (Papers Please) au sommet."
  },
  {
    "title": "Chicory: A Colorful Tale",
    "reason": "0.5h de jeu, Score Platinum. Zelda-like où vous peignez le monde. Histoire touchante, gameplay créatif, OST de Lena Raine. Caché mais magnifique."
  }
]
```

---

## 🎲 EXEMPLE 7 : Session rapide

### Question
```
Je n'ai que 30 minutes, suggère-moi des jeux parfaits pour une session courte avec un excellent gameplay loop
```

### Réponse JSON attendue
```json
[
  {
    "title": "Vampire Survivors",
    "reason": "0.2h de jeu, Score Platinum. LA référence pour les sessions courtes. Une run = 15-30min. Gameplay loop hypnotique : tue, level up, deviens OP, recommence. 3€, des centaines d'heures de contenu."
  },
  {
    "title": "Brotato",
    "reason": "5h de jeu, Score Gold. Comme Vampire Survivors mais avec plus de build diversity. Runs de 20min max. Parfait pour le Steam Deck."
  },
  {
    "title": "Rounds",
    "reason": "12h de jeu, Score Platinum. PvP local avec potes, parties de 10-20min. Combat frénétique avec power-ups. Fun garanti."
  },
  {
    "title": "Slay the Spire",
    "reason": "80h (vous aimez déjà !). Runs de 30-60min. Le deck-builder parfait pour les sessions courtes. Toujours 'une dernière run'."
  },
  {
    "title": "Into the Breach",
    "reason": "10h de jeu, Score Gold. Stratégie au tour par tour, runs de 20-40min. Chaque décision compte, gameplay tactique parfait."
  }
]
```

---

## 📈 EXEMPLE 8 : Analyse comparative

### Question
```
Compare mes heures de jeu entre RPG, action et stratégie et recommande des jeux pour équilibrer
```

### Réponse JSON attendue
```json
[
  {
    "title": "Analyse de votre bibliothèque",
    "reason": "RPG : 450h (45%), Action : 380h (38%), Stratégie : 170h (17%). Vous êtes clairement RPG > Action > Stratégie. Pour équilibrer, voici mes suggestions de jeux stratégie dans votre bibliothèque :"
  },
  {
    "title": "XCOM 2",
    "reason": "8h de jeu. Stratégie tactique au tour par tour. Si vous avez aimé les RPG tactiques, c'est le pont parfait vers la pure stratégie. Score Platinum ProtonDB."
  },
  {
    "title": "Civilization VI",
    "reason": "45h (vous avez déjà accroché !). Grande stratégie 4X. Continuez, c'est parfait pour équilibrer vos RPG d'action. Sessions longues mais satisfaisantes."
  },
  {
    "title": "Stellaris",
    "reason": "2h de jeu. Grand strategy spatial. Courbe d'apprentissage raide mais incroyablement profond. Donnez-lui 10h et vous aurez un nouveau genre favori."
  },
  {
    "title": "Into the Breach",
    "reason": "10h. Petit format mais stratégie pure. Parfait pour alterner avec vos gros RPG. Sessions courtes, réflexion intense."
  }
]
```

---

## 💡 EXEMPLE 9 : Recommandation externe + interne

### Question
```
J'ai adoré God of War (PS4). Quels jeux dans ma bibliothèque ont un combat et une narration similaires ? Et suggère-moi aussi des jeux Steam similaires que je n'ai pas
```

### Réponse JSON attendue
```json
[
  {
    "title": "Jedi: Fallen Order",
    "reason": "15h dans votre bibliothèque. Combat souls-like cinématique + narration forte comme GoW. Exploration metroidvania. Score Gold ProtonDB."
  },
  {
    "title": "Darksiders II",
    "reason": "8h dans votre bibliothèque. Hack'n'slash + RPG + énigmes. Moins épique que GoW mais même recette action-aventure. Bonne histoire."
  },
  {
    "title": "Devil May Cry 5",
    "reason": "25h dans votre bibliothèque. Combat spectaculaire mais différent de GoW (moins narratif, plus arcade). Si vous voulez de l'action pure, c'est ça."
  },
  {
    "title": "God of War (2018)",
    "appid": "1593500",
    "reason": "JEU NON POSSÉDÉ - Le GoW que vous aimez est maintenant sur PC ! Combat amélioré, narration père-fils exceptionnelle. Must-have si vous avez aimé la version PS4."
  },
  {
    "title": "Lies of P",
    "appid": "1627720",
    "reason": "JEU NON POSSÉDÉ - Souls-like avec combat technique proche de GoW. Boss design excellent, narration sombre. Sorti en 2023."
  }
]
```

---

## 🎮 EXEMPLE 10 : Question complexe multi-critères

### Question
```
Je veux un jeu d'aventure narratif, solo, avec moins de 20h pour finir l'histoire principale, score ProtonDB minimum Gold, et qui a une ambiance unique
```

### Réponse JSON attendue
```json
[
  {
    "title": "What Remains of Edith Finch",
    "reason": "2h de jeu dans votre bibliothèque, Score Platinum. Walking simulator narratif de 2-3h. Histoire fractionnée incroyable, ambiance mélancolique unique. Expérience inoubliable."
  },
  {
    "title": "Firewatch",
    "reason": "Jamais lancé, Score Gold. 4-5h, aventure narrative dans les forêts du Wyoming. Ambiance contemplative, mystère, dialogues excellents. Parfait sur Steam Deck."
  },
  {
    "title": "A Plague Tale: Innocence",
    "reason": "8h de jeu, Score Gold. 12-15h, action-aventure narratif. France médiévale + peste noire = ambiance unique et sombre. Histoire touchante."
  },
  {
    "title": "Outer Wilds",
    "reason": "2h de jeu, Score Gold. 15-20h, exploration spatiale + puzzle temporel. Ambiance cosmique contemplative absolument unique. Pas d'action, que de l'exploration et découverte."
  },
  {
    "title": "Oxenfree",
    "reason": "3h de jeu, Score Platinum. 4-6h, aventure narrative avec dialogues en temps réel. Ambiance surnaturelle adolescente unique. OST incroyable."
  }
]
```

---

## 🏆 Conseils pour formuler vos questions

### ✅ Questions efficaces

**Spécifiques** :
- ✅ "RPG avec moins de 30h, score Platinum, jamais lancé"
- ❌ "Un bon jeu"

**Contextuelles** :
- ✅ "J'ai aimé X et Y, suggère Z dans ma bibliothèque"
- ❌ "Recommande un jeu"

**Avec critères** :
- ✅ "Multijoueur, sessions courtes, ProtonDB Gold minimum"
- ❌ "Jeu sympa"

### 💡 Ajoutez vos préférences

**Temps de jeu** :
- "moins de 10h pour finir"
- "sessions de 30min max"
- "jeu long type 100h+"

**Compatibilité** :
- "score Platinum ProtonDB"
- "parfait pour Steam Deck"
- "fonctionne avec manette"

**Genre et style** :
- "roguelike avec progression permanente"
- "narration forte"
- "gameplay difficile mais juste"

---

## 🚀 Mode d'emploi rapide

1. **Chargez votre bibliothèque**
2. **Formulez une question claire avec des critères**
3. **Cliquez sur "POSER LA QUESTION"**
4. **Mode local** : Attendez la réponse automatique
5. **Mode manuel** : Collez dans votre LLM, importez la réponse
6. **Explorez les suggestions**
7. **Sauvegardez** si vous voulez les retrouver

---

## 📚 Ressources

- `GUIDE_ASK_ANYTHING.md` - Guide complet
- `README_LLM_LOCAL.md` - Setup Ollama
- `CHANGELOG_ASK_ANYTHING.md` - Détails techniques

Bon gaming ! 🎮✨
