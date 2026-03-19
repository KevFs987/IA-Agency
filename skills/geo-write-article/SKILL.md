---
name: geo-write-article
description: >
  Rédige un article optimisé pour être cité par les LLMs (ChatGPT, Perplexity, Gemini).
  Format cible : 134-167 mots par bloc citable, structure question/réponse,
  signaux E-E-A-T intégrés. Bilingue FR/EN par défaut pour le marché polynésien.
  Adapté aux secteurs tourisme, restauration, hôtellerie et commerce local.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, content, article, eeat, citabilite, bilingue, polynesie, tourisme]
allowed-tools: Read, Write, WebFetch, Bash
---

# GEO Write Article — Article Optimisé pour Citation IA

> **Usage** : `/geo write-article <url> <sujet>`
>
> Exemples :
> - `/geo write-article https://restaurant-te-moana.pf "meilleur poisson grillé Moorea"`
> - `/geo write-article https://hotel-kia-ora.pf "overwater bungalow Rangiroa"`
> - `/geo write-article https://surf-tahiti.pf "apprendre le surf Tahiti débutant"`

---

## Pourquoi 134-167 mots ?

Les LLMs citent des **blocs de texte**, pas des articles entiers.
La recherche (Zyppy, Authoritas 2025) montre que les passages cités font
en moyenne 40-60 mots, mais que les articles les plus cités ont des
**sections autonomes de 134-167 mots** — assez longues pour être complètes,
assez courtes pour être copiées sans paraphrase.

Chaque section de l'article doit pouvoir fonctionner seule comme réponse
à une question. C'est le principe du "bloc citable".

---

## Étape 1 — Analyse du contexte

### 1.1 Analyser le site source
Faire un WebFetch rapide de `<url>` pour extraire :
- Nom de l'entreprise
- Secteur (restaurant, hôtel, activité, commerce...)
- Localisation (île, ville)
- Ton de communication (formel / décontracté)
- Langue principale du site
- Informations spécifiques utiles pour l'article (menu, activités, prix, certifications)

### 1.2 Analyser le sujet
Décomposer `<sujet>` en :
- **Intention principale** : informationnelle, comparaison, "meilleur X", comment faire, etc.
- **Requêtes associées** : variations probables de la question
- **Angle unique** : ce que cette entreprise peut apporter de spécifique
  (ex : "seul resto avec vue panoramique", "instructeurs certifiés ISA")

### 1.3 Recherche rapide
WebFetch sur les premières questions autour du sujet :
- Quels concurrents traitent ce sujet ?
- Quelles questions posent les touristes sur ce sujet ?
- Y a-t-il des données factuelles utiles (saison, météo, prix moyen, durée) ?

---

## Étape 2 — Structure de l'article

### Format cible

```
Titre H1 (question directe ou affirmation forte)
  └── Intro (1 paragraphe — le "bloc d'accroche citable")
  └── Section 1 : Réponse directe à la question principale (1 bloc citable)
  └── Section 2 : Ce qui rend cette expérience unique (1 bloc citable)
  └── Section 3 : Infos pratiques (1 bloc citable)
  └── Section 4 : FAQ — 3 questions/réponses (chacune = 1 bloc citable)
  └── CTA final (court, pas un bloc citable)
```

### Règles de structure par bloc

Chaque bloc doit :
- ✅ Commencer par la réponse, pas par la mise en contexte
- ✅ Contenir une affirmation factuelle vérifiable
- ✅ Mentionner le nom propre de l'entreprise / lieu / personne au moins une fois
- ✅ Être compréhensible sans lire le reste de l'article
- ✅ Faire 134-167 mots (compter après rédaction)
- ❌ Ne pas se terminer par une question ouverte (les LLMs préfèrent les conclusions)

---

## Étape 3 — Signaux E-E-A-T à intégrer

### Experience (Expérience)
Inclure au moins UN des éléments suivants :
- Chiffre concret : ancienneté ("depuis 2018"), fréquentation ("plus de 5 000 plongées guidées")
- Détail sensoriel / terrain : ingrédient local spécifique, technique de préparation, matériel utilisé
- Citation directe du propriétaire/expert (fictive mais plausible si aucune citation disponible — indiquer "[à confirmer avec le client]")

