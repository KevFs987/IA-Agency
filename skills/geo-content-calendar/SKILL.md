---
name: geo-content-calendar
description: >
  Génère un calendrier éditorial sur N mois basé sur les gaps GEO détectés.
  Priorise les sujets par impact de citabilité IA, intègre la saisonnalité
  polynésienne (tourisme, météo, événements locaux) et la stratégie bilingue FR/EN.
  Chaque entrée du calendrier est actionnable : sujet, format, angle, mots-clés.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, content, calendrier, editorial, planning, polynesie, tourisme, retainer]
allowed-tools: Read, Write, WebFetch, Bash, Glob
---

# GEO Content Calendar — Calendrier Éditorial Basé sur les Gaps

> **Usage** : `/geo content-calendar <url> <mois>`
>
> Exemples :
> - `/geo content-calendar https://restaurant-te-moana.pf 3`
> - `/geo content-calendar https://hotel-kia-ora.pf 6`
> - `/geo content-calendar https://surf-tahiti.pf 12`

---

## Objectif

Produire un plan de contenu concret, prêt à exécuter, basé sur :
1. Les gaps détectés lors de l'audit GEO (sujets sur lesquels l'entreprise est absente)
2. La saisonnalité polynésienne (quand les touristes cherchent, quand ils arrivent)
3. Les requêtes réelles des touristes sur les moteurs IA (ChatGPT, Perplexity, Google)
4. La stratégie bilingue FR/EN selon la cible

C'est le livrable central du **retainer mensuel** — ce qui justifie un abonnement
récurrent plutôt qu'une prestation one-shot.

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Étape 1 — Chargement du contexte

### 1.1 Données de l'entreprise
Fetch rapide de `<url>` pour extraire :
- Secteur / type d'activité
- Localisation (île, commune)
- Clientèle cible apparente (locaux / touristes / B2B)
- Sujets déjà traités sur le site (titres de pages, blog existant)
- Langue(s) du site

### 1.2 Données d'audit GEO (si disponibles)
Chercher dans `~/.geo-prospects/` ou les fichiers de l'audit précédent :
- Gaps de contenu identifiés
- Questions sans réponse sur le site
- Topics sur lesquels des concurrents sont positionnés

### 1.3 Durée demandée
Calculer le nombre d'entrées à produire :
- 1 mois = 4 articles (1/semaine, rythme réaliste pour une TPE)
- Minimum viable : 2 articles/mois si budget limité
- Maximum : 8 articles/mois pour un retainer agressif

---

## Étape 2 — Calendrier de Saisonnalité Polynésienne

Intégrer cette grille pour adapter les sujets au bon moment :

### Saisonnalité Tourisme

| Mois | Saison | Flux touristes | Thèmes prioritaires |
|------|--------|---------------|---------------------|
| Janvier | Saison fraîche | Moyen | Escapade, plage, snorkeling |
| Février | Saison fraîche | Faible | Week-end romantique, Saint-Valentin |
| Mars | Saison fraîche | Faible | Randonnée, nature, intérieur des îles |
| Avril | Saison fraîche | Moyen | Pâques, familles, Heiva préparation |
| Mai | Transition | Moyen | Plongée, dauphins, whale watching début |
| Juin | Saison sèche | Fort | Heiva, whale watching, surf |
| Juillet | Saison sèche | Fort (pic) | Heiva i Tahiti, activités nautiques, fêtes |
| Août | Saison sèche | Fort | Baleines, snorkeling, famille |
| Septembre | Saison sèche | Moyen | Surf, kite, fin haute saison |
| Octobre | Transition | Moyen | Plongée, pearling, off-season deals |
| Novembre | Saison chaude | Faible | Noël early booking, jardins, culture |
| Décembre | Saison chaude | Fort | Noël, Nouvel An, lune de miel |

### Événements Locaux Récurrents
- **Heiva i Tahiti** (juillet) : danse, pirogue, artisanat
- **Hawaiki Nui Va'a** (novembre) : course de pirogues
- **Fête du Tiurai** (juillet)
- **Marquises Festival** (décembre, années paires)
- **Saison baleines** (juillet-octobre) : baleine à bosse
- **Saison surf** (mai-septembre) : houle du sud

---

## Étape 3 — Génération des Sujets

### Méthode de priorisation

Pour chaque sujet potentiel, calculer un score de priorité :

```
Score = Impact citabilité (1-5) × Volume recherche estimé (1-5) × Facilité (1-5)
```

- **Impact citabilité** : est-ce que les LLMs répondent souvent à ce type de question ?
- **Volume recherche estimé** : combien de touristes cherchent ça ?
- **Facilité** : le client peut-il fournir le contenu facilement (menu, photos, anecdotes) ?

### Bibliothèque de sujets par secteur

