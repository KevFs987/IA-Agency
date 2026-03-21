---
name: geo-teaser-report
description: >
  Génère un rapport de prospection volontairement incomplet — 2 pages max.
  Montre le score + 3 problèmes critiques + CTA vers un appel.
  NE contient JAMAIS les solutions, le plan d'action complet, ni aucun tarif.
  Règle d'or : révéler le problème, taire la solution.
  Destiné à être envoyé en prospection froide pour déclencher une conversation.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, prospection, teaser, commercial, outreach, pdf, polynesie]
allowed-tools: Read, Write, WebFetch, Bash, Glob
---

# GEO Teaser Report — Rapport Sniper de Prospection

> **Usage** : `/geo teaser-report <url-ou-nom>`
>
> Exemples :
> - `/geo teaser-report https://hotel-kia-ora.pf`
> - `/geo teaser-report "Restaurant Te Moana Moorea"`
> - `/geo teaser-report https://facebook.com/surf-tahiti`

---

## ⚠️ Règle Absolue — Gravée dans le marbre

> **RÉVÉLER LE PROBLÈME. TAIRE LA SOLUTION.**

Ce rapport est un outil commercial, pas un audit.
Son seul objectif : créer suffisamment de douleur pour déclencher un appel.

Ce rapport **NE DOIT JAMAIS contenir** :
- ❌ Les solutions aux problèmes identifiés
- ❌ Un plan d'action détaillé
- ❌ Toute mention de tarif ou de prestation
- ❌ Des recommandations techniques détaillées
- ❌ Plus de 2 pages de contenu

Ce rapport **DOIT contenir** :
- ✅ Le score global (chiffre + niveau)
- ✅ 3 problèmes critiques nommés (sans expliquer comment les résoudre)
- ✅ L'impact business estimé de chaque problème (en langage client, pas technique)
- ✅ Une question ouverte finale qui invite à l'appel
- ✅ Coordonnées de l'agence + lien de réservation appel

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Étape 1 — Collecte des données (si pas encore auditée)

Si l'entreprise n'a pas encore été auditée :
1. Détecter le type d'input (URL site / URL sociale / nom de marque)
2. Lancer l'audit approprié :
   - URL site → `/geo quick` (60 secondes)
   - URL sociale → `geo-social` (extraction rapide)
   - Nom → `geo-discover` (recherche rapide)
3. Extraire les données minimales nécessaires :
   - Score de maturité digitale (0-100)
   - Niveau de maturité (0-4)
   - Top 3 des problèmes les plus critiques (par impact business)
   - 1-2 points positifs (pour ne pas paraître agressif)

Si l'entreprise a déjà été auditée (données dans `~/.geo-prospects/`) :
→ Charger les données existantes du prospect

---

## Étape 2 — Sélection des 3 problèmes

Parmi tous les gaps détectés, choisir les **3 qui auront le plus d'impact émotionnel** sur le prospect.