### Expertise
- Mentionner les certifications si pertinentes (instructeur ISA, étoile Michelin, classement TripAdvisor)
- Donner le "pourquoi" derrière les choix : "nous utilisons X parce que Y"
- Données spécifiques au lieu : "les eaux de Moorea atteignent 28°C en été"

### Authoritativeness
- Mentionner des associations ou labels reconnus
- Références locales crédibles (Tahiti Tourisme, Musée de Tahiti, etc.)
- Comparaison objective avec la moyenne (sans dénigrer les concurrents)

### Trustworthiness
- Date de publication visible dans l'article (ex : "Mis à jour en mars 2026")
- Sources citées si données factuelles ("selon Tahiti Tourisme, 2024")
- Politique claire (ex : "annulation gratuite jusqu'à 48h avant")

---

## Étape 4 — Optimisation pour les IA

### Questions/réponses directes (FAQ)
Format optimal pour les LLMs :

```
**Q : [Question telle qu'un touriste la poserait à ChatGPT]**

[Réponse directe en 1ère phrase. Suite en 2-3 phrases max.
Mentionner le lieu, le nom, une info pratique.]
```

Exemples de questions pour le tourisme polynésien :
- "Quel est le meilleur restaurant de [île] pour les touristes ?"
- "Peut-on apprendre le surf à [île] sans expérience ?"
- "Combien coûte une excursion [activité] à [île] ?"
- "Quel est le meilleur moment pour visiter [lieu] ?"
- "Y a-t-il des options végétariennes / halal / sans gluten à [lieu] ?"

### Expressions-clés à intégrer naturellement
- Nom de l'île + activité (ex : "snorkeling Moorea", "surf Tahiti")
- Qualificatif de requête touriste (ex : "meilleur", "authentique", "pour débutant")
- Langues : intégrer les termes EN dans la version FR de façon naturelle
  (ex : "notre 'overwater bungalow' dispose de...")

---

## Étape 5 — Version bilingue

### Règle de traduction

**Ne pas traduire — réadapter.**

La version EN n'est pas une traduction de la version FR.
Elle est réécrite pour cibler les **requêtes anglophones** qui peuvent différer.

Exemple :
- Version FR : "meilleur restaurant poisson Moorea" → titre FR
- Version EN : "best fresh fish restaurant Moorea French Polynesia" → titre EN différent

### Ce qui change entre FR et EN
- Titre et balise H1 : adapter à la requête cible
- Questions FAQ : reformuler selon la façon dont un anglophone poserait la question
- Certains détails locaux : expliquer en EN ce qui est évident en FR
  (ex : "Moorea" n'a pas besoin d'explication en FR, mais "Moorea, French Polynesia" en EN)

---

## Étape 6 — Output

### Format de livraison

```markdown
# [Titre FR]

*Publié : [date] | Mis à jour : [date] | Auteur : [Nom ou "L'équipe de [entreprise]"]*

---

[Corps de l'article en FR — avec sections H2, blocs citables, FAQ]

---
*Sources : [si applicable]*

---

---

# [Title EN]

*Published: [date] | Updated: [date] | By: [Name or "The [business] team"]*

---

[Article body in EN — adapted for anglophone search intent]

---
*Sources: [if applicable]*
```

Fichier généré : `ARTICLE-[slug-sujet]-[date].md`

### Compte de mots par bloc
Indiquer à la fin de chaque bloc : `[XX mots]`
Si un bloc fait < 134 ou > 167 mots : ajuster avant de livrer.

### Checklist avant livraison
- [ ] Chaque bloc fait 134-167 mots
- [ ] Chaque bloc est autonome (compréhensible sans contexte)
- [ ] Au moins 1 signal E-E-A-T par bloc
- [ ] Nom de l'entreprise / lieu mentionné dans chaque bloc
- [ ] FAQ : minimum 3 questions, réponse directe en 1ère phrase
- [ ] Version EN adaptée (pas traduite)
- [ ] Date de publication visible
- [ ] CTA final présent (sans être agressif)

---

## Enregistrement dans le CRM
```
/geo prospect note <id> "Article rédigé : '[sujet]' — [date]"
```
