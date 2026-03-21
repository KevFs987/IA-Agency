---
name: geo-prospect
description: >
  CRM-lite for managing GEO agency prospects and clients. Track leads through
  the full sales pipeline: Lead → Qualified → Proposal Sent → Won → Lost.
  Store audit history, notes, deal values, and generate pipeline summaries.
  Includes automated local business discovery: scan a niche + city, score leads,
  filter below 50, generate a prioritized prospect list.
  Use when user says "prospect", "lead", "client", "pipeline", "crm", "scrape",
  "find prospects", "trouver prospects", or when managing the business side of GEO services.
version: 1.1.0
tags: [geo, business, crm, prospect, pipeline, sales, scraping, decouverte, polynesie]
allowed-tools: Read, Write, Bash, Glob, WebFetch
---

# GEO Prospect Manager

## Purpose

Manage GEO agency prospects and clients through the full sales lifecycle.
All data is stored in `~/.geo-prospects/prospects.json` (persistent across sessions).

---

## Commands

| Command | What It Does |
|---------|-------------|
| `/geo prospect new <domain>` | Create new prospect (interactive prompts) |
| `/geo prospect list` | Show all prospects with pipeline status |
| `/geo prospect list <status>` | Filter: lead, qualified, proposal, won, lost |
| `/geo prospect show <id-or-domain>` | Full prospect detail with history |
| `/geo prospect audit <id-or-domain>` | Run quick GEO audit and save to prospect record |
| `/geo prospect note <id-or-domain> "<text>"` | Add interaction note with timestamp |
| `/geo prospect status <id-or-domain> <new-status>` | Move through pipeline |
| `/geo prospect won <id-or-domain> <monthly-value>` | Mark as won, set contract value |
| `/geo prospect lost <id-or-domain> "<reason>"` | Mark as lost with reason |
| `/geo prospect pipeline` | Visual pipeline summary with revenue forecast |
| `/geo prospect scan "<niche>" "<ville>"` | Découverte automatique : recherche N entreprises locales, score chacune, filtre < 50 |

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Data Structure

Each prospect is stored as a JSON record:

```json
{
  "id": "PRO-001",
  "company": "Electron Srl",
  "domain": "electron-srl.com",
  "contact_email": "info@electron-srl.com",
  "contact_name": "",
  "industry": "Educational Equipment Manufacturing",
  "country": "Italy",
  "status": "qualified",
  "geo_score": 32,
  "audit_date": "2026-03-12",
  "audit_file": "~/.geo-prospects/audits/electron-srl.com-2026-03-12.md",
  "proposal_file": "~/.geo-prospects/proposals/electron-srl.com-proposal.md",
  "monthly_value": 0,
  "contract_start": null,
  "contract_months": 0,
  "notes": [
    {
      "date": "2026-03-12",
      "text": "Initial GEO quick scan. Score 32/100 - Critical tier. Strong candidate for GEO services."
    }
  ],
  "created_at": "2026-03-12",
  "updated_at": "2026-03-12"
}
```

---

## Orchestration Instructions

### `/geo prospect new <domain>`

1. Check if `~/.geo-prospects/prospects.json` exists, create if not (empty array)
2. Auto-detect company name from domain (e.g., `electron-srl.com` → `Electron Srl`)
3. Assign next sequential ID: `PRO-001`, `PRO-002`, etc.
4. Ask user for:
   - Contact name (optional)
   - Contact email
   - Monthly contract value estimate (optional)
5. Set status to `lead`
6. Save to JSON file
7. Suggest next step: "Run `/geo prospect audit electron-srl.com` to score this prospect"

### `/geo prospect list`

Read `~/.geo-prospects/prospects.json` and render a summary table:

```
GEO Prospect Pipeline — March 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID       Domain                  Company           Status      Score  Value
───────  ──────────────────────  ────────────────  ──────────  ─────  ──────
PRO-001  electron-srl.com        Electron Srl      Qualified   32/100  €4.5K
PRO-002  acme.com                ACME Corp         Lead        —       —
PRO-003  bigshop.it              BigShop           Won         41/100  €6.0K

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pipeline: 1 lead | 1 qualified | 0 proposals | 1 won | 0 lost
Committed MRR: €6,000 | Pipeline Value: €4,500
```

### `/geo prospect audit <id-or-domain>`

1. Run `/geo quick <domain>` to get GEO snapshot score
2. Save score to prospect record: `geo_score`, `audit_date`
3. Save audit output to `~/.geo-prospects/audits/<domain>-<date>.md`
4. Update `audit_file` path in prospect record
5. Add auto-note: "Quick audit run. GEO Score: XX/100."
6. If score < 55: suggest "Score indicates strong sales opportunity. Run `/geo proposal <domain>` to generate proposal."

### `/geo prospect note <id-or-domain> "<text>"`

1. Find prospect by ID or domain
2. Append note with current ISO date
3. Save back to JSON
4. Confirm: "Note added to Electron Srl (PRO-001)"

### `/geo prospect status <id-or-domain> <status>`

Valid statuses: `lead`, `qualified`, `proposal`, `won`, `lost`

1. Update status field
2. Add auto-note: "Status changed to <status>"
3. Save and confirm

### `/geo prospect pipeline`

