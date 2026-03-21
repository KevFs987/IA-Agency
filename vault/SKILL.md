---
name: vault
description: >
  Base de connaissances persistante du projet IA-Agency.
  Deux commandes : /vault research pour une recherche ciblée à la demande,
  /vault veille pour la veille mensuelle automatique sur 5 vecteurs.
  Le vault knowledge/ est le cerveau partagé de tous les skills du projet.
version: 1.0.0
author: IA-Agency Polynésie
tags: [vault, knowledge, research, veille, obsidian, intelligence]
allowed-tools: WebSearch, WebFetch, Read, Write, Glob
---

# Vault — Base de connaissances IA-Agency

> **Usage** :
> - `/vault research "<sujet>" [--category <cat>]` — veille ciblée à la demande
> - `/vault veille [--mois YYYY-MM]` — veille mensuelle automatique (5 vecteurs)

---

## Commandes disponibles

| Commande | Description |
|----------|-------------|
| `/vault research "<sujet>" [--category marche\|scoring\|inspiration\|sales\|marketing\|ooh-dooh\|concurrents\|prospects]` | Recherche web libre (WebSearch + WebFetch) → note structurée sauvegardée dans `knowledge/` |
| `/vault veille [--mois YYYY-MM]` | Veille mensuelle sur 5 vecteurs → rapport delta `knowledge/veille/veille-YYYY-MM.md` + notes individuelles |

---

## Routing

- Argument contient `research` → lire et exécuter `skills/vault-research/SKILL.md`
- Argument contient `veille` → lire et exécuter `skills/vault-veille/SKILL.md`

---

## Structure du vault

```
knowledge/
  index.md          ← index auto-mis à jour
  marche/           ← données marché Polynésie française
  scoring/          ← calibration et notes d'ajustement des scores
  concurrents/      ← benchmark concurrents et acteurs locaux
  prospects/        ← fiches prospects enrichies
  inspiration/      ← innovations importées (US, EU, CN, marchés comparables)
  sales/            ← techniques de vente, prospection, closing, pricing agences
  marketing/        ← marketing digital, campagnes, tactiques, social media
  ooh-dooh/         ← Out-of-Home et Digital Out-of-Home (affichage, billboards, aéroport PF)
  veille/           ← rapports delta mensuels
```

---

## Intégration avec les autres skills

Tous les skills du projet (`/geo`, `/agency`) lisent le vault en **Phase 0 optionnelle**
avant d'exécuter leur workflow principal.

Si `knowledge/` est vide ou absent : les skills fonctionnent normalement sans blocage.
Plus le vault est alimenté, plus les analyses, scores et livrables sont précis et contextualisés.
