---
name: vault-veille
description: >
  Veille mensuelle automatique sur 5 vecteurs : marché PF, marchés comparables,
  marchés leaders (US/EU/CN), écosystème GEO/IA, et sales/marketing/OOH-DOOH.
  Produit un rapport delta mensuel + notes individuelles dans knowledge/.
  Invoqué par /vault veille [--mois YYYY-MM].
version: 1.0.0
author: IA-Agency Polynésie
tags: [vault, veille, intelligence, monthly, research, knowledge]
allowed-tools: WebSearch, WebFetch, Read, Write, Glob
---

# Vault Veille — Veille mensuelle automatique

> **Usage** : `/vault veille [--mois YYYY-MM]`
>
> Exemples :
> - `/vault veille` — veille du mois courant
> - `/vault veille --mois 2026-03` — veille pour mars 2026

---

## Objectif

Produire chaque mois une intelligence à 5 vecteurs qui :
1. **Détecte** les évolutions du marché local PF
2. **Importe** les meilleures pratiques des marchés comparables
3. **Anticipe** les innovations des marchés leaders (US, EU, CN)
4. **Suit** l'écosystème GEO/IA technique
5. **Surveille** les tendances sales, marketing digital et OOH/DOOH

Et positionne l'agence comme **force de proposition** auprès de ses clients polynésiens.

---

## Phase 1 — Initialisation

1. Déterminer la période :
   - Si `--mois YYYY-MM` fourni → utiliser cette valeur
   - Sinon → utiliser le mois courant au format `YYYY-MM`
2. Vérifier si un rapport existe déjà : `Glob("knowledge/veille/veille-<YYYY-MM>.md")`
   - Si trouvé → demander : "Un rapport pour [mois] existe déjà. Le remplacer ou créer une révision ?"
3. Afficher : `🔍 Démarrage de la veille [Mois YYYY] — 5 vecteurs en cours...`

---

## Phase 2 — Les 5 vecteurs de recherche

Effectuer les recherches de façon **séquentielle par vecteur** (WebSearch puis WebFetch des meilleures sources).

---

### Vecteur 1 — Marché Polynésie française

**Objectif** : Détecter les évolutions comportementales et économiques locales.

Requêtes WebSearch à lancer (adapter la date au mois de la veille) :
```
"marché digital Polynésie française [YYYY]"
"comportement consommateurs Tahiti réseaux sociaux [YYYY]"
"économie numérique Fenua TPE actualités [YYYY]"
"statistiques internet mobile Polynésie [YYYY]"
"ISPF DGEN rapport numérique entreprises [YYYY]"
```

Sources à prioriser dans les résultats :
- ispf.pf, service-public.pf/dgen, open.pf, ccism.pf
- datareportal.com (rapport Digital French Polynesia)
- tahiti-kiwi.com, webmaid.pf, tntvnews.pf, ladepeche.pf

Extraire : nouvelles statistiques, changements de comportement, actualités secteur digital local.

---

### Vecteur 2 — Marchés comparables

**Objectif** : Identifier des tactiques adaptables depuis des marchés similaires (insulaires, peu digitalisés).

Requêtes WebSearch :
```
"digital marketing small business Caribbean island [YYYY]"
"transformation numérique TPE Réunion Martinique Guadeloupe [YYYY]"
"social media business Pacific islands [YYYY]"
"marketing digital Nouvelle-Calédonie [YYYY]"
"agence digitale TPE marché émergent Afrique [YYYY]"
```

Extraire : cas clients, tactiques qui marchent, chiffres de résultats, adaptations culturelles.
Annoter chaque trouvaille avec : `📍 Depuis [pays/région] — Adaptable PF : [oui/non/partiel]`

---

### Vecteur 3 — Marchés leaders

**Objectif** : Importer les innovations avant qu'elles arrivent en Polynésie.

Requêtes WebSearch :
```
"AI marketing agency innovation [YYYY]"
"local business digital transformation US [YYYY]"
"GEO optimization agency best practices [YYYY]"
"restaurant hotel marketing AI tools [YYYY]"
"digital agency small business tools Europe [YYYY]"
```

Sources à prioriser : SparkToro, Ahrefs Blog, HubSpot Research, Think with Google, McKinsey Digital, Search Engine Journal.

Extraire : innovations, outils, tactiques émergentes, résultats mesurés.
Annoter chaque trouvaille avec : `🌍 Depuis [US/EU/CN/...] — Horizon PF : [immédiat/6 mois/12 mois+]`

---

### Vecteur 4 — Écosystème GEO/IA technique

**Objectif** : Suivre les évolutions techniques des outils qui définissent la visibilité IA.

Requêtes WebSearch :
```
"ChatGPT search update [YYYY]"
"Claude Anthropic new capabilities search [YYYY]"
"Perplexity AI search behavior [YYYY]"
"Google AI Overviews update [YYYY]"
"llms.txt adoption SEO [YYYY]"
"schema.org new types [YYYY]"
"GEO generative engine optimization update [YYYY]"
```

Sources à prioriser : openai.com/blog, anthropic.com/news, blog.perplexity.ai, developers.google.com/search, schema.org/docs.

Extraire : changements de comportement des moteurs IA, nouveaux formats de réponse, nouvelles pratiques recommandées.
Impact direct sur le scoring et les recommandations du projet.

