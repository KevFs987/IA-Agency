---
name: geo-citations
description: >
  Mesure le Share of Model (SoM) d'une entreprise : dans quelle proportion
  apparaît-elle quand un client potentiel pose des questions à une IA ?
  Teste Perplexity, Google, et Bing (proxy Copilot). Identifie les concurrents
  cités à la place. Produit un score SoM (0-100%) et des recommandations concrètes.
version: 1.0.0
author: IA-Agency Polynésie
tags: [geo, citations, share-of-model, som, llm, perplexity, chatgpt, visibilite-ia]
allowed-tools: Read, Write, WebFetch, Bash, Glob
---

# GEO Citations — Mesure du Share of Model (SoM)

> **Usage** : `/geo citations <url-ou-nom>`
>
> Exemples :
> - `/geo citations https://hotel-kia-ora.pf`
> - `/geo citations "Restaurant Te Moana Moorea"`
> - `/geo citations https://facebook.com/surf-tahiti`

---

## Qu'est-ce que le Share of Model ?

Le Share of Model (SoM) mesure la fréquence à laquelle une entreprise est citée
dans les réponses des IA génératives (ChatGPT, Perplexity, Gemini) quand un client
potentiel pose une question sur son secteur.

**Analogie** : comme la part de marché, mais dans les réponses des IA plutôt que
dans les ventes. Un SoM de 0% = invisible sur les IA. Un SoM de 60% = cité dans
6 requêtes sur 10 pertinentes.

**Contexte PF** : ChatGPT = 4ème site le plus visité en Polynésie française
(70 000 visites/mois). Un touriste qui planifie son séjour pose des questions
à ChatGPT ou Perplexity avant même d'ouvrir Google Maps.

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Étape 1 — Identification de l'entreprise

Détecter le type d'input :

| Input | Action |
|-------|--------|
| URL site web | WebFetch homepage → extraire nom, secteur, localisation |
| URL sociale (Facebook/Instagram/TikTok) | WebFetch → extraire nom, secteur, localisation |
| Nom entre guillemets | Utiliser directement + WebFetch Google pour confirmer secteur et lieu |

Construire le profil minimal :

```
- nom_canonique : [ex: "Hôtel Kia Ora"]
- secteur : [restaurant / hôtel / activité / commerce / service]
- localisation : [île + commune — ex: "Rangiroa, Polynésie française"]
- cible_langue : [FR / EN / bilingue — selon le secteur]
```

---

## Étape 2 — Génération des requêtes de test

Générer **8 requêtes** qui simulent ce que de vrais clients poseraient à une IA.
Les requêtes doivent être naturelles, pas orientées SEO.

### Règles de génération