Visual revenue-focused pipeline summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEO AGENCY PIPELINE SUMMARY — March 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STAGE          COUNT   POTENTIAL VALUE   NOTES
─────────────  ─────   ───────────────   ─────────────────────
Lead             2      €8,000/mo        New discoveries
Qualified        1      €4,500/mo        Ready for proposal
Proposal Sent    1      €6,000/mo        Awaiting signature
Won              3      €18,500/mo       Active clients (MRR)
Lost             1      —                Budget freeze

COMMITTED MRR:        €18,500
PIPELINE (qualified+): €10,500
TOTAL POTENTIAL:      €29,000/mo → €348,000/yr

Next actions:
→ PRO-003 (acme.com): Send proposal — score 38/100 (strong case)
→ PRO-007 (shop.it): Follow up — proposal sent 8 days ago
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Storage Location

All data stored in `~/.geo-prospects/`:
```
~/.geo-prospects/
├── prospects.json          # Main CRM database
├── audits/                 # Quick audit snapshots
│   └── electron-srl.com-2026-03-12.md
└── proposals/              # Generated proposals
    └── electron-srl.com-proposal.md
```

Create directory if it does not exist: `mkdir -p ~/.geo-prospects/audits ~/.geo-prospects/proposals`

---

## Pipeline Stage Definitions

| Status | Meaning | Typical Next Action |
|--------|---------|---------------------|
| `lead` | Discovered, not yet contacted | Run quick audit, assess opportunity |
| `qualified` | Audit done, confirmed pain points | Generate proposal |
| `proposal` | Proposal sent, awaiting decision | Follow up, answer questions |
| `won` | Contract signed, active client | Run full audit, start onboarding |
| `lost` | Deal closed lost | Log reason for future reference |

---

### `/geo prospect scan "<niche>" "<ville>"`

Commande de prospection automatisée — le cœur de la machine à leads.

**Flux d'exécution :**

1. **Recherche d'entreprises locales**

   Construire les URLs de recherche :
   ```
   https://www.google.com/maps/search/[niche]+[ville]+polynésie+française
   https://www.pagesjaunes.pf/annuaires/recherche?quoi=[niche]&ou=[ville]
   ```
   WebFetch de ces pages pour extraire :
   - Nom de l'entreprise
   - URL ou domaine (si disponible)
   - Adresse
   - Note Google / nombre d'avis
   - Numéro de téléphone

   Objectif : collecter 15-25 entreprises.

2. **Scoring rapide de chaque entreprise**

   Pour chaque entrée trouvée, lancer un mini-audit (30 secondes max) :
   - Si URL connue → `/geo quick <url>` → score GEO (0-100)
   - Si pas d'URL → `geo-discover "<nom>"` → score de maturité digitale (0-100)
   - Si aucune donnée suffisante → score estimé selon présence Maps + avis

3. **Filtrage et tri**

   - Garder uniquement les entreprises avec score < 50
   - Trier par score croissant (les plus faibles = opportunités les plus grandes)
   - Éliminer les entreprises déjà dans `~/.geo-prospects/prospects.json`

4. **Affichage du rapport de scan**

   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   SCAN PROSPECTS — "[niche]" à [ville] — [date]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   [N] entreprises trouvées → [M] avec score < 50 → [K] nouvelles

   Rang  Nom                   Score  URL/Présence         Action suggérée
   ────  ────────────────────  ─────  ───────────────────  ─────────────────────
    1    Restaurant Te Moana   18/100  Facebook only        Priorité haute
    2    Pension Chez Marie    24/100  Site basique         Priorité haute
    3    Surf School Tahiti    31/100  Site sans SEO        Priorité moyenne
    4    ...

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Prochaine étape : /geo prospect scan-add pour ajouter au CRM
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

5. **Ajout au CRM**

   Proposer d'ajouter les N meilleures opportunités au CRM :
   ```
   Voulez-vous ajouter ces [M] prospects au CRM ? (oui / sélectionner / non)
   ```
   Si oui → créer une entrée `lead` pour chacun avec les données trouvées.

**Limites et bonne pratique :**
- Les résultats dépendent de ce que Google Maps et Pages Jaunes exposent publiquement
- Le score rapide est une estimation — toujours confirmer avec un audit complet
- Ne pas envoyer le teaser-report sans audit complet préalable
- Respecter un délai de 1-2 secondes entre chaque fetch pour ne pas se faire bloquer

---

## Storage Location

All data stored in `~/.geo-prospects/`:
```
~/.geo-prospects/
├── prospects.json          # Main CRM database
├── audits/                 # Quick audit snapshots
│   └── electron-srl.com-2026-03-12.md
├── proposals/              # Generated proposals
│   └── electron-srl.com-proposal.md
└── scans/                  # Résultats de scan de niche
    └── restaurants-papeete-2026-03-18.md
```

Create directory if it does not exist:
`mkdir -p ~/.geo-prospects/audits ~/.geo-prospects/proposals ~/.geo-prospects/scans`

---

## Pipeline Stage Definitions

| Status | Meaning | Typical Next Action |
|--------|---------|---------------------|
| `lead` | Discovered, not yet contacted | Run quick audit, assess opportunity |
| `qualified` | Audit done, confirmed pain points | Generate teaser-report + outreach |
| `proposal` | Proposal sent, awaiting decision | Follow up, prep-call |
| `won` | Contract signed, active client | Run full audit, start onboarding |
| `lost` | Deal closed lost | Log reason for future reference |

---

## Output

- All commands print confirmation + current prospect status to terminal
- Scan results saved to `~/.geo-prospects/scans/`
- JSON database is the single source of truth
