---
name: agency-status
description: >
  Auto-diagnostic du repo IA-Agency — état actuel vs roadmap définie dans CLAUDE.md.
  Compare ce qui existe dans le repo avec ce qui devrait exister, identifie les gaps,
  évalue la qualité des skills, et produit un rapport d'avancement honnête.
  Usage interne — ne modifie aucun fichier existant.
version: 1.0.0
author: IA-Agency Polynésie
tags: [agency, status, diagnostic, roadmap, audit-interne, meta]
allowed-tools: Read, Glob, Grep, Bash
---

# Agency Status — Auto-Diagnostic du Repo

> **Usage** : `/agency status`
>
> Pas d'arguments — analyse le repo courant.

---

## Rôle

Tu es l'auditeur interne du projet IA-Agency.
Ton travail est d'analyser l'état réel du repo, de le comparer à la roadmap
définie dans CLAUDE.md, et de produire un rapport d'avancement honnête
avec les prochaines actions prioritaires.

**Tu ne génères pas de code. Tu observes, compares, et recommandes.**

---

## Workflow en 4 phases

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

### Phase 1 — Cartographie du repo

Identifier le répertoire racine du projet (là où est CLAUDE.md et install.sh).

Parcourir l'arborescence complète :

```
Glob("**/*")
```

Dresser l'inventaire par dossier :
- Nom du dossier
- Nombre de fichiers contenus
- Skill de base IA-Agency ou extension ?

**Skills de base (14) :**
`geo-audit`, `geo-brand-mentions`, `geo-citability`, `geo-compare`,
`geo-content`, `geo-crawlers`, `geo-llmstxt`, `geo-platform-optimizer`,
`geo-proposal`, `geo-prospect` (v1.0), `geo-report-pdf`, `geo-report`,
`geo-schema`, `geo-technical`

**Tout ce qui dépasse cette liste = extension IA-Agency.**

---

### Phase 2 — Analyse des additions

Pour chaque fichier ou dossier ajouté dans le fork :

1. Lire le contenu (Read)
2. Identifier la fonction : à quoi sert-il ?
3. Évaluer la complétude sur 3 critères :

| Critère | Question |
|---------|----------|
| Workflow | Le SKILL.md contient-il un workflow en étapes numérotées ? |
| Outils | Les `allowed-tools` sont-ils déclarés dans le frontmatter ? |
| Output | Un format de sortie (fichier ou affichage) est-il défini ? |

4. Vérifier si la commande est routée dans `/geo/SKILL.md` :

```
Grep pattern="geo social-to-site|geo-readiness|geo-discover|geo-social|geo-outreach|geo-teaser|geo-prep-call|write-article|rewrite-page|content-calendar|agency-status" fichier="geo/SKILL.md"
```

5. Vérifier si le skill est copié par `install.sh` :
- L'installateur itère-t-il sur `skills/*/` de façon générique ? → OK automatique
- Ou copie-t-il des fichiers en dur ? → vérifier si le skill est inclus

---

### Phase 3 — Comparaison roadmap vs réalité

Lire `CLAUDE.md` (Priorité absolue).

**Si CLAUDE.md est absent :**
→ Arrêter l'analyse et commencer le rapport par :

```
🚨 ALERTE CRITIQUE — CLAUDE.md ABSENT
Ce fichier est la mémoire stratégique du projet.
Son absence signifie que la roadmap n'est pas accessible à Claude.
Action immédiate requise : recréer CLAUDE.md depuis la dernière version connue.
```

**Si CLAUDE.md est présent :**

Extraire la liste complète des extensions définies et vérifier leur statut :

#### Extensions priorité HAUTE (CLAUDE.md section 4)

| Extension | Dossier attendu | Commande attendue dans SKILL.md |
|-----------|----------------|--------------------------------|
| geo-social | `skills/geo-social/` | `/geo audit https://facebook.com/...` |
| geo-discover | `skills/geo-discover/` | `/geo audit "Nom de marque"` |
| geo-readiness | `skills/geo-readiness/` | `/geo readiness <url-ou-nom>` |
| geo-outreach | `skills/geo-outreach/` | `/geo outreach <url-ou-nom>` |
| geo-teaser-report | `skills/geo-teaser-report/` | `/geo teaser-report <url-ou-nom>` |
| geo-prep-call | `skills/geo-prep-call/` | `/geo prep-call <url-ou-nom>` |

#### Extensions priorité MOYENNE (CLAUDE.md section 4)

| Extension | Dossier attendu | Commande attendue |
|-----------|----------------|-------------------|
| geo-social-to-site | `skills/geo-social-to-site/` | `/geo social-to-site <url-sociale>` |
| geo-write-article | `skills/geo-write-article/` | `/geo write-article <url> "<sujet>"` |
| geo-rewrite-page | `skills/geo-rewrite-page/` | `/geo rewrite-page <url>` |
| geo-content-calendar | `skills/geo-content-calendar/` | `/geo content-calendar <url> <mois>` |

#### Commandes commerciales (CLAUDE.md section 4)

| Commande | Skill/Mise à jour attendue |
|----------|--------------------------|
| `/geo prospect scan "<niche>" "<ville>"` | Mise à jour de `skills/geo-prospect/` |

#### Statuts possibles

| Statut | Définition |
|--------|------------|
| ✅ Complète | Dossier existe + SKILL.md complet (workflow + outils + output) + routé dans geo/SKILL.md |
| 🔶 Partielle | Fichier existe mais incomplet ou non connecté au routing |
| ❌ Absente | Aucun fichier trouvé |

#### Vérifications complémentaires

