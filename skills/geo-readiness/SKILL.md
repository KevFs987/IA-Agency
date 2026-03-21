---
name: geo-readiness
description: >
  Rapport de maturité digitale pour entreprises sans site web.
  Positionne l'entreprise sur un spectre 0-4 (zéro présence → GEO-ready)
  avec plan d'action concret et estimation de coût par niveau.
  Accepte une URL de site, une URL sociale, ou un nom de marque seul.
  Adapté au marché polynésien : ~50% des commerces locaux n'ont pas de site.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, readiness, maturite, prospection, polynesie, local, social]
allowed-tools: Read, Write, WebFetch, Bash, Glob
---

# GEO Readiness — Rapport de Maturité Digitale

> **Usage** : `/geo readiness <url-ou-nom>`
>
> Exemples :
> - `/geo readiness https://facebook.com/restaurant-te-moana`
> - `/geo readiness "Resto Te Moana Moorea"`
> - `/geo readiness https://hotel-kia-ora.pf`

---

## Objectif

Ce rapport remplace le GEO Score classique pour les entreprises qui n'ont pas (encore) de site web optimisé. Il est conçu pour deux usages simultanés :

1. **Outil de prospection** — créer la prise de conscience chez le prospect
2. **Premier livrable client** — feuille de route concrète livrable dès le premier RDV

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Étape 1 — Détection du type d'input

Analyser l'argument reçu :

| Input | Type | Action |
|-------|------|--------|
| URL contenant `facebook.com`, `instagram.com`, `tiktok.com` | Social URL | → Lancer `geo-social` pour extraire les données |
| URL avec domaine `.pf`, `.com`, `.fr`, etc. | Site web | → Fetch homepage + analyse rapide |
| Texte entre guillemets ou sans `http` | Nom de marque | → Lancer `geo-discover` pour rechercher les traces |

---

## Étape 2 — Collecte des données

### Si input = Site web
- Fetch homepage
- Vérifier robots.txt, sitemap.xml, HTTPS
- Détecter schema.org, Google Tag Manager, balises meta
- Vérifier présence sur Google Maps (chercher le nom dans le HTML ou title)
- Chercher liens vers réseaux sociaux

### Si input = URL sociale
- Extraire via `geo-social` : nom, description, abonnés, fréquence de posts, avis
- Chercher si un site web est mentionné dans le profil
- Chercher si Google Maps / TripAdvisor / Pages Jaunes existent pour ce nom

### Si input = Nom de marque
- Utiliser `geo-discover` : WebFetch sur Google, Maps, TripAdvisor, Pages Jaunes
- Reconstruire le profil de présence digitale complet

---

## Étape 3 — Calcul du Niveau de Maturité

### Les 5 Niveaux

```
NIVEAU 0 — Présence Zéro
Aucune trace digitale détectable.
Pas de site, pas de réseaux, pas de Google Maps, pas de mentions.
→ Le commerce est invisible pour quiconque cherche en ligne.

NIVEAU 1 — Social Only
Présence uniquement sur Facebook / Instagram / TikTok.
Pas de site web, pas de Google My Business, pas d'indexation Google.
→ Visible pour les abonnés existants, invisible pour les nouveaux clients.

NIVEAU 2 — Site Basique
Site web existant mais sans SEO : pas de meta tags, pas de schema,
vitesse médiocre, pas de version mobile optimisée.
Peut avoir ou non une présence sociale.
→ Indexé par Google mais non optimisé. Presque invisible.

NIVEAU 3 — SEO Traditionnel
Site avec SEO classique : meta, structure, mobile OK.
Mais pas de GEO : pas de schema avancé, pas de llms.txt,
crawlers IA non configurés, pas de présence sur plateformes IA.
→ Visible sur Google classique, invisible sur ChatGPT / Perplexity.

NIVEAU 4 — GEO-Ready (Cible)
Site + SEO + GEO complet : schema.org, llms.txt, crawlers IA autorisés,
présence sur Google Maps + TripAdvisor + plateformes d'autorité,
contenu structuré pour être cité par les LLMs.
→ Visible partout : Google, ChatGPT, Perplexity, Gemini.
```

### Critères de scoring par niveau

| Critère | Niveau 0 | Niveau 1 | Niveau 2 | Niveau 3 | Niveau 4 |
|---------|----------|----------|----------|----------|----------|
| Site web existant | ✗ | ✗ | ✓ | ✓ | ✓ |
| HTTPS | - | - | Variable | ✓ | ✓ |
| Présence sociale active | ✗ | ✓ | Variable | Variable | ✓ |
| Google My Business | ✗ | ✗ | Variable | Variable | ✓ |
| Meta tags / SEO base | - | - | ✗ | ✓ | ✓ |
| Schema.org | ✗ | ✗ | ✗ | Partiel | ✓ |
| llms.txt | ✗ | ✗ | ✗ | ✗ | ✓ |
| Crawlers IA autorisés | - | - | ✗ | Variable | ✓ |
| Contenu citable (LLM) | ✗ | ✗ | ✗ | Faible | ✓ |

