---
name: geo-rewrite-page
description: >
  Réécrit une page web existante pour maximiser les signaux E-E-A-T et la citabilité IA.
  Conserve le contenu utile, restructure pour les LLMs, ajoute les signaux manquants.
  Produit la version réécrite + un diff commenté des changements et leur justification.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, content, rewrite, eeat, citabilite, optimisation, page]
allowed-tools: Read, Write, WebFetch, Bash
---

# GEO Rewrite Page — Réécriture E-E-A-T pour Citabilité IA

> **Usage** : `/geo rewrite-page <url>`
>
> Exemples :
> - `/geo rewrite-page https://restaurant-te-moana.pf/notre-histoire`
> - `/geo rewrite-page https://hotel-kia-ora.pf/chambres`
> - `/geo rewrite-page https://surf-tahiti.pf/cours-surf`

---

## Objectif

Transformer une page existante en **ressource citable par les IA**.
Ne pas tout réécrire — conserver ce qui fonctionne, optimiser ce qui bloque.

Le livrable : la page réécrite + un document d'explication pour le client
("voici ce qu'on a changé et pourquoi").

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Étape 1 — Extraction et audit de la page existante

### 1.1 Fetch de la page
```
WebFetch <url>
```

Extraire :
- Titre H1 et méta-titre
- Méta-description
- Structure des headings (H1, H2, H3...)
- Contenu textuel complet
- Balises de schéma existantes (si visibles dans le HTML)
- Liens internes et externes présents
- Images avec ou sans alt text
- Longueur totale en mots

### 1.2 Diagnostic rapide

Pour chaque problème identifié, le coder avec un niveau de priorité :

| Code | Priorité | Exemples |
|------|----------|---------|
| 🔴 CRITIQUE | Impact direct sur la citabilité | Pas de réponse directe, contenu vague, pas de H2 |
| 🟡 IMPORTANT | Impact sur E-E-A-T | Pas de date, pas d'auteur, pas de données |
| 🟢 AMÉLIORATION | Optimisation fine | Longueur des blocs, formulation, mots-clés |

---

## Étape 2 — Grille d'audit E-E-A-T

Évaluer chaque signal sur la page originale :

### Experience (Expérience vécue)
| Signal | Présent ? | Notes |
|--------|-----------|-------|
| Chiffres concrets (années, nombre de clients...) | ✓/✗ | |
| Détails terrain / sensoriels spécifiques | ✓/✗ | |
| Citations directes de l'équipe ou du propriétaire | ✓/✗ | |
| Photos avec contexte réel (pas stock) | ✓/✗ | |

### Expertise
| Signal | Présent ? | Notes |
|--------|-----------|-------|
| Nom de l'auteur / signataire | ✓/✗ | |
| Certifications, formations, labels | ✓/✗ | |
| Explications techniques ou de métier | ✓/✗ | |
| Données vérifiables (dates, chiffres) | ✓/✗ | |

### Authoritativeness
| Signal | Présent ? | Notes |
|--------|-----------|-------|
| Mentions de partenaires reconnus | ✓/✗ | |
| Prix, labels, classements | ✓/✗ | |
| Liens vers des sources externes fiables | ✓/✗ | |
| Présence sur des annuaires officiels (mentionnée) | ✓/✗ | |

### Trustworthiness
| Signal | Présent ? | Notes |
|--------|-----------|-------|
| Date de publication / mise à jour visible | ✓/✗ | |
| Politique de contact, conditions claires | ✓/✗ | |
| Avis clients intégrés ou mentionnés | ✓/✗ | |
| HTTPS (vérifié lors du fetch) | ✓/✗ | |

