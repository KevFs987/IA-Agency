---
name: agency
description: >
  Outil de pilotage interne de l'agence IA-Agency Polynésie.
  Commandes de gestion et de diagnostic du repo, distinctes des commandes clients /geo.
  Utiliser quand l'utilisateur dit "agency", "status", "diagnostic", "avancement",
  "où en est le projet", "qu'est-ce qui manque", ou "/agency".
  Inclut aussi le skill-creator pour créer et modifier les skills du projet.
version: 1.0.0
author: IA-Agency Polynésie
tags: [agency, meta, diagnostic, status, pilotage, interne]
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Agency — Outil de Pilotage Interne

> **Commandes disponibles :**
>
> | Commande | Description |
> |----------|-------------|
> | `/agency status` | Auto-diagnostic complet du repo vs roadmap CLAUDE.md |
> | `/agency new-skill` | Créer ou modifier un skill du projet (skill-creator) |

---

## Routing

### `/agency status`

→ Charger et exécuter `skills/agency-status/SKILL.md`

### `/agency new-skill` (ou toute demande de création/modification de skill)

→ Charger et exécuter `skills/skill-creator/SKILL.md`

Workflow :
1. Cartographier le repo (Phase 1)
2. Analyser les additions du fork (Phase 2)
3. Comparer roadmap CLAUDE.md vs réalité (Phase 3)
4. Générer le rapport `AGENCY-STATUS-[date].md` + résumé inline (Phase 4)

**Règle fondamentale :** lecture seule — aucune modification de fichier existant.

---

## Extension future

D'autres commandes `/agency` pourront être ajoutées ici :

| Commande (future) | Description |
|------------------|-------------|
| `/agency changelog` | Résumé des évolutions du projet |
| `/agency clients` | Vue consolidée de tous les clients actifs |
