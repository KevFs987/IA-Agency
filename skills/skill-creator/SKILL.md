---
name: skill-creator
description: Crée de nouvelles skills, modifie et améliore les skills existantes du projet IA-Agency. Utilise quand l'utilisateur veut créer une skill depuis zéro, modifier une skill existante (geo-*, agency-*, autoresearch), tester une skill sur un cas réel, optimiser le description field pour un meilleur déclenchement, ou ajouter une nouvelle commande au routage /geo ou /agency. Se déclenche aussi quand l'utilisateur dit "crée un skill", "nouvelle commande", "ajoute une skill", "modifie la skill", "améliore le SKILL.md".
---

# Skill Creator — IA-Agency

Un skill pour créer et itérer sur les skills du projet IA-Agency.

## Architecture du projet (à connaître avant de toucher quoi que ce soit)

```
IA-Agency/
├── skills/[nom-du-skill]/SKILL.md   ← chaque skill a son propre dossier
├── geo/SKILL.md                     ← routeur principal des commandes /geo
├── agency/SKILL.md                  ← routeur des commandes /agency
└── agents/                          ← sous-agents réutilisables
```

**Règles d'architecture :**
- Chaque nouveau skill → dossier `skills/[nom]/SKILL.md`
- Toute nouvelle commande `/geo *` → mettre à jour `geo/SKILL.md` (Quick Reference + routing)
- Toute nouvelle commande `/agency *` → mettre à jour `agency/SKILL.md`
- Les skills geo polynésiens doivent gérer 3 types d'input : URL web, URL sociale (FB/IG/TikTok), nom de marque seul

---

## Processus de création

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

### Étape 1 — Comprendre l'intention

Commence par poser ces questions (sauf si la conversation fournit déjà les réponses) :

1. Qu'est-ce que ce skill doit faire exactement ?
2. Quelle commande déclenchera ce skill ? (ex : `/geo xxx <url>`)
3. Quel est le format de sortie attendu ? (rapport Markdown, PDF, message outreach, JSON…)
4. Quels tools sont nécessaires ? (WebFetch, Bash, Write, Read…)
5. Ce skill doit-il gérer les 3 types d'input polynésiens (site web / social / nom seul) ?

Si le contexte de la conversation montre déjà un workflow que l'utilisateur veut capturer (ex : "transforme ça en skill"), extrait les réponses directement depuis l'historique.

### Étape 2 — Recherche et contexte

Avant d'écrire, lis les skills existants pertinents pour t'aligner sur les patterns du projet :
- Un skill similaire dans `skills/` pour réutiliser la structure
- `geo/SKILL.md` pour voir comment le routage est organisé
- `CLAUDE.md` pour les contraintes métier (règles commerciales, marché PF, etc.)

