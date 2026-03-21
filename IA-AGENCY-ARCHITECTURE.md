# IA-Agency — Architecture & référentiel des skills
> Généré le 2026-03-20

---

## Vue d'ensemble

IA-Agency est une **agence marketing IA locale** construite sur Claude Code, ciblant le marché polynésien (et marchés émergents similaires). Extensions commerciales et workflows adaptés aux marchés où la majorité des entreprises n'ont pas de site web.

L'outil permet à une seule personne de gérer 15 à 20 clients avec les marges d'un logiciel, pas d'une agence traditionnelle.

---

## Structure de répertoires

```
IA-Agency/
├── CLAUDE.md                     # Mémoire stratégique du projet (lire avant tout)
├── README.md                     # Présentation publique
├── install.sh                    # Installateur one-command
│
├── geo/                          # Orchestrateur principal des commandes /geo
│   └── SKILL.md                  # Table de routage de 50+ commandes
│
├── agency/                       # Pilotage interne de l'agence
│   └── SKILL.md                  # Routage /agency status et /agency new-skill
│
├── skills/                       # 27 sous-skills (implémentations)
│   ├── geo-audit/
│   ├── geo-citability/
│   ├── geo-crawlers/
│   ├── geo-schema/
│   ├── geo-technical/
│   ├── geo-content/
│   ├── geo-social/
│   ├── geo-discover/
│   ├── geo-readiness/
│   ├── geo-outreach/
│   ├── geo-teaser-report/
│   ├── geo-prep-call/
│   ├── geo-prospect/
│   ├── geo-write-article/
│   ├── geo-rewrite-page/
│   ├── geo-content-calendar/
│   ├── geo-social-to-site/
│   ├── geo-report/
│   ├── geo-report-pdf/
│   ├── geo-proposal/
│   ├── geo-compare/
│   ├── geo-llmstxt/
│   ├── geo-brand-mentions/
│   ├── geo-crawlers-check/
│   ├── agency-status/
│   ├── skill-creator/
│   └── autoresearch/
│
├── agents/                       # 5 sous-agents spécialisés
│   ├── geo-technical.md
│   ├── geo-platform-analysis.md
│   ├── geo-schema.md
│   ├── geo-ai-visibility.md
│   └── geo-content.md
│
└── scripts/                      # Utilitaires Python (génération PDF, etc.)
```

---

## Principes architecturaux

### 1. Trois types d'input
Toutes les skills orientées marché gèrent trois cas :
- **Cas A** — URL de site web → audit GEO classique
- **Cas B** — URL sociale (Facebook / Instagram / TikTok) → audit social
- **Cas C** — Nom de marque seul → reconstruction de présence depuis zéro

### 2. Bilingue par défaut
Tout le contenu produit est pensé **FR/EN** — le français pour le marché local, l'anglais pour les touristes qui cherchent sur ChatGPT avant d'arriver en Polynésie.

### 3. GEO avant SEO
L'accessibilité aux crawlers IA (GPTBot, ClaudeBot, PerplexityBot…) et la citabilité dans les réponses LLM priment sur le SEO traditionnel. Le scoring reflète cette hiérarchie :

| Catégorie | Poids |
|-----------|-------|
| AI Citability | 25% |
| Brand Authority | 20% |
| Content E-E-A-T | 20% |
| Technical | 15% |
| Structured Data | 10% |
| Platform Optimization | 10% |

### 4. Règle commerciale d'or
> **Révéler le problème. Taire la solution.**

Aucun rapport de prospection ne contient de tarif ni de plan d'action détaillé. Les tarifs n'apparaissent que dans `/geo prep-call`, document confidentiel non partagé avec le prospect.

### 5. Philosophie read-only
Les skills de pilotage interne (`/agency status`, `/autoresearch`) ne modifient aucun fichier existant. Elles lisent, analysent, et produisent de nouveaux rapports.

---

## Flux de routage

```
Commande utilisateur
       │
       ▼
geo/SKILL.md  ──────────────────────────────────────────────────────────┐
       │                                                                  │
  /geo audit          /geo readiness       /geo prospect                 │
  /geo outreach        /geo write-article   /geo prospect scan            │
  /geo teaser-report   /geo rewrite-page    /geo prep-call                │
  /geo social-to-site  /geo content-calendar /geo compare                 │
  /geo report          /geo report-pdf       /geo proposal                │
       │                                                                  │
       ▼                                                                  │
skills/geo-[nom]/SKILL.md                                                 │
       │                                                                  │
       ▼ (si audit complet)                                               │
  Lance en parallèle 4 sous-agents :                                     │
  ├── agents/geo-technical.md                                             │
  ├── agents/geo-schema.md                                                │
  ├── agents/geo-ai-visibility.md                                         │
  └── agents/geo-content.md                                               │
       │                                                                  │
       ▼                                                                  │
  Synthèse → GEO-AUDIT-REPORT.md                                         │
                                                                          │
agency/SKILL.md ◄─────────────────────────────────────────────────────────┘
  /agency status → agency-status/SKILL.md
  /agency new-skill → skill-creator/SKILL.md
```