Critères de sélection (dans l'ordre) :
1. **Argent perdu** — "vos clients vous cherchent et ne vous trouvent pas"
2. **Concurrents avantagés** — "votre concurrent X est visible, pas vous"
3. **Opportunité manquée** — "les touristes cherchent en anglais sur ChatGPT avant d'arriver"

### Bibliothèque de problèmes par catégorie

**Pour les restaurants / bars / cafés :**
- "Absent de Google Maps → [N]% des recherches 'restaurant [ville]' ne vous voient pas"
- "Pas de fiche TripAdvisor → invisible pour les touristes internationaux"
- "Invisible sur ChatGPT → quand un touriste demande 'best restaurant [île]', vous n'existez pas"
- "Pas de site web → impossible d'apparaître en résultat #1 sur Google"
- "Pas de système de réservation en ligne → perte estimée de X réservations/mois"

**Pour les hôtels / pensions de famille :**
- "Non listé sur les moteurs de réservation IA → vos concurrents captent vos clients"
- "Score Booking / TripAdvisor non optimisé → 60% des voyageurs lisent les avis avant de réserver"
- "Absent de 'best overwater bungalow [destination]' sur ChatGPT"
- "Pas de contenu en anglais → marché américain et australien inaccessible"

**Pour les commerces / boutiques :**
- "Horaires absents de Google → clients qui font le déplacement pour rien"
- "Pas de Google My Business → invisible dans les recherches locales 'près de moi'"
- "Zéro avis en ligne → les nouveaux clients ne peuvent pas vous faire confiance"

**Pour les activités / excursions :**
- "Non référencé sur les plateformes que consultent les croisiéristes avant embarquement"
- "Absent des réponses ChatGPT sur '[activité] [île]'"
- "Pas de présence Instagram → marché 25-45 ans qui planifie son voyage sur réseaux sociaux"

---

## Étape 3 — Génération du Rapport

### Template exact (ne pas dévier)

```markdown
---

# [Nom de l'entreprise]
## Analyse de Visibilité Digitale

*[Date] — Confidentiel — Préparé par IA-Agency*

---

## Score de Visibilité : [XX]/100

[Une seule phrase de contexte, neutre et factuelle.
Exemple : "Ce score reflète la capacité de [nom] à être trouvé
par de nouveaux clients sur Google et les intelligences artificielles."]

---

## Ce que nous avons trouvé

### ✓ Ce qui fonctionne
- [1-2 points positifs, brefs — montre l'objectivité de l'analyse]

### ⚠ Les 3 points critiques

---

**Problème #1 — [Titre court et impactant]**

[2-3 phrases maximum. Décrire le problème en langage client (pas technique).
Terminer par l'impact business concret.

Exemple :
"Votre restaurant n'apparaît pas dans les résultats Google Maps pour
'restaurant Moorea'. Quand un touriste cherche où dîner depuis son hôtel,
il voit vos concurrents — pas vous.
Cela représente une perte estimée de plusieurs dizaines de réservations par mois."]

---

**Problème #2 — [Titre court et impactant]**

[Même format : problème + impact en 2-3 phrases max]

---

**Problème #3 — [Titre court et impactant]**

[Même format]

---

## Une question pour vous

[Poser UNE seule question ouverte, simple, qui invite à réfléchir.
Ne pas y répondre dans le rapport.

Exemples :
- "Savez-vous combien de clients potentiels ont cherché '[type d'activité] [île]'
   sur Google le mois dernier — sans vous trouver ?"
- "Si vos trois concurrents les plus proches apparaissent sur ChatGPT
   quand un touriste américain planifie son séjour, est-ce que vous apparaissez aussi ?"
- "Combien de réservations directes (sans commission) auriez-vous pu capter
   si votre visibilité digitale était deux fois supérieure ?"]

---

## La suite

Je suis disponible pour un échange de 30 minutes pour vous expliquer
ce qui se passe exactement et ce que nous pourrions faire ensemble.

[Prénom] — IA-Agency Polynésie
📞 [Téléphone]
📧 [Email]
🗓 [Lien calendrier ou "Répondez à ce message pour convenir d'un appel"]

---
*Cette analyse a été préparée spécifiquement pour [nom].
Document non destiné à la diffusion.*

---
```

---

## Règles de ton et de style

- **Longueur** : 2 pages max. Si ça déborde → couper. Moins c'est plus.
- **Ton** : factuel, bienveillant, professionnel. Pas agressif. Pas vendeur.
- **Langue** : FR par défaut. Si l'entreprise est clairement anglophone → EN.
- **Chiffres** : utiliser des chiffres estimatifs quand possible (donnent de la crédibilité)
  - "plusieurs dizaines de réservations" plutôt que "des réservations"
  - Éviter les % précis non vérifiables
- **Mise en page** : sobre, lisible. Ce rapport peut être imprimé ou envoyé par email.
- **Pas de jargon** : SEO, GEO, schema, robots.txt → ces mots n'apparaissent PAS dans ce rapport

---

## Output

Fichier Markdown : `GEO-TEASER-[nom-nettoyé]-[date].md`

Optionnel — PDF :
Si Playwright est disponible :
```bash
~/.claude/skills/geo/venv/bin/python3 ~/.claude/skills/geo/scripts/generate_pdf_report.py \
  --mode teaser \
  --input GEO-TEASER-[nom]-[date].md \
  --output GEO-TEASER-[nom]-[date].pdf
```

Enregistrer dans le CRM :
```
/geo prospect note <id> "Teaser report généré le [date]"
/geo prospect status <id> qualified
```

---

## Flux recommandé (audit sniper complet)

```
1. /geo prospect new <domaine>                → créer la fiche prospect
2. /geo teaser-report <url-ou-nom>            → générer le PDF
3. /geo outreach <url-ou-nom>                 → rédiger le message d'envoi
4. [Envoi manuel du message + PDF]
5. [Appel entrant du prospect]
6. /geo prep-call <url-ou-nom>                → se préparer
7. [RDV — closing oral — tarif mentionné ici seulement]
```