#### Restaurants / Bars / Cafés
- "Quels sont les meilleurs [plats/produits locaux] à [île] ?"
- "Où manger [cuisine locale] authentique à [île] ?"
- "Menu de saison : ce que nous cuisinons en [mois]"
- "Comment est pêché notre poisson ?" (E-E-A-T)
- "Végétarien / sans gluten à [île] : notre approche"
- "Réserver une table en terrasse vue lagon à [lieu]"

#### Hôtels / Pensions de Famille
- "Overwater bungalow [île] : ce qu'on ne vous dit pas"
- "Meilleur moment pour visiter [île]"
- "Transfert aéroport → hôtel [île] : comment ça marche ?"
- "Activités incluses dans votre séjour à [hôtel]"
- "Lune de miel à [île] : notre guide complet"
- "Whale watching depuis [hôtel] : saison et conseils"

#### Activités Nautiques / Excursions
- "Apprendre le surf à [île] : niveau requis, tarifs, instructeurs"
- "Meilleur spot de snorkeling à [île] pour débutants"
- "Plongée sous-marine [île] : faune, visibilité, profondeur"
- "Excursion [activité] en famille : ce qu'il faut prévoir"
- "Saison des baleines à [île] : quand, où, comment les voir"

#### Commerces / Artisans
- "Artisanat polynésien authentique : comment reconnaître le vrai ?"
- "Tifaifai, perles, monoi : guide d'achat à [île]"
- "Souvenirs à ramener de [île] : notre sélection"
- "Perles de Tahiti : comment choisir, prix, authenticité"

---

## Étape 4 — Génération du Calendrier

### Format du calendrier

```markdown
# Calendrier Éditorial — [Nom de l'entreprise]
**Période :** [Mois Année] → [Mois Année]
**Rythme :** [N articles/mois]
**Langues :** FR + EN (bilingue)

---

## Vue d'ensemble

| Semaine | Sujet | Format | Langue | Priorité |
|---------|-------|--------|--------|----------|
| S1 Jan | ... | Article | FR+EN | 🔴 |
| S2 Jan | ... | FAQ | FR | 🟡 |
| ... | | | | |

---

## Détail par article

### [Mois] — Article 1
**Titre FR :** [Titre optimisé question/réponse]
**Titre EN :** [Version anglaise adaptée pour requêtes touristiques]
**Angle :** [Ce qui rend cet article unique vs la concurrence]
**Requêtes cibles :**
  - FR : "[requête principale]", "[variante]"
  - EN : "[main query]", "[variant]"
**Blocs citables :** [Liste des 3-4 sous-questions à couvrir]
**Signaux E-E-A-T à inclure :** [Ex : "certif ISA instructeur", "depuis 2012", "X plongées guidées"]
**Infos à collecter auprès du client :** [Ce qu'on a besoin de lui demander]
**Format :** Article / FAQ / Guide / Comparatif / "Derrière la scène"
**Longueur cible :** [N mots] (dont [N] blocs de 134-167 mots)
**Date de publication idéale :** [Date — en lien avec la saisonnalité]
**Commande pour générer :** `/geo write-article <url> "[sujet]"`

---

[Répéter pour chaque article du calendrier]

---

## Résumé stratégique

### Gaps couverts ce trimestre
- [Gap 1] → couvert par articles [liste]
- [Gap 2] → couvert par articles [liste]

### Gaps restants (trimestre suivant)
- [Gap 1]
- [Gap 2]

### KPIs à suivre
- Nombre d'articles publiés vs planifiés
- Apparitions dans les réponses ChatGPT / Perplexity sur les requêtes cibles
- Évolution du GEO Score (mesurer avec `/geo compare` chaque mois)

---
*Calendrier généré par IA-Agency Polynésie — [date]*
*À revoir et ajuster chaque mois selon les résultats*
```

---

## Étape 5 — Présentation au client

Le calendrier est livré comme document de travail collaboratif.
Ajouter un bloc d'explication :

```markdown
## Comment utiliser ce calendrier

1. **Chaque semaine**, je prépare l'article indiqué dans le planning.
2. **Avant rédaction**, je vous envoie une courte liste de questions
   (les infos marquées "À collecter auprès du client").
3. **Après rédaction**, je vous livre l'article en FR et EN pour relecture.
4. **Publication** : soit vous publiez directement sur votre site,
   soit je m'en charge selon notre accord.
5. **Bilan mensuel** : je vous envoie un rapport d'évolution
   (quelles requêtes ont progressé, quels articles ont été cités par des IA).
```

---

## Output

Fichier : `CONTENT-CALENDAR-[nom]-[periode].md`

Enregistrer dans le CRM :
```
/geo prospect note <id> "Calendrier éditorial [N] mois créé — [date]"
```