---

## Catalogue des skills

### Groupe 1 — Audit GEO (core)

#### `/geo audit <url-ou-nom>` → `skills/geo-audit/`
Orchestrateur principal. Lance un audit complet GEO+SEO en 3 phases :
1. Détection du type de business (SaaS, Local Business, E-commerce, Publisher…)
2. Lancement en parallèle des 4 sous-agents spécialisés
3. Synthèse avec score composite et plan d'action priorisé

**Output :** `GEO-AUDIT-REPORT.md`

---

#### `skills/geo-citability/`
Mesure la **citabilité IA** du contenu : est-ce qu'un LLM va citer ce texte dans une réponse ?

Scoring sur 5 dimensions :
| Dimension | Poids |
|-----------|-------|
| Answer Block Quality (blocs 134-167 mots) | 30% |
| Auto-suffisance (le bloc se comprend seul) | 25% |
| Lisibilité structurelle (H2/H3, listes) | 20% |
| Densité statistique (chiffres, dates, sources) | 15% |
| Unicité (angle différent de la masse) | 10% |

---

#### `skills/geo-crawlers/`
Analyse l'accès des **14 crawlers IA** au site (robots.txt, headers, blocages).

3 tiers de priorité :
- **Tier 1 (critique)** : GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot
- **Tier 2** : Google-Extended, Applebot-Extended, Amazonbot, FacebookBot
- **Tier 3** : CCBot, anthropic-ai, Bytespider, cohere-ai

Point clé : GPTBot et PerplexityBot n'exécutent pas le JavaScript — les sites SPA doivent servir du HTML statique.

---

#### `skills/geo-schema/`
Audit et génération de **données structurées Schema.org**.

Couvre 10+ types de schémas (Organization, LocalBusiness, Article, Product, FAQPage, SoftwareApplication, WebSite+SearchAction, Person, speakable). Accent particulier sur la stratégie `sameAs` (14+ liens vers des plateformes tierces) pour renforcer la reconnaissance d'entité par les LLMs.

---

#### `skills/geo-technical/`
Audit technique SEO en 8 catégories avec scoring sur 100 pts :

| Catégorie | Points |
|-----------|--------|
| Crawlabilité | 15 |
| Indexabilité | 12 |
| Sécurité (HTTPS, headers) | 10 |
| Structure URLs | 8 |
| Mobile | 10 |
| Core Web Vitals (LCP/INP/CLS) | 15 |
| Server-Side Rendering | 15 |
| Vitesse page | 15 |

---

#### `skills/geo-content/`
Évaluation qualité contenu via le framework **E-E-A-T** (25 pts par dimension) :
- **Experience** : témoignages, cas réels, données terrain
- **Expertise** : certifications, profondeur technique
- **Authoritativeness** : citations tierces, partenaires reconnus
- **Trustworthiness** : dates à jour, sources vérifiables, transparence

Cible de lisibilité Flesch : 60-70.

---

### Groupe 2 — Extensions marché polynésien

#### `/geo audit <url-sociale>` → `skills/geo-social/`
Audite une **présence sociale uniquement** (Facebook, Instagram, TikTok) quand l'entreprise n'a pas de site.

Extrait : nom de marque, description, type de contenu, fréquence de publication, signaux d'autorité (abonnés, avis, engagement). Identifie les gaps critiques (pas de site, pas de GMB, pas de schéma).

**Output :** Score de maturité digitale 0-100 avec roadmap.

---

#### `/geo audit "Nom de marque"` → `skills/geo-discover/`
Reconstruit une **présence digitale complète depuis un simple nom**. Cherche sur : Google Maps, TripAdvisor, Facebook, Instagram, Pages Jaunes Polynésie, Wikipedia…

**Output :** Profil consolidé avec liens `sameAs` et score.

---

#### `/geo readiness <url-ou-nom>` → `skills/geo-readiness/`
Positionne l'entreprise sur un **spectre de maturité à 5 niveaux** :

| Niveau | Description |
|--------|-------------|
| 0 | Aucune trace digitale |
| 1 | Social only (FB/IG/TikTok) |
| 2 | Site basique sans SEO |
| 3 | Site avec SEO traditionnel |
| 4 | GEO-ready (cible finale) |

