---
name: vault-research
description: >
  Effectue une recherche web approfondie (WebSearch + WebFetch) sur un sujet
  métier et sauvegarde le résultat comme note structurée dans knowledge/.
  Invoqué par /vault research "<sujet>" [--category <cat>].
  Catégories : marche, scoring, inspiration, sales, marketing, ooh-dooh, concurrents, prospects.
version: 1.0.0
author: IA-Agency Polynésie
tags: [vault, research, knowledge, veille, webresearch]
allowed-tools: WebSearch, WebFetch, Read, Write, Glob
---

# Vault Research — Veille ciblée à la demande

> **Usage** : `/vault research "<sujet>" [--category marche|scoring|inspiration|sales|marketing|ooh-dooh|concurrents|prospects]`
>
> Exemples :
> - `/vault research "comportement Facebook Polynésie 2026" --category marche`
> - `/vault research "techniques closing agence digitale" --category sales`
> - `/vault research "DOOH aéroport Tahiti Faa'a" --category ooh-dooh`
> - `/vault research "AI search GEO optimization 2026" --category inspiration`

---

## Objectif

Enrichir la base de connaissances du projet avec une note de recherche approfondie
sur un sujet précis. Cette note sera consultée par tous les skills en Phase 0
pour calibrer leurs analyses, scores et recommandations.

---

## Phase 1 — Parsing et préparation

1. Extraire le sujet (texte entre guillemets ou tout ce qui suit `research` avant `--`)
2. Détecter la catégorie depuis `--category`. Défaut si absent : **`marche`**
3. Catégories valides : `marche | scoring | inspiration | sales | marketing | ooh-dooh | concurrents | prospects`
4. Générer le `topic-slug` : minuscules, accents supprimés, espaces → tirets, max 50 caractères
5. Générer la date du jour : `YYYY-MM-DD` et le mois courant : `YYYY-MM`
6. Chemin output : `knowledge/<category>/<topic-slug>-<YYYY-MM>.md`
7. Vérifier si une note existante correspond : `Glob("knowledge/<category>/<topic-slug>*.md")`
   - Si trouvée → proposer : "Une note similaire existe déjà ([chemin]). Mettre à jour ou créer une nouvelle version ?"
   - Si l'utilisateur choisit update → remplacer le fichier existant
   - Sinon → créer avec version suffixe `-v2`, `-v3`, etc.

---

## Phase 2 — Génération des requêtes de recherche

Générer **4 à 5 requêtes WebSearch** couvrant le sujet sous plusieurs angles :

| Règle | Obligation |
|-------|-----------|
| Requêtes en français | ≥ 2 |
| Requêtes en anglais | ≥ 1 |
| Qualificatif marché/géographie | ≥ 1 (ex: "Polynésie française", "Tahiti", "Fenua", ou marché cible) |
| Requête orientée données/stats | ≥ 1 (ex: "statistiques 2025 2026", "étude", "rapport", "data") |

Exemples pour `"comportement Facebook Polynésie 2026" --category marche` :
```
1. "comportement consommateurs Facebook Polynésie française 2026"
2. "usages réseaux sociaux Tahiti statistiques 2025 2026"
3. "Facebook Messenger business discovery French Polynesia"
4. "digital behavior small island markets social media 2026"
5. "TPE Fenua présence Facebook données ISPF DGEN"
```

---

## Phase 3 — Recherche web

Pour chaque requête :
1. `WebSearch <requête>` → collecter les URLs retournées
2. Dédupliquer les URLs à travers toutes les requêtes
3. Filtrer :
   - Exclure : profils réseaux sociaux (facebook.com/posts, twitter.com, instagram.com)
   - Préférer : articles de presse, rapports institutionnels, blogs experts, études sectorielles
   - Pour catégorie `marche` : prioriser les sources .pf (ispf.pf, service-public.pf, open.pf, opt.pf)
4. Constituer une liste de **10 à 15 URLs candidates**
5. Sélectionner les **3 à 5 meilleures** selon : pertinence du titre, autorité de la source, récence

Fallback si WebSearch indisponible :
- Construire URL Google : `https://www.google.com/search?q=<requête+encodée>`
- `WebFetch` sur l'URL Google pour extraire les liens de résultats
- Continuer avec ces liens

---

## Phase 4 — Extraction du contenu