### Structure pour LLMs
| Critère | Présent ? | Notes |
|---------|-----------|-------|
| H1 = réponse directe à une question fréquente | ✓/✗ | |
| H2 = sous-questions logiques | ✓/✗ | |
| Premier paragraphe = réponse directe (pas d'intro générique) | ✓/✗ | |
| Blocs de 134-167 mots autonomes | ✓/✗ | |
| FAQ section présente | ✓/✗ | |
| Listes à puces pour les infos factuelles | ✓/✗ | |

---

## Étape 3 — Plan de réécriture

Avant de réécrire, produire un plan commenté :

```
## Plan de réécriture — [URL]

### Ce qu'on conserve
- [Éléments à garder tels quels — ex : "le témoignage client en §3 est excellent"]

### Ce qu'on restructure
- [Éléments à réorganiser — ex : "déplacer les infos pratiques en FAQ"]

### Ce qu'on ajoute
- [Signaux manquants — ex : "ajouter date de mise à jour", "ajouter certifications"]

### Ce qu'on supprime
- [Éléments contre-productifs — ex : "intro générique de 3 lignes sans information"]

### Titre réécrit
- Avant : "[ancien titre]"
- Après : "[nouveau titre = question directe ou affirmation forte]"
```

---

## Étape 4 — Réécriture

### Règles de réécriture

**Le premier paragraphe doit répondre directement.**
Les LLMs lisent la page comme un scanner — ils extraient le premier paragraphe
substantiel. S'il ne contient pas la réponse, la page ne sera pas citée.

❌ Avant (intro générique) :
> "Bienvenue chez Restaurant Te Moana ! Nous sommes ravis de vous accueillir
> dans notre établissement situé au cœur de Moorea..."

✅ Après (réponse directe) :
> "Restaurant Te Moana propose une cuisine polynésienne authentique à Moorea,
> spécialisée dans les poissons du lagon pêchés chaque matin. La carte change
> selon les arrivages, avec une sélection de 8 à 12 plats par service."

**Chaque H2 = une question que quelqu'un poserait à ChatGPT.**

❌ Avant : "Notre histoire"
✅ Après : "Depuis quand Restaurant Te Moana est-il ouvert ?"

❌ Avant : "Nos services"
✅ Après : "Que propose Restaurant Te Moana ?"

**Intégrer les données factuelles manquantes.**
Si le client n'a pas fourni certaines données, marquer avec `[À CONFIRMER]` :
> "Restaurant Te Moana accueille [À CONFIRMER : environ X couverts] par service."

---

## Étape 5 — Output

### Fichier livrable

```markdown
# Réécriture E-E-A-T — [URL]
**Date :** [date]

---

## Rapport de diagnostic

### Score E-E-A-T avant réécriture : [XX]/100

| Dimension | Avant | Problèmes identifiés |
|-----------|-------|---------------------|
| Experience | [X]/25 | [...] |
| Expertise | [X]/25 | [...] |
| Authoritativeness | [X]/25 | [...] |
| Trustworthiness | [X]/25 | [...] |

### Problèmes critiques traités
1. [Problème 🔴 → Solution appliquée]
2. [Problème 🔴 → Solution appliquée]
3. [Problème 🟡 → Solution appliquée]

---

## Page réécrite

[Contenu complet de la page réécrite, prêt à copier-coller dans le CMS]

---

## Guide de mise en ligne

Instructions pour le client (non-technique) :
1. [Étape concrète — ex : "Aller dans WordPress > Pages > [nom de la page]"]
2. [Étape — ex : "Copier le texte ci-dessus dans l'éditeur"]
3. [Étape — ex : "Modifier la date de mise à jour (champ en bas de page)"]
4. [Étape — ex : "Cliquer sur Mettre à jour"]

---

## Points à confirmer avec le client

- [ ] [Donnée marquée [À CONFIRMER] #1]
- [ ] [Donnée marquée [À CONFIRMER] #2]

---

## Score E-E-A-T estimé après réécriture : [XX]/100

[Brève explication de l'amélioration attendue]
```

Fichier généré : `REWRITE-[slug-page]-[date].md`

---

## Enregistrement dans le CRM
```
/geo prospect note <id> "Page réécrite : [url] — E-E-A-T [avant] → [après estimé]"
```
