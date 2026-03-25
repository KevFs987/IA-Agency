# Rapport Agency Status — 2026-03-21
*Généré par : /agency status — lecture seule, aucune modification effectuée*

---

## Vue d'ensemble

| Métrique | Valeur |
|---------|--------|
| Skills de base (référence fork) | 14 skills |
| Skills total dans le repo | 29 skills |
| Extensions IA-Agency ajoutées | 15 extensions |
| Agents total | 12 agents (5 audit classique + 5 social + 2 création) |
| CLAUDE.md présent | ✅ Oui — à jour (2026-03-20) |
| Skills originaux intacts | ✅ Tous présents |
| Installateur générique | ✅ `for skill_dir in "$SOURCE_DIR/skills"/*/` |

---

## Tableau d'avancement — Extensions CLAUDE.md

| Extension | Priorité | Statut | Fichier | Routing geo/SKILL.md | W | O | S |
|-----------|----------|--------|---------|---------------------|---|---|---|
| geo-social | HAUTE | ✅ | `skills/geo-social/SKILL.md` (469 lignes) | ✅ | ✅ | ✅ | ✅ |
| geo-discover | HAUTE | ✅ | `skills/geo-discover/SKILL.md` (364 lignes) | ✅ | ✅ | ✅ | ✅ |
| geo-readiness | HAUTE | ✅ | `skills/geo-readiness/SKILL.md` (262 lignes) | ✅ | ✅ | ✅ | ✅ |
| geo-outreach | HAUTE | ✅ | `skills/geo-outreach/SKILL.md` (297 lignes) | ✅ | ✅ | ✅ | ✅ |
| geo-teaser-report | HAUTE | ✅ | `skills/geo-teaser-report/SKILL.md` (257 lignes) | ✅ | ✅ | ✅ | ✅ |
| geo-prep-call | HAUTE | ✅ | `skills/geo-prep-call/SKILL.md` (310 lignes) | ✅ | ✅ | ✅ | ✅ |
| geo-social-to-site | MOYENNE | ✅ | `skills/geo-social-to-site/SKILL.md` (396 lignes) | ✅ | ✅ | ✅ | ✅ |
| geo-write-article | MOYENNE | ✅ | `skills/geo-write-article/SKILL.md` (229 lignes) | ✅ | ✅ | ✅ | ✅ |
| geo-rewrite-page | MOYENNE | ✅ | `skills/geo-rewrite-page/SKILL.md` (244 lignes) | ✅ | ✅ | ✅ | ✅ |
| geo-content-calendar | MOYENNE | ✅ | `skills/geo-content-calendar/SKILL.md` (247 lignes) | ✅ | ✅ | ✅ | ✅ |
| prospect scan | HAUTE | ✅ | `skills/geo-prospect/SKILL.md` (312 lignes) | ✅ | ✅ | ✅ | ✅ |

*W = Workflow en étapes numérotées, O = Outils déclarés, S = Sortie définie*

**Score fonctionnel : 11/11 — 100%**

---

## Problèmes critiques

Aucun problème bloquant le fonctionnement en production.

---

## Traces du fork identifiées 🔴

| # | Fichier | Ligne(s) | Contenu |
|---|---------|----------|---------|
| 1 | `README.md` | L.34 | `curl -fsSL https://raw.githubusercontent.com/KevFs987/IA-Agency/main/install.sh` |
| 2 | `README.md` | L.40 | `git clone https://github.com/KevFs987/IA-Agency.git` |
| 3 | Git remote | — | `origin = https://github.com/KevFs987/IA-Agency.git` |
| 4 | Git history | 10+ commits | Historique complet depuis le fork initial |

---

## Avertissements (non bloquants)

1. ⚠ **Livrables clients à la racine** — 12 fichiers de sortie (PDFs, MDs) traînent à la racine : à gitignorer.
2. ⚠ **geo-citations absent de la section Output Files** dans geo/SKILL.md (présent en Quick Reference et Sub-Skills).
3. ⚠ **knowledge/ très vide** — 2 fichiers seulement. Vault sous-alimenté.
4. ⚠ **Rapports agency-status en double** à la racine (2026-03-18, 2026-03-19).

---

## État du routeur (geo/SKILL.md)

| Commande | Quick Reference | Sub-Skills | Output Files |
|----------|----------------|------------|--------------|
| /geo readiness | ✅ | ✅ | ✅ |
| /geo teaser-report | ✅ | ✅ | ✅ |
| /geo outreach | ✅ | ✅ | ✅ |
| /geo prep-call | ✅ | ✅ | ✅ |
| /geo prospect scan | ✅ | ✅ | ✅ |
| /geo social-to-site | ✅ | ✅ | ✅ |
| /geo write-article | ✅ | ✅ | ✅ |
| /geo rewrite-page | ✅ | ✅ | ✅ |
| /geo content-calendar | ✅ | ✅ | ✅ |
| /geo citations | ✅ | ✅ | ⚠ absent |

---

## État de l'installateur

| Vérification | Statut | Détail |
|-------------|--------|--------|
| install.sh itère sur skills/* génériquement | ✅ | ligne 166 : `for skill_dir in "$SOURCE_DIR/skills"/*/` |
| install-win.sh présent | ✅ | variante Windows |

---

## Prochaines actions recommandées

### Immédiat — Reconstruction sans traces fork
1. Définir l'architecture cible (même structure ou refonte ?)
2. Créer un nouveau repo git propre
3. Écrire le nouveau `CLAUDE.md` comme pierre angulaire
4. Recréer skill par skill depuis le routeur `/geo/SKILL.md`

### Court terme
1. Ajouter `.gitignore` excluant `GEO-*.md`, `GEO-*.pdf`, `AGENCY-STATUS-*.md`
2. Corriger l'entrée Output Files manquante pour `/geo citations` dans `geo/SKILL.md`
3. Alimenter le `knowledge/` vault (données marché PF)

---

## Historique des rapports

| Date | Score extensions | Problèmes critiques | Notes |
|------|-----------------|--------------------|----- |
| 2026-03-18 | — | — | Premier rapport |
| 2026-03-19 | — | — | — |
| 2026-03-21 | 11/11 (100%) | 0 | Traces fork identifiées — reconstruction demandée |

---
*Rapport agency-status — généré en lecture seule — aucune modification effectuée*
*Prochain diagnostic : après reconstruction du repo*