- **geo/SKILL.md** : les nouvelles commandes y sont-elles déclarées dans la Quick Reference ?
- **install.sh** : copie-t-il les skills de façon générique (`for skill_dir in skills/*/`) ?
- **README.md** : pointe-t-il vers le bon repo (KevFs987/IA-Agency) ?
- **CLAUDE.md** : a-t-il été mis à jour pour refléter les extensions développées ?

---

### Phase 4 — Génération du rapport

Construire le rapport complet en markdown.

---

## Template du rapport

```markdown
# Rapport Agency Status — [AAAA-MM-JJ]
*Généré par : /agency status — lecture seule, aucune modification effectuée*

---

## Vue d'ensemble

| Métrique | Valeur |
|---------|--------|
| Skills de base (référence) | 14 skills |
| Fichiers total | [N] fichiers |
| Extensions IA-Agency | [N - base] fichiers |
| CLAUDE.md présent | ✅ Oui / 🚨 Non |
| Skills originaux intacts | ✅ / ⚠ [détail si problème] |

---

## Tableau d'avancement — Extensions CLAUDE.md

| Extension | Priorité | Statut | Fichier(s) | Routing geo/SKILL.md | Qualité |
|-----------|----------|--------|------------|---------------------|---------|
| geo-social | HAUTE | ✅/🔶/❌ | [chemin] | ✅/❌ | [W:✓ O:✓ S:✓] |
| geo-discover | HAUTE | ... | | | |
| geo-readiness | HAUTE | ... | | | |
| geo-outreach | HAUTE | ... | | | |
| geo-teaser-report | HAUTE | ... | | | |
| geo-prep-call | HAUTE | ... | | | |
| geo-social-to-site | MOYENNE | ... | | | |
| geo-write-article | MOYENNE | ... | | | |
| geo-rewrite-page | MOYENNE | ... | | | |
| geo-content-calendar | MOYENNE | ... | | | |
| prospect scan | HAUTE | ... | | | |

*Qualité : W = Workflow en étapes, O = Outils déclarés, S = Sortie définie*

---

## Score d'avancement global

**[X] / 11 extensions implémentées ([X]%)**

Priorité HAUTE : [X]/6
Priorité MOYENNE : [X]/4
Commandes commerciales : [X]/1

---

## Problèmes critiques

*Blocages qui empêchent le fonctionnement en production.*

[Si aucun → "Aucun problème critique détecté."]

1. 🚨 [Problème critique #1 — description + impact]
2. 🚨 [Problème critique #2]

---

## Avertissements (non bloquants)

1. ⚠ [Avertissement #1]
2. ⚠ [Avertissement #2]

---

## Qualité des skills — détail

| Skill | Workflow | Outils | Output | Note |
|-------|----------|--------|--------|------|
| geo-social | ✅/❌ | ✅/❌ | ✅/❌ | [commentaire si problème] |
| geo-discover | ... | | | |
| geo-readiness | ... | | | |
| geo-teaser-report | ... | | | |
| geo-outreach | ... | | | |
| geo-prep-call | ... | | | |
| geo-social-to-site | ... | | | |
| geo-write-article | ... | | | |
| geo-rewrite-page | ... | | | |
| geo-content-calendar | ... | | | |

---

## État de l'installateur

| Vérification | Statut | Détail |
|-------------|--------|--------|
| install.sh itère sur skills/* génériquement | ✅/❌ | [ligne concernée] |
| Nouvelles skills détectées au dernier install | ✅/❌ | [N skills installées] |
| venv Python créé | ✅/❌ | [chemin] |
| Playwright installé | ✅/❌ | [requis pour PDF] |

---

## État du routeur (geo/SKILL.md)

| Commande | Présente dans Quick Reference | Présente dans Sub-Skills | Présente dans Output Files |
|----------|------------------------------|--------------------------|---------------------------|
| /geo readiness | ✅/❌ | ✅/❌ | ✅/❌ |
| /geo teaser-report | ... | | |
| /geo outreach | ... | | |
| /geo prep-call | ... | | |
| /geo prospect scan | ... | | |
| /geo social-to-site | ... | | |
| /geo write-article | ... | | |
| /geo rewrite-page | ... | | |
| /geo content-calendar | ... | | |

---

## Prochaines actions recommandées

### Cette semaine (priorité haute)
1. [Action concrète avec commande si applicable]
2. [Action concrète]

### Ce mois (priorité moyenne)
1. [Action concrète]
2. [Action concrète]

### Suggestions d'amélioration (non bloquantes)
- [Suggestion 1]
- [Suggestion 2]

---

## Historique des rapports

| Date | Score | Problèmes critiques | Notes |
|------|-------|--------------------|----- |
| [date] | [X]/11 | [N] | Premier rapport |

---
*Rapport agency-status — généré en lecture seule — aucune modification effectuée*
*Prochain diagnostic recommandé : dans 2 semaines ou après chaque sprint de développement*
```

---

## Output

1. **Sauvegarder** le rapport : `AGENCY-STATUS-[AAAA-MM-JJ].md` à la racine du repo
2. **Afficher** un résumé inline :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENCY STATUS — [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Extensions : [X]/11 complètes ([X]%)
Problèmes critiques : [N]
CLAUDE.md : ✅/🚨
Routeur geo/SKILL.md : ✅/⚠
Installateur : ✅/⚠
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rapport complet → AGENCY-STATUS-[date].md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Règles absolues

- ❌ Ne pas modifier un seul fichier existant (sauf créer le rapport)
- ❌ Ne pas exécuter de commandes de modification (git, rm, mv, sed...)
- ✅ Bash uniquement pour listing et comptage : `ls`, `wc -l`, `find -name`, `grep -c`
- Si un fichier est ambigu ou illisible : signaler plutôt que supposer
- Être honnête : un fichier avec 3 lignes ≠ "complété"
- Comparer à la roadmap CLAUDE.md, pas à une opinion subjective