---

## Étape 4 — Génération du Rapport

### Structure du rapport (output Markdown)

```markdown
# Rapport de Maturité Digitale — [Nom de l'entreprise]
**Date :** [Date]  **Analysé par :** GEO Readiness / IA-Agency

---

## Résumé Exécutif

[2-3 phrases : nom de l'entreprise, secteur, niveau actuel, et l'implication concrète
pour leur visibilité. Ton direct, pas de jargon.]

Exemple : "Resto Te Moana est actuellement au Niveau 1 — Social Only.
Votre page Facebook a 1 200 abonnés et un engagement régulier,
ce qui est un excellent point de départ. Cependant, vous êtes
actuellement invisible sur Google, ChatGPT et Perplexity — là où
vos clients touristes cherchent un restaurant avant d'arriver en Polynésie."

---

## Niveau Actuel : [X]/4 — [Nom du niveau]

[Description du niveau en 2-3 phrases adaptées à la réalité détectée.
Mentionner les signaux spécifiques trouvés : ex. "Votre page Facebook
compte X abonnés et vous postez en moyenne Y fois par semaine."]

### Ce qui a été détecté

| Élément | Statut | Impact |
|---------|--------|--------|
| Site web | ✓ Présent / ✗ Absent | [Impact business en 1 ligne] |
| Google My Business | ✓ / ✗ | [Impact] |
| Facebook | ✓ X abonnés / ✗ | [Impact] |
| Instagram | ✓ X abonnés / ✗ | [Impact] |
| TikTok | ✓ / ✗ | [Impact] |
| TripAdvisor | ✓ / ✗ | [Impact] |
| Pages Jaunes | ✓ / ✗ | [Impact] |
| Schema.org | ✓ / ✗ | [Impact] |
| Visible sur ChatGPT | ✓ / ✗ | [Impact] |

---

## Parcours vers le Niveau 4

[Phrase d'intro : "Voici le chemin concret depuis votre situation actuelle
jusqu'à une visibilité complète sur Google et les IA."]

### → Niveau [X+1] — [Nom] : Ce qu'il faut faire

**Actions concrètes :**
1. [Action spécifique et réalisable — ex. "Créer et vérifier votre fiche Google My Business"]
2. [Action 2]
3. [Action 3]

**Estimation :** [X heures de travail / X€ en autonomie ou X€ avec accompagnement]
**Délai réaliste :** [X jours / X semaines]

### → Niveau [X+2] — [Nom] : Ce qu'il faudra ensuite

[Idem pour le niveau suivant]

[Répéter jusqu'au Niveau 4]

---

## Impact Business Estimé

[Paragraphe court, ton direct, pas de promesses extravagantes.
Exemple : "Un touriste américain qui cherche 'best restaurant Moorea'
sur ChatGPT ou Google aujourd'hui ne vous trouvera pas.
Avec une présence Niveau 3-4, vous apparaissez dans ces réponses —
sans publicité payante."]

---

## Prochaine Étape

[CTA vers un appel de découverte. Ne pas mentionner de tarif.
Exemple : "Pour discuter de la marche à suivre adaptée à votre budget
et vos priorités, je suis disponible pour un appel de 30 minutes.
Pas d'engagement."]

---
*Rapport généré par IA-Agency Polynésie — [date]*
```

---

## Tone & Règles d'or

- **Langue** : Français par défaut, sauf si l'entreprise communique en anglais
- **Ton** : Direct, bienveillant, pas condescendant. On décrit une réalité, on ne juge pas.
- **Jamais de tarif** dans ce rapport — ce n'est pas le lieu
- **Jamais de solution trop détaillée** — le rapport montre le chemin, pas le mode d'emploi complet
- **Toujours un CTA** — ce rapport doit déclencher une conversation
- Adapter les exemples au secteur (restaurant, hôtel, commerce, service...)
- Si l'entreprise est dans le tourisme : mentionner explicitement les touristes qui cherchent en anglais sur ChatGPT/Google

---

## Estimations de coût par niveau (fourchettes marché polynésien)

À utiliser dans le rapport — ces fourchettes sont indicatives :

| De → Vers | En autonomie | Avec accompagnement |
|-----------|-------------|-------------------|
| 0 → 1 | Gratuit (ouvrir FB/Insta) | Non pertinent |
| 1 → 2 | 300-800€ (template site) | 600-1 500€ |
| 2 → 3 | 500-2 000€ (SEO) | 1 200-3 000€ |
| 3 → 4 | 800-2 500€ (GEO) | 2 000-5 000€ |
| 0 → 4 complet | 2 000-5 000€ | 4 000-10 000€ |

**Note :** Ces fourchettes ne doivent jamais apparaître dans le teaser-report.
Elles peuvent apparaître dans le rapport readiness complet livré APRÈS signature.

---

## Output

Fichier généré : `GEO-READINESS-[nom-entreprise]-[date].md`

Enregistrer aussi dans le CRM si un prospect existe :
`/geo prospect note <id> "Readiness audit : Niveau X/4"`