Pour chaque niveau : plan d'action concret + estimation de coût + timeline. Ce rapport est à la fois l'outil de prospection ET le premier livrable client.

---

### Groupe 3 — Workflow commercial (prospecting)

#### `/geo prospect scan "<niche>" "<ville>"` → `skills/geo-prospect/`
**CRM-lite** intégré au terminal. Scrape Google Maps + Pages Jaunes, score 15-25 entreprises locales, filtre les scores < 50 (leads prioritaires).

Commandes disponibles : `new`, `list`, `show`, `audit`, `note`, `status`, `won`, `lost`, `pipeline`, `scan`.

Stockage JSON : `~/.geo-prospects/prospects.json`

Pipeline : lead → qualified → proposal → won/lost

---

#### `/geo outreach <url-ou-nom>` → `skills/geo-outreach/`
Génère un **message de prospection personnalisé** basé sur les problèmes réels trouvés — pas un template générique.

3 formats selon le canal :
- Email (professionnel, 150-200 mots)
- DM Instagram/Facebook (conversationnel, 80-100 mots)
- WhatsApp (ultra-court, 40-60 mots)

Disponible en FR et EN.

---

#### `/geo teaser-report <url-ou-nom>` → `skills/geo-teaser-report/`
**Rapport PDF 2 pages** conçu pour la prospection. Applique strictement la règle "révéler le problème, taire la solution" :

**CONTIENT :**
- Score global (ex : 34/100)
- 3 problèmes critiques nommés
- Impact business estimé
- CTA vers un appel

**NE CONTIENT PAS :**
- Les solutions
- Le plan d'action complet
- Tout tarif ou mention de prestation

**Output :** `GEO-TEASER-[nom]-[date].md` (+ PDF optionnel)

---

#### `/geo prep-call <url-ou-nom>` → `skills/geo-prep-call/`
**Briefing commercial confidentiel** avant un RDV prospect. Document jamais partagé.

