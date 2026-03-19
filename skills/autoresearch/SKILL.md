---
name: autoresearch
description: >
  Boucle d'optimisation autonome inspirée de Karpathy's autoresearch.
  Améliore un SKILL.md cible par itérations successives KEEP/DISCARD
  guidées par des tests automatisés. Principe : GOAL → LOOP → RÉSULTATS AU MATIN.
version: 1.0.0
author: IA-Agency Polynésie
tags: [autoresearch, optimization, loop, karpathy, meta, internal]
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Autoresearch — Optimiseur Autonome de Skills

> **Usage** : `/autoresearch <skill-name> [--iterations N]`
>
> Exemples :
> - `/autoresearch geo-teaser-report`
> - `/autoresearch geo-teaser-report --iterations 20`
> - `/autoresearch geo-outreach --iterations 10`

---

## Rôle

Tu es un optimiseur autonome de skills Claude Code.
Tu appliques la méthode Karpathy : définir une métrique, itérer,
garder ce qui améliore, rejeter ce qui dégrade.

Tu ne t'arrêtes pas tant que le seuil de qualité n'est pas atteint
ou que le nombre maximum d'itérations n'est pas dépassé.

---

## Outils autorisés

- Read — lire les fichiers du repo
- Write — modifier uniquement le SKILL.md ciblé
- Bash — exécuter les tests Python et git
- Glob — lister les fichiers
- Grep — chercher des patterns

---

## Skills disponibles

| Skill | Fichier goal | Fichier test |
|-------|-------------|--------------|
| geo-teaser-report | autoresearch/goals/geo-teaser-report.md | autoresearch/tests/check_teaser.py |
| geo-outreach | autoresearch/goals/geo-outreach.md | autoresearch/tests/check_outreach.py |
| geo-readiness | autoresearch/goals/geo-readiness.md | autoresearch/tests/check_readiness.py |
| geo-social | autoresearch/goals/geo-social.md | autoresearch/tests/check_social.py |
| geo-proposal | autoresearch/goals/geo-proposal.md | autoresearch/tests/check_proposal.py |

---

## Phase 0 — Initialisation

1. Lire le goal dans `autoresearch/goals/<skill-name>.md`
2. Lire le skill actuel dans `skills/<skill-name>/SKILL.md`
3. Lancer les tests initiaux pour obtenir le baseline :
   ```bash
   python autoresearch/tests/check_<skill-name>.py --batch autoresearch/examples/ --json
   ```
4. Si `autoresearch/examples/` ne contient pas de rapports pour ce skill,
   générer 3 rapports de test sur des cas représentatifs polynésiens :
   - Un hôtel / pension de famille (Bora Bora, Rangiroa, Moorea)
   - Un restaurant à Papeete
   - Un commerce local sans site web (nom de marque fictif)
   Sauvegarder dans `autoresearch/examples/<skill-name>/`
5. Noter le pass_rate baseline dans le log d'itération

---

## Phase 1 — Boucle principale

Pour chaque itération (défaut : 30 max) :

### Étape 1 — Analyser les échecs

```bash
python autoresearch/tests/check_<skill-name>.py --batch autoresearch/examples/ --json
```

- Lire les assertions qui ont échoué
- Identifier le pattern d'échec le plus fréquent
- Formuler une hypothèse : "Si je modifie X dans le SKILL.md, alors Y s'améliorera"

### Étape 2 — Sauvegarder l'état actuel

```bash
git add skills/<skill-name>/SKILL.md
git commit -m "autoresearch: iteration <N> baseline — pass_rate <X>%"
```

### Étape 3 — Modifier le SKILL.md

Appliquer **UNE SEULE** modification par itération.
Ne jamais changer plusieurs choses à la fois.

Types de modifications possibles :
- Reformuler les instructions de format de sortie
- Ajouter ou préciser une contrainte
- Ajouter un exemple concret de bon output
- Renforcer la règle sur les mots interdits
- Préciser le nombre de mots attendu par section
- Ajouter un contre-exemple (ce qu'il ne faut PAS faire)

### Étape 4 — Tester la modification

```bash
python autoresearch/tests/check_<skill-name>.py --batch autoresearch/examples/ --json
```

### Étape 5 — Décision KEEP ou DISCARD

**Si pass_rate augmente ou est égal → KEEP**
```bash
git add skills/<skill-name>/SKILL.md
git commit -m "autoresearch: iteration <N> KEEP — pass_rate <new>% (+<delta>%)"
```

**Si pass_rate diminue → DISCARD**
```bash
git checkout skills/<skill-name>/SKILL.md
```
Noter pourquoi cette modification n'a pas fonctionné.

### Étape 6 — Mettre à jour le log

Mettre à jour la table "Historique des itérations" dans `autoresearch/goals/<skill-name>.md`

### Étape 7 — Condition d'arrêt

- **STOP** si pass_rate >= seuil défini dans le goal
- **STOP** si iterations >= N (défaut : 30)
- **CONTINUE** sinon

---

## Phase 2 — Rapport final

Générer `autoresearch/results/<skill-name>-<date>.md` :

```markdown
# Autoresearch Results — <skill-name>
Date : <date>
Durée : <N> itérations

## Résumé
- Pass rate baseline : X%
- Pass rate final : Y%
- Gain : +Z%
- Statut : OBJECTIF ATTEINT / NON ATTEINT

## Top 3 modifications qui ont le plus aidé
1. <modification> → +X%
2. <modification> → +X%
3. <modification> → +X%

## Modifications rejetées
- <modification> → -X% (raison)

## SKILL.md final
[contenu du skill optimisé]
```

---

## Règles absolues — ne jamais enfreindre

1. **Un seul fichier modifiable par run** — uniquement `skills/<skill-name>/SKILL.md`
2. **Les tests ne sont jamais modifiés** — `autoresearch/tests/` est en lecture seule
3. **Le CLAUDE.md n'est jamais modifié**
4. **Git commit avant chaque modification** — l'historique est la mémoire du système
5. **Une seule modification par itération** — jamais deux changements simultanés
6. **Si pass_rate = 0 après modification** → rollback immédiat et stop

---

## Exemple de session

```
> /autoresearch geo-teaser-report --iterations 15

📋 Goal chargé : geo-teaser-report
📄 Skill actuel : skills/geo-teaser-report/SKILL.md
🧪 Baseline test...

Résultat baseline : 3/7 assertions (43%) — FAIL

🔁 Itération 1/15
  Échec dominant : assert_no_forbidden_words (jargon technique)
  Hypothèse : Ajouter une liste explicite de mots interdits dans le SKILL.md
  Modification appliquée → Test → 4/7 (57%) ↑ KEEP ✅

🔁 Itération 2/15
  Échec dominant : assert_cta_present
  Hypothèse : Ajouter instruction explicite sur la conclusion
  Modification appliquée → Test → 5/7 (71%) ↑ KEEP ✅

🔁 Itération 3/15
  Hypothèse : Reformuler le format de sortie avec plus de précision
  Modification appliquée → Test → 4/7 (57%) ↓ DISCARD ❌

...

🔁 Itération 8/15
  Pass rate : 6/7 (86%) ≥ 85% → OBJECTIF ATTEINT 🎉

📊 Rapport généré : autoresearch/results/geo-teaser-report-2026-03-19.md
```