Pour chacune des 3 à 5 sources sélectionnées :
1. `WebFetch <url>`
2. Extraire :
   - Statistiques chiffrées avec leur date de publication
   - Comportements observés ou tendances décrites
   - Citations d'experts ou d'études
   - Données géographiques ou sectorielles pertinentes
3. Flaguer toute donnée dont la date source est **> 18 mois** avec `⚠️ [DONNÉES À VÉRIFIER — date]`
4. Si fetch échoue (timeout, paywall, login) → noter "Source inaccessible" et passer à la suivante
5. Évaluer la fiabilité globale des sources :
   - `haute` : 3+ sources concordantes, sources institutionnelles ou études reconnues
   - `moyenne` : 2 sources, blogs experts reconnus
   - `faible` : source unique ou données anciennes

---

## Phase 5 — Synthèse de la note

Rédiger la note complète selon ce template exact :

```markdown
---
title: "[Titre descriptif — max 80 caractères]"
date: YYYY-MM-DD
topic: "[sujet tel que saisi par l'utilisateur]"
topic-slug: "[topic-slug]"
category: [marche|scoring|inspiration|sales|marketing|ooh-dooh|concurrents|prospects]
market: polynesie-francaise
tags: [research, <category>, <mots-clés du sujet>]
sources:
  - url: "[url1]"
    title: "[titre de la page]"
    date_accessed: YYYY-MM-DD
  - url: "[url2]"
    title: "[titre]"
    date_accessed: YYYY-MM-DD
confidence: haute|moyenne|faible
expires: YYYY-MM
---

# [Titre]

> Recherche effectuée le [date] — [N] sources analysées — Confiance : [haute|moyenne|faible]

---

## Données clés

- [Statistique 1 avec source inline — ex: "Facebook = 81,78% des parts marché social PF (Statcounter, jan 2025)"]
- [Statistique 2]
- [...]

## Comportements observés

[2 à 4 paragraphes de synthèse narrative.
Priorité au marché polynésien. Si données PF indisponibles,
extrapoler depuis marchés comparables en le signalant.]

## Implications scoring

[Comment ces données modifient-elles les pondérations ou critères du scoring IA-Agency ?
Ex : "La pondération Facebook dans geo-social mériterait d'être augmentée de 25% à 30%."
Laisser VIDE (ne pas supprimer la section) si la recherche n'a pas d'implication directe sur le scoring.]

## Idées d'implémentation

[Nouveaux skills, commandes, ou fonctionnalités suggérés pour le projet IA-Agency
inspirés par cette recherche.
Ex : "Ajouter une détection du badge Messenger (<15 min) dans geo-social."
Laisser VIDE si aucune idée n'émerge.]

## Sources

| # | Source | Date accès | Fiabilité |
|---|--------|------------|-----------|
| 1 | [titre](url) | YYYY-MM-DD | haute/moyenne/faible |
| 2 | ... | | |

---
*Note générée par `/vault research` — IA-Agency Polynésie*
```

---

## Phase 6 — Sauvegarde et mise à jour de l'index

**Étape 6a — Write la note** :
```
Write knowledge/<category>/<topic-slug>-<YYYY-MM>.md
```

**Étape 6b — Mise à jour de l'index** :
1. `Read knowledge/index.md`
2. Localiser l'ancre `<!-- AUTO: <category> links -->`
3. Vérifier si le slug existe déjà dans la section → si oui, mettre à jour la ligne existante
4. Si non, insérer une nouvelle ligne juste avant l'ancre :
   ```
   - [[<topic-slug>-<YYYY-MM>]] — [Titre] — [YYYY-MM-DD]
   ```
5. `Write knowledge/index.md` avec la version mise à jour

**Étape 6c — Confirmation** :
```
✅ Note sauvegardée : knowledge/<category>/<topic-slug>-<YYYY-MM>.md
📚 Sources analysées : N
🗂️ Index mis à jour : knowledge/index.md
💡 Idées d'implémentation : [résumé en 1 ligne si présentes]
```

---

## Règles importantes

- **Jamais de tarif** dans les notes — règle commerciale du projet
- **Toujours dater les données** — une stat sans date est inutilisable
- **Section "Implications scoring" toujours présente** — même si vide
- **Section "Idées d'implémentation" toujours présente** — même si vide
- **Anti-collision index** : vérifier existence du slug avant insertion