Contient :
- Profil du prospect et situation digitale
- 3 douleurs à exploiter pendant le call
- 14 questions à poser (découverte)
- 6 objections probables avec réponses suggérées
- 3 tiers tarifaires avec pricing (c'est le **seul endroit** où les tarifs apparaissent)
- Structure du RDV (5-45 min)

---

### Groupe 4 — Production de contenu

#### `/geo write-article <url> "<sujet>"` → `skills/geo-write-article/`
Écrit un article optimisé pour la **citabilité IA** avec des blocs de 134-167 mots (longueur idéale pour être cité par un LLM).

Structure : Intro hero → Réponse directe → Angle unique → Info pratique → FAQ 3 questions → CTA.

Signaux E-E-A-T intégrés, bilingue FR/EN par défaut (adapté, pas traduit).

---

#### `/geo rewrite-page <url>` → `skills/geo-rewrite-page/`
Réécrit une page existante pour l'optimiser pour les LLMs :
- Premier paragraphe = réponse directe à la question principale
- Chaque H2 = question qu'un utilisateur poserait à ChatGPT
- Structure lisible par les crawlers IA

**Output :** Contenu réécrit + rapport de diagnostic avec scores E-E-A-T avant/après.

---

#### `/geo content-calendar <url> <mois>` → `skills/geo-content-calendar/`
Génère un **calendrier éditorial** sur N mois. Intègre les cycles touristiques polynésiens (Heiva en juillet, baleines mai-oct, surf mai-sept).

Scoring des sujets : Impact citabilité × Volume recherche × Facilité.
Stratégie bilingue : cible différentes langues selon la saison touristique.

---

#### `/geo social-to-site <url-sociale>` → `skills/geo-social-to-site/`
Récupère le contenu d'une page sociale (photos, descriptions, posts) et génère les **specs d'un site one-page bilingue FR/EN**. Réutilise ce que l'entreprise produit déjà — pas de contenu à créer from scratch.

---

### Groupe 5 — Rapports et livrables

#### `skills/geo-report/`
Rapport client complet en **12 sections**. Formule de scoring :

```
GEO Score = (Platform×0.25) + (Content×0.25) + (Technical×0.20) + (Schema×0.15) + (Brand×0.15)
```

---

#### `skills/geo-report-pdf/`
Génère un **PDF professionnel** via ReportLab (script Python). Contient : page de couverture, résumé exécutif, breakdown des scores avec graphiques, tableau des crawlers, plan d'action, annexes.

---

#### `skills/geo-proposal/`
Génère automatiquement une **proposition commerciale** à partir des données d'audit.

3 tiers de service :
| Tier | Prix |
|------|------|
| Basic | ~2 500 €/mois |
| Standard | ~5 000 €/mois |
| Premium | ~9 500 €/mois |

---

#### `/geo compare <url>` → `skills/geo-compare/`
Compare deux audits dans le temps (**tracking mensuel**). Affiche les deltas : scores, catégories, plateformes, crawlers. Indispensable pour les clients en retainer mensuel.

---

### Groupe 6 — Pilotage interne

#### `/agency status` → `skills/agency-status/`
Auto-diagnostic du dépôt vs le roadmap dans `CLAUDE.md`. En 4 phases :
1. Cartographie de ce qui existe
2. Analyse des ajouts non planifiés
3. Comparaison roadmap vs réalité
4. Génération du rapport

Vérifie les 11 extensions définies dans la roadmap.

**Output :** `AGENCY-STATUS-[AAAA-MM-JJ].md`

---

#### `/agency new-skill <nom>` → `skills/skill-creator/`
Crée ou améliore des fichiers `SKILL.md` en suivant les standards du projet :
- Structure frontmatter obligatoire
- Étapes de workflow
- Format de sortie
- Gestion des 3 types d'input
- Mise à jour du routage dans `geo/SKILL.md`
- Checklist pré-livraison

---

#### `skills/autoresearch/`
**Boucle d'optimisation autonome** (inspirée Karpathy). Améliore les skills par itération :

1. **Phase 0** — Initialisation : définir la métrique cible et le threshold
2. **Phase 1** — Boucle principale : analyser les échecs → backup → modifier UNE seule chose → tester → KEEP ou DISCARD
3. **Phase 2** — Rapport : résumé des changements, métriques avant/après

Stop automatique quand `pass_rate >= threshold` ou `iterations >= 30`.

Principe : une seule modification par itération pour isoler les causalités.

---

## Les 5 sous-agents

Les sous-agents sont des spécialistes appelés par `geo-audit` pour analyser en parallèle :

| Agent | Rôle | Spécialité clé |
|-------|------|----------------|
| `geo-technical.md` | Audit technique | Core Web Vitals, SSR, crawlabilité |
| `geo-platform-analysis.md` | Optimisation plateforme | Score par plateforme IA (ChatGPT, Perplexity, Gemini…) |
| `geo-schema.md` | Données structurées | JSON-LD, `sameAs`, schémas deprecated |
| `geo-ai-visibility.md` | Visibilité IA | Citabilité, brand mentions, Wikipedia |
| `geo-content.md` | Qualité contenu | E-E-A-T, détection contenu IA générique |

---

## Flux commercial complet

```
1. /geo prospect scan "restaurants" "Papeete"
   └─→ Liste de 20 leads scorés, filtrés < 50

2. /geo outreach <url prospect>
   └─→ Message personnalisé (Email / DM / WhatsApp)

3. /geo teaser-report <url prospect>
   └─→ PDF 2p : le problème sans la solution → crée la douleur

4. Prospect rappelle

5. /geo prep-call <url prospect>
   └─→ Briefing confidentiel : 14 questions, 6 objections, tarifs

6. Closing → le tarif n'apparaît que dans ce contexte oral
```

---

## État d'implémentation

| Extension | Commande | Statut |
|-----------|----------|--------|
| geo-social | `/geo audit https://facebook.com/...` | ✅ Complet |
| geo-discover | `/geo audit "Nom de marque"` | ✅ Complet |
| geo-readiness | `/geo readiness <url-ou-nom>` | ✅ Complet |
| geo-outreach | `/geo outreach <url-ou-nom>` | ✅ Complet |
| geo-teaser-report | `/geo teaser-report <url-ou-nom>` | ✅ Complet |
| geo-prep-call | `/geo prep-call <url-ou-nom>` | ✅ Complet |
| geo-social-to-site | `/geo social-to-site <url-sociale>` | ✅ Complet |
| geo-write-article | `/geo write-article <url> "<sujet>"` | ✅ Complet |
| geo-rewrite-page | `/geo rewrite-page <url>` | ✅ Complet |
| geo-content-calendar | `/geo content-calendar <url> <mois>` | ✅ Complet |
| geo-prospect scan | `/geo prospect scan "<niche>" "<ville>"` | ✅ Complet |
| agency-status | `/agency status` | ✅ Complet |
| skill-creator | `/agency new-skill` | ✅ Complet |

**Score : 13/13 — 100% implémenté**

---

*Document généré depuis l'état du dépôt au 2026-03-20.*
*Pour un rapport d'état en temps réel : `/agency status`*