- **2 requêtes génériques FR** (ce qu'un local chercherait)
  - ex: "meilleur restaurant à Rangiroa"
  - ex: "où dormir à Rangiroa pas cher"

- **2 requêtes génériques EN** (ce qu'un touriste anglophones chercherait)
  - ex: "best hotel in Rangiroa"
  - ex: "where to stay in Rangiroa French Polynesia"

- **2 requêtes avec caractéristiques** (ce que quelqu'un de plus précis chercherait)
  - ex: "pension de famille avec demi-pension Rangiroa"
  - ex: "overwater bungalow Rangiroa with diving"

- **2 requêtes de recommandation directe** (trigger le plus fort pour les LLM)
  - ex: "recommande-moi un hôtel à Rangiroa pour plongée"
  - ex: "what's the best place to stay in Rangiroa for scuba diving"

---

## Étape 3 — Test multi-moteurs IA

Pour chaque requête, tester sur **3 moteurs** :

### 3.1 Perplexity (priorité 1 — le plus accessible)
```
WebFetch : https://www.perplexity.ai/search?q=[requête+encodée]

Pour chaque résultat :
- [nom_canonique] est-il cité dans la réponse ? (OUI / NON)
- Si OUI : extrait de citation (1-2 phrases)
- Si NON : quels concurrents sont cités à la place ?
- Sources utilisées par Perplexity pour cette réponse
```

### 3.2 Google (proxy Google AIO et Search Generative Experience)
```
WebFetch : https://www.google.com/search?q=[requête+encodée]

Pour chaque résultat :
- [nom_canonique] apparaît-il dans les 5 premiers résultats organiques ?
- Apparaît-il dans un Knowledge Panel / Local Pack / Featured Snippet ?
- Quels concurrents apparaissent avant lui ?
```

### 3.3 Bing (proxy Copilot / Microsoft AI)
```
WebFetch : https://www.bing.com/search?q=[requête+encodée]

Pour chaque résultat :
- [nom_canonique] est-il cité ?
- Position dans les résultats
```

### Gestion des blocages
Si un moteur bloque le fetch :
→ Marquer "Non accessible lors de ce test"
→ Continuer avec les moteurs disponibles
→ Indiquer dans le rapport que le score est partiel

---

## Étape 4 — Calcul du Score SoM

### Tableau de résultats

Construire une matrice de résultats :

```
Requête | Perplexity | Google | Bing | Cité ?
--------|-----------|--------|------|-------
req 1   | OUI       | OUI    | NON  | ✅ (2/3)
req 2   | NON       | NON    | NON  | ❌ (0/3)
...
```

### Formule SoM

```python
# Pondération par moteur (importance dans le marché PF)
poids = {
    "perplexity": 0.45,  # Fort chez les early adopters + touristes
    "google":     0.40,  # Dominant tous publics
    "bing":       0.15   # Copilot / utilisateurs Microsoft
}

# Score par requête = moyenne pondérée des présences sur les moteurs testés
score_requete = sum(presence[moteur] * poids[moteur] for moteur in moteurs_testés)

# SoM global = moyenne des scores sur toutes les requêtes
som_global = sum(score_requete) / nombre_requetes_testées

# Convertir en pourcentage (0-100)
som_pct = round(som_global * 100)
```

### Interprétation du SoM

| SoM | Niveau | Interprétation |
|-----|--------|---------------|
| 0% | Invisible | L'entreprise n'existe pas pour les IA |
| 1-20% | Émergent | Cité très rarement, sur des requêtes très spécifiques |
| 21-40% | Présent | Commence à apparaître, mais pas systématiquement |
| 41-60% | Visible | Cité dans 1 requête sur 2, bonne base à renforcer |
| 61-80% | Fort | Référence locale reconnue par les IA |
| 81-100% | Leader | Dominant dans les réponses IA sur son marché local |

---

## Étape 5 — Analyse concurrentielle

Identifier les **concurrents cités à la place** de l'entreprise analysée :

```
Pour chaque requête où [nom_canonique] n'est PAS cité :
- Lister les 1-3 noms cités dans la réponse
- Tabuler la fréquence : quel concurrent est cité le plus souvent ?
```

Construire le classement concurrentiel :

```
Concurrent A — cité dans X/8 requêtes
Concurrent B — cité dans Y/8 requêtes
[nom_canonique] — cité dans Z/8 requêtes ← position actuelle
```

---

## Étape 6 — Rapport SoM

```markdown
# Rapport Share of Model — [Nom de l'entreprise]
**Date :** [date]  **Moteurs testés :** Perplexity, Google, Bing

---

## Score SoM : [XX]%

[Une phrase de contexte]
Exemple : "Sur 8 requêtes qu'un touriste ou client local pourrait poser à une IA,
[nom] apparaît dans [N] d'entre elles — soit [XX]% du temps."

---

## Résultats par requête

| Requête | Perplexity | Google | Bing | Résultat |
|---------|-----------|--------|------|----------|
| [req 1] | ✅ / ❌ | ✅ / ❌ | ✅ / ❌ | Cité / Non cité |
| [req 2] | ... | ... | ... | ... |
| [req 3] | ... | ... | ... | ... |
| [req 4] | ... | ... | ... | ... |
| [req 5] | ... | ... | ... | ... |
| [req 6] | ... | ... | ... | ... |
| [req 7] | ... | ... | ... | ... |
| [req 8] | ... | ... | ... | ... |

---

## Vos concurrents dans les IA

[Tableau des concurrents les plus cités avec leur SoM estimé]

| Concurrent | Citations IA | Avantage estimé |
|-----------|-------------|----------------|
| [Concurrent A] | X/8 requêtes | [Ce qu'ils ont que vous n'avez pas] |
| [Concurrent B] | Y/8 requêtes | [...] |

---

## Pourquoi ces concurrents apparaissent-ils ?

[Analyse courte : que font-ils que [nom] ne fait pas ?
ex: fiche TripAdvisor complète, site web bien indexé, nombreux avis récents, etc.]

---

## Ce qu'il faut corriger en priorité

[3 actions classées par impact sur le SoM — sans solution détaillée si usage prospection]

### Action 1 — [Titre] (impact estimé : +[X]% SoM)
[Description du problème en 1-2 phrases]

### Action 2 — [Titre] (impact estimé : +[X]% SoM)
[...]

### Action 3 — [Titre] (impact estimé : +[X]% SoM)
[...]

---

## Objectif atteignable à 3 mois

Avec les corrections prioritaires, SoM estimé : **[XX]% → [YY]%**

[Formulation client — ex: "Passer de 12% à 40% signifie apparaître dans les réponses
de 3 touristes sur 10 qui planifient un séjour à Rangiroa sur ChatGPT ou Perplexity.
Sans publicité payante."]

---

*Rapport GEO Citations v1.0 — IA-Agency Polynésie — [date]*
```

---

## Règles d'or

- **Jamais de tarif** dans ce rapport — il peut être utilisé en prospection
- Si l'entreprise a un SoM = 0% : ne pas être brutal — "votre secteur en PF est
  sous-représenté sur les IA, ce qui crée une opportunité réelle pour les premiers movers"
- Toujours mentionner les concurrents cités : c'est l'argument le plus motivant
- Langue du rapport = langue de la cible (FR pour commerces locaux, EN si tourisme)

---

## Intégration avec les autres skills

Ce skill peut être invoqué :
- **Seul** : `/geo citations <url>` — rapport complet standalone
- **Depuis geo-discover** : la vérification Perplexity (étape 2.9) est une version
  rapide du test SoM — geo-citations va plus loin avec 8 requêtes + analyse concurrentielle
- **Depuis geo-prep-call** : intégrer le SoM dans le briefing commercial
  ("leur SoM est de 8% — leurs concurrents sont à 35%")
- **Depuis geo-teaser-report** : la question finale peut être
  "Saviez-vous que [Concurrent A] apparaît 4 fois plus souvent que vous sur ChatGPT ?"

---

## Output

Fichier : `GEO-CITATIONS-[nom-nettoyé]-[date].md`

Données JSON pour intégration CRM :
```json
{
  "nom": "[nom canonique]",
  "date": "[YYYY-MM-DD]",
  "som_pct": [0-100],
  "requetes_testees": 8,
  "citations_count": [N],
  "moteurs": ["perplexity", "google", "bing"],
  "top_concurrent": "[nom concurrent le plus cité]",
  "top_concurrent_som": [0-100]
}
```