---

### Vecteur 5 — Sales, Marketing & OOH/DOOH

**Objectif** : Rester à la pointe des techniques de vente agence et des formats publicitaires émergents.

Requêtes WebSearch :
```
"B2B agency sales techniques [YYYY]"
"digital agency pricing closing prospect [YYYY]"
"OOH DOOH advertising innovation [YYYY]"
"digital out-of-home airport retail [YYYY]"
"social media advertising ROI small business [YYYY]"
"content marketing strategy local business [YYYY]"
```

Extraire :
- Sales : nouvelles approches de prospection, scripts, outils CRM, méthodes de closing
- Marketing : nouveaux formats, plateformes émergentes, ROI mesuré, cas d'usage
- OOH/DOOH : innovations affichage, cas d'usage aéroport/retail, technologies DOOH

---

## Phase 3 — Synthèse croisée

Après les 5 vecteurs, identifier les **connexions entre vecteurs** :
- Une innovation leaders (V3) est-elle déjà présente dans un marché comparable (V2) ?
- Une évolution GEO/IA (V4) a-t-elle un impact sur le marché PF (V1) ?
- Une tactique sales (V5) peut-elle s'appliquer au contexte PF ?

Ces connexions génèrent les meilleures **idées d'implémentation**.

---

## Phase 4 — Rédaction du rapport delta

Produire le rapport complet :

**Fichier** : `knowledge/veille/veille-<YYYY-MM>.md`

```markdown
---
title: "Veille mensuelle [Mois YYYY]"
date: YYYY-MM-DD
type: veille-mensuelle
mois: YYYY-MM
vecteurs: [marche-pf, comparables, leaders, geo-ia, sales-marketing-ooh]
sources_total: N
---

# Veille mensuelle — [Mois YYYY]

> [N] sources analysées sur 5 vecteurs — Généré le [date] par `/vault veille`

---

## 🇵🇫 Évolutions marché PF

[Synthèse des changements détectés sur le marché polynésien ce mois-ci.
Statistiques nouvelles, tendances comportementales, actualités secteur digital local.]

**Signal fort du mois** : [la donnée la plus importante en 1 phrase]

---

## 🏝️ Inspirations marchés comparables

[Ce qui marche dans des contextes similaires (Caraïbes, DOM-TOM, Pacifique, Afrique).
Format : "📍 [Pays/Région] — [Tactique] — [Résultat mesuré] — Adaptable PF : [oui/partiel/non]"]

---

## 🌍 Innovations marchés leaders

[Ce qui émerge aux US, EU, CN et qu'on peut anticiper pour la PF.
Format : "🌍 [Pays] — [Innovation] — [Horizon d'adoption estimé en PF]"]

---

## ⚙️ Évolutions GEO/IA technique

[Changements détectés dans l'écosystème ChatGPT, Claude/Anthropic, Perplexity, Google AIO, schema.org, llms.txt.
Impact direct sur les recommandations et le scoring du projet.]

---

## 📣 Sales, Marketing & OOH/DOOH

[Nouvelles techniques de vente et closing, innovations marketing digital, tendances OOH/DOOH.
Idées directement applicables à la prospection et aux livrables clients.]

---

## 💡 Idées d'implémentation

[Nouveaux skills, commandes, ou fonctionnalités suggérés pour le projet IA-Agency
émergés de cette veille. Classés par priorité estimée.]

1. [Idée 1 — priorité haute/moyenne/faible]
2. [Idée 2]
3. [...]

---

## 📊 Impact sur les scores

[Ajustements suggérés aux pondérations des skills geo-social, geo-discover, geo-readiness, etc.
Basés sur les données fraîches de cette veille.]

---

*Rapport généré par `/vault veille` — IA-Agency Polynésie*
```

---

## Phase 5 — Notes individuelles et mise à jour de l'index

Pour chaque **trouvaille significative** (statistique clé, cas client, innovation importante) :
1. Si elle mérite une note dédiée (contenu suffisant) → créer une note dans la catégorie appropriée via le workflow de `skills/vault-research/SKILL.md` Phase 5-6
2. Update `knowledge/index.md` : ajouter le lien du rapport mensuel sous l'ancre `<!-- AUTO: veille links -->`

**Confirmation finale** :
```
✅ Rapport sauvegardé : knowledge/veille/veille-<YYYY-MM>.md
📊 Vecteurs couverts : 5/5
📚 Sources totales analysées : N
💡 Idées d'implémentation : X
📝 Notes individuelles créées : X
🗂️ Index mis à jour
```

**Affichage du rapport** :
Après la confirmation, lire et afficher intégralement le contenu de `knowledge/veille/veille-<YYYY-MM>.md` dans la conversation — pour que l'utilisateur puisse lire le rapport directement et s'en servir pour orienter ses décisions prospects et stratégiques.

---

## Règles importantes

- **Jamais de tarif** dans les rapports ou notes
- **Toujours dater les données** avec leur source et année
- **La section "Idées d'implémentation" est obligatoire** — c'est le moteur d'évolution du projet
- **Les connexions entre vecteurs** sont les insights les plus précieux — les chercher activement
- **Priorité au contexte PF** — extrapoler depuis les marchés comparables si données locales absentes