Si le skill touche à la prospection ou aux rapports clients, relis **la section 5 du CLAUDE.md** (règle d'or : révéler le problème, taire la solution).

### Étape 3 — Écrire le SKILL.md

Structure minimale d'un bon SKILL.md dans ce projet :

```markdown
---
name: [nom-kebab-case]
description: [Ce que fait le skill + quand le déclencher. Sois "pushy" : liste les mots-clés qui doivent déclencher ce skill.]
allowed-tools:
  - Read
  - WebFetch
  - Write
  - Bash   # seulement si nécessaire
---

# [Titre du Skill]

## Objectif
[1-2 phrases sur pourquoi ce skill existe et ce qu'il produit]

## Input
[Types d'input acceptés : URL web / URL sociale / nom de marque]

## Workflow
[Étapes numérotées, claires et actionnables]

## Format de sortie
[Structure exacte de ce que le skill produit]

## Contraintes métier
[Règles spécifiques au projet : bilingue FR/EN, pas de tarifs dans les rapports clients, etc.]
```

#### Bonnes pratiques d'écriture

- **Explique le pourquoi**, pas seulement le quoi. Un LLM qui comprend la raison fait mieux que celui qui suit des règles aveugles.
- **Évite les MUSTs en majuscules en cascade.** Si tu te retrouves à écrire ALWAYS/NEVER/MUST partout, reformule avec une explication.
- **Sois bilingue dans les instructions** si le skill produit du contenu pour les clients (les outputs doivent souvent être FR/EN).
- **Reste sous 300 lignes** dans le SKILL.md principal. Si c'est plus long, crée des fichiers `references/` avec un pointeur clair.
- **La description frontmatter est le mécanisme de déclenchement principal** — inclus les mots-clés que l'utilisateur tapera.

#### Pattern description "pushy" (anti-undertriggering)

Au lieu de : `"Génère un message de prospection."`

Préfère : `"Génère un message de prospection personnalisé basé sur l'audit. Se déclenche quand l'utilisateur dit outreach, message, prospection, email, DM, WhatsApp, contact prospect, ou fournit une URL après /geo outreach."`

### Étape 4 — Cas de test

Prépare 2-3 prompts réalistes que l'utilisateur pourrait taper. Exemple :

```
/geo [nouvelle-commande] https://www.restaurant-te-moana.pf
/geo [nouvelle-commande] https://www.facebook.com/hotelbora
/geo [nouvelle-commande] "Resto Chez Manu Tahiti"
```

Soumets ces prompts à l'utilisateur : "Voici 3 cas de test. Est-ce que ça correspond à ce que tu veux tester ?"

Puis exécute-les toi-même en suivant le SKILL.md que tu viens d'écrire, et montre les résultats à l'utilisateur.

### Étape 5 — Mettre à jour le routage

Après validation du skill, mets à jour les fichiers de routage :

**Pour une commande `/geo *` :**
```bash
# Ajouter dans geo/SKILL.md :
# 1. Quick Reference (tableau des commandes)
# 2. Section de routage qui pointe vers skills/[nom]/SKILL.md
```

**Pour une commande `/agency *` :**
```bash
# Ajouter dans agency/SKILL.md
```

**Mettre à jour CLAUDE.md :**
- Section 11 "Extensions implémentées" → ajouter la ligne dans le tableau correspondant
- Si c'est une extension prioritaire, cocher la case ✅

### Étape 6 — Itérer

Après que l'utilisateur a vu les résultats des cas de test :

1. Identifie ce qui ne correspond pas aux attentes
2. **Généralise** le problème — ne corrige pas seulement pour ce cas précis, mais pour tous les cas similaires
3. Réécris le SKILL.md avec les améliorations
4. Reteste avec les mêmes prompts
5. Répète jusqu'à satisfaction

---

## Améliorer un skill existant

Si l'utilisateur veut modifier un skill existant (ex : "le skill geo-outreach n'est pas assez personnalisé") :

1. Lis le SKILL.md actuel en entier
2. Identifie les instructions qui causent le problème (pas seulement le symptôme)
3. Propose une réécriture ciblée — ne refais pas tout si seule une section pose problème
4. Teste sur un exemple concret avant de modifier le fichier
5. Applique la modification en conservant la structure existante

---

## Optimiser le déclenchement (description field)

Le champ `description` dans le frontmatter YAML est le principal mécanisme de déclenchement. Si un skill ne se déclenche pas assez souvent :

1. Liste 10 façons différentes dont l'utilisateur pourrait demander cette fonctionnalité
2. Intègre ces variations dans la description (mots-clés, synonymes, contextes)
3. Teste en relançant des prompts variés pour voir si le skill se déclenche

Exemple de description bien optimisée (skill geo-outreach) :
```
"Génère un message de prospection personnalisé basé sur les problèmes trouvés lors d'un audit.
Se déclenche quand l'utilisateur dit outreach, prospection, message, email, DM, WhatsApp,
contact, prise de contact, approcher un prospect, ou lance /geo outreach."
```

---

## Checklist avant de livrer un nouveau skill

- [ ] `skills/[nom]/SKILL.md` créé avec frontmatter valide (name + description)
- [ ] `allowed-tools` listé si le skill a besoin de tools spécifiques
- [ ] Les 3 types d'input polynésiens gérés (si pertinent) : URL web / social / nom
- [ ] Bilingue FR/EN dans les outputs si le skill produit du contenu client
- [ ] Règle commerciale respectée : pas de tarifs dans les rapports de prospection
- [ ] `geo/SKILL.md` ou `agency/SKILL.md` mis à jour avec la nouvelle commande
- [ ] `CLAUDE.md` section 11 mise à jour
- [ ] Au moins 1 test réel effectué sur un business polynésien ou similaire

---

## Référence rapide — skills existants

| Catégorie | Skills | Commandes |
|-----------|--------|-----------|
| Audit | geo-audit, geo-social, geo-discover | `/geo audit` |
| Rapport | geo-readiness, geo-report, geo-report-pdf, geo-teaser-report | `/geo readiness`, `/geo report` |
| Contenu | geo-write-article, geo-rewrite-page, geo-content-calendar, geo-social-to-site | `/geo write-article`, etc. |
| Prospection | geo-outreach, geo-prep-call, geo-prospect | `/geo outreach`, etc. |
| Technique | geo-schema, geo-technical, geo-crawlers, geo-llmstxt | `/geo schema`, etc. |
| Agence | agency-status | `/agency status` |

Lis `geo/SKILL.md` pour la liste complète et le routage exact.
