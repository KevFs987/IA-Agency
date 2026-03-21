---
name: geo-social
description: >
  Audit de présence digitale depuis une URL de réseau social (Facebook, Instagram, TikTok).
  Pour les entreprises sans site web — cas dominant en Polynésie française.
  Architecture : extraction de base (Phase 1) + 5 agents spécialisés en parallèle (Phase 2)
  → Brand Entity AI, Local Listings, Cross-Platform Consistency, Content Quality, Sentiment.
  Produit un score de maturité digitale (0-100) et un diagnostic LLM complet.
version: 2.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, social, facebook, instagram, tiktok, polynesie, local, audit, llm, geo-ready]
allowed-tools: Read, Write, WebFetch, Bash, Agent
---

# GEO Social — Audit depuis Réseau Social

> **Usage** : invoqué par `/geo audit <social-url>` ou `/geo readiness <social-url>`
>
> Exemples :
> - `/geo audit https://facebook.com/restaurant-te-moana`
> - `/geo audit https://www.instagram.com/surf_tahiti/`
> - `/geo audit https://tiktok.com/@moncommerce`

---

## Objectif

Auditer la présence digitale d'une entreprise qui utilise les réseaux sociaux
comme **unique vitrine** — situation courante pour ~40% des commerces polynésiens.

Produire :
1. Un **profil de présence digitale** complet
2. Un **score de maturité digitale GEO** (0-100) — agrégat des 5 dimensions spécialisées
3. Les **gaps prioritaires** (ce qui manque et son impact sur les LLM)
4. Les **recommandations concrètes** adaptées au niveau réel
5. Les **livrables clients** : thermomètre LLM, plan avis, JSON-LD sameAs, kit contenu

## Architecture v2.0 — 5 agents spécialisés en parallèle

```
Phase 1 — Extraction de base (ce skill)
  ↓ données sociales brutes
  ↓
Phase 2 — 5 agents spécialisés lancés EN PARALLÈLE
  ├── geo-social-brand-ai      → Brand Entity Score (0-100)
  ├── geo-social-local-listings → Local Listings Score (0-100)
  ├── geo-social-cross-platform → Cross-Platform Score (0-100)
  ├── geo-social-content-quality → Content Quality Score (0-100)
  └── geo-social-sentiment     → Sentiment Score (0-100)
  ↓
Phase 3 — Agrégation + rapport final (ce skill)
  Score GEO Social = moyenne pondérée des 5 scores
```

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Étape 1 — Détection de la plateforme

| URL contient | Plateforme | Action |
|-------------|------------|--------|
| `facebook.com` | Facebook | → Extraction Facebook |
| `fb.com` | Facebook | → Extraction Facebook |
| `instagram.com` | Instagram | → Extraction Instagram |
| `tiktok.com` | TikTok | → Extraction TikTok |

---

## Étape 2 — Extraction des données sociales

### Facebook (`facebook.com/<page>`)

Faire un WebFetch de la page et extraire :

```
- Nom de la page
- Catégorie / type d'activité (restaurant, hôtel, commerce...)
- Description / À propos
- Nombre de "J'aime" / Abonnés
- Note moyenne et nombre d'avis (si visible)
- Adresse physique (si mentionnée)
- Numéro de téléphone (si mentionné)
- Site web listé dans le profil (si présent)
- Fréquence de publication (estimer depuis les posts visibles)
- Dernière date de publication
- Types de contenu : photos, vidéos, texte, événements
- Horaires d'ouverture (si mentionnés)
- Lien vers Instagram / TikTok (si mentionné)
```

### Instagram (`instagram.com/<handle>`)

```
- Nom du compte
- Bio (description)
- Nombre d'abonnés
- Nombre de publications
- Lien dans la bio (si site web mentionné)
- Fréquence de publication estimée
- Dernier post (date approximative)
- Présence de Reels / Stories highlights
- Email / contact dans le profil
```

### TikTok (`tiktok.com/@<handle>`)

```
- Nom du compte
- Bio
- Nombre de followers
- Nombre total de likes
- Nombre de vidéos
- Fréquence de publication estimée
- Lien dans la bio
```

**Note** : Les réseaux sociaux bloquent souvent le scraping.
Si le fetch retourne une page vide ou un login wall :
- Indiquer "Données partiellement accessibles — analyse basée sur les métadonnées disponibles"
- Utiliser les balises Open Graph dans le HTML (og:title, og:description)
- Continuer avec ce qui est disponible

---

## Étape 2.5 — Packaging des données pour les agents

Après l'extraction (étape 2), consolider un objet `social_context` à passer aux 5 agents.

### 2.5a — Détermination du secteur_type

Le `secteur_type` est utilisé par les agents pour ajuster leurs sous-critères internes
*avant* de calculer leur score 0-100. Il doit être déterminé ici, une seule fois.

| business_type | secteur_type |
|--------------|-------------|
| restaurant / snack / food truck / café | `tourisme` |
| hôtel / pension / resort / chambre d'hôtes | `tourisme` |
| activité touristique / excursion / plongée | `tourisme` |
| commerce de détail / boutique | `commerce_mixte` |
| bar / discothèque | `commerce_mixte` |
| coiffeur / esthétique / spa (local) | `service_local` |
| plombier / électricien / artisan | `service_local` |
| médecin / cabinet médical | `service_local` |
| autre / inconnu | `commerce_mixte` |

### 2.5b — Résolution des conflits de nom

Avant de passer `brand_name` aux agents, déterminer le nom canonique selon l'ordre de priorité :

1. **Registre du commerce PF (RCCM)** — si fourni par le client → priorité absolue
2. **GBP vérifiée** — si fiche vérifiée trouvée à l'étape 3 → second rang
3. **Nom Facebook** — page professionnelle → référence par défaut
4. **Nom Instagram** — si pas de Facebook

Documenter : `canonical_name_source: rccm / gbp_verified / facebook / instagram`

Si des agents remontent des variantes de nom en phase 2, la règle de résolution
est : **la source prioritaire ci-dessus l'emporte**. L'orchestrateur (ce fichier)
consolide avant de construire le rapport final.

### 2.5c — Chargement des seuils LLM

```bash
# Lire les seuils depuis le fichier de configuration unique
cat config/llm-thresholds.json
```

Ne jamais coder les seuils en dur dans ce fichier ni dans les agents.
Toute mise à jour des seuils se fait dans `config/llm-thresholds.json` uniquement.

### 2.5d — Objet social_context final

```json
{
  "brand_name":            "[nom canonique — voir 2.5b]",
  "canonical_name_source": "[rccm / gbp_verified / facebook / instagram]",
  "brand_variants":        "[variantes détectées, séparées par virgule]",
  "business_type":         "[restaurant / hôtel / commerce / activité / service / autre]",
  "secteur_type":          "[tourisme / commerce_mixte / service_local — voir 2.5a]",
  "location":              "[ville + île]",
  "phone":                 "[+689 XX XX XX XX ou absent]",
  "address":               "[adresse ou absent]",
  "website_listed":        "[URL ou absent]",
  "facebook_url":          "[URL ou absent]",
  "instagram_url":         "[URL ou absent]",
  "tiktok_url":            "[URL ou absent]",
  "followers":             "[N]",
  "last_post_date":        "[date]",
  "post_frequency":        "[posts/semaine estimé]",
  "bio_text":              "[texte complet de la bio]",
  "account_type":          "[personnel / page_pro / inconnu]",
  "llm_thresholds":        "[objet lu depuis config/llm-thresholds.json]"
}
```

---

## Phase 2 — Lancement des 5 agents en parallèle

Lancer les 5 agents **simultanément** en passant le `social_context` à chacun.
Ne pas attendre la fin d'un agent pour lancer le suivant.

> **Mode rapide (`--quick`)** : lancer uniquement les agents listings + sentiment.
> Formule alternative : `Score Quick = score_listings × 0.50 + score_sentiment × 0.50`
> Afficher dans le rapport : "⚠️ Score partiel — 2 agents sur 5 exécutés.
> Lancer `/geo audit [url]` pour l'analyse complète (5 agents)."

```
LANCEMENT PARALLÈLE :

Agent 1 → Read agents/geo-social-brand-ai.md
          Données : social_context complet
          Objectif : Brand Entity Score + diagnostic citations LLM

Agent 2 → Read agents/geo-social-local-listings.md
          Données : brand_name, business_type, location
          Objectif : Local Listings Score + chaîne alimentation LLM

Agent 3 → Read agents/geo-social-cross-platform.md
          Données : social_context + URLs agents 1-2
          Objectif : Cross-Platform Score + JSON-LD sameAs généré

Agent 4 → Read agents/geo-social-content-quality.md
          Données : social_context (bio, fréquence, account_type)
          Objectif : Content Quality Score + kit quick wins contenu

Agent 5 → Read agents/geo-social-sentiment.md
          Données : brand_name, business_type, location, plateformes
          Objectif : Sentiment Score + thermomètre LLM + plan avis
```

Collecter les outputs de chaque agent :

```
agent_scores:
  brand_ai:        [0-100] + gaps_list
  local_listings:  [0-100] + gaps_list
  cross_platform:  [0-100] + json_ld_block + gaps_list
  content_quality: [0-100] + templates_list + gaps_list
  sentiment:       [0-100] + thermometre_llm + plan_avis + gaps_list
```

---

## Étape 3 — Recherche de présence complémentaire

Après extraction sociale, rechercher les traces complémentaires :

1. **Google Maps** : chercher le nom de l'entreprise sur Google Maps
   - `WebFetch https://www.google.com/maps/search/[nom+encodé]`
   - Détecter : fiche GMB existante ?, note ?, nombre d'avis ?

2. **Site web** : si un URL est mentionné dans le profil social
   - Vérifier que le site répond (status 200)
   - Version mobile ? HTTPS ? Vitesse approximative ?

3. **TripAdvisor** (si restaurant / hôtel / activité)
   - `WebFetch https://www.tripadvisor.fr/Search?q=[nom+encodé]`

4. **Pages Jaunes Polynésie**
   - `WebFetch https://www.pagesjaunes.pf/`

---

## Phase 3 — Agrégation des scores et Score GEO Social final

### Formule d'agrégation

Le Score GEO Social final est une **moyenne pondérée** des 5 scores spécialisés.
Pondération calibrée pour le marché PF (fort tourisme, priorité LLM) :

| Agent | Score | Poids | Justification |
|-------|-------|-------|--------------|
| Sentiment & Reputation | [0-100] | **25%** | Levier n°1 sur les LLM — la note débloque ou bloque tout |
| Local Listings | [0-100] | **25%** | GBP = alimentation directe Gemini + ChatGPT |
| Brand Entity AI | [0-100] | **20%** | Reconnaissance entité = citabilité LLM long terme |
| Content Quality | [0-100] | **15%** | Contenu citable = visibilité Perplexity et ChatGPT |
| Cross-Platform | [0-100] | **15%** | Cohérence NAP = unification entité LLM |

```python
score_geo_social = (
    score_sentiment       * 0.25 +
    score_local_listings  * 0.25 +
    score_brand_ai        * 0.20 +
    score_content_quality * 0.15 +
    score_cross_platform  * 0.15
)
# Arrondi à l'entier le plus proche
```

> **Contexte marché PF (DataReportal jan. 2025)** : TikTok atteint 67,5% des adultes 18+ en PF,
> quasi-parité avec Facebook (82,3%). Messenger actif (badge réponse rapide < 15 min) = signal
> de contact fort à noter dans les informations de contact lors de l'extraction (étape 2).

### Score → Niveau de maturité digitale GEO

| Score | Niveau | Interprétation LLM |
|-------|--------|--------------------|
| 0-20 | Niveau 0 | Invisible — aucun LLM ne peut citer cet établissement |
| 21-40 | Niveau 1 | Social only — bases absentes, LLM ne cite pas |
| 41-60 | Niveau 1-2 | Social actif mais gaps critiques LLM non comblés |
| 61-80 | Niveau 2-3 | Bonne base — commence à apparaître dans Gemini/Perplexity |
| 81-100 | Niveau 3-4 | GEO-ready — citable par ChatGPT, Perplexity et Gemini |

---

## Phase 3 — Génération du Rapport Final

### Structure du rapport

```markdown
# Audit GEO Social — [Nom de l'entreprise]
**Plateforme analysée :** [Facebook / Instagram / TikTok]
**URL :** [url]
**Date :** [date]
**Type de présence :** [Social only / Multiplateforme]

---

## Score GEO Social : [XX]/100

[Une phrase de contexte : "Ce score mesure votre visibilité sur les moteurs
de recherche IA — ChatGPT, Perplexity, Gemini — pas seulement votre présence
sur [plateforme]. C'est là que vos futurs clients touristes cherchent avant
même d'arriver en Polynésie."]

### Détail par dimension

| Dimension | Score | Poids | Contribution |
|----------|-------|-------|-------------|
| Réputation & Avis | [XX]/100 | 25% | [XX] pts |
| Annuaires locaux | [XX]/100 | 25% | [XX] pts |
| Entité de marque IA | [XX]/100 | 20% | [XX] pts |
| Qualité du contenu | [XX]/100 | 15% | [XX] pts |
| Cohérence multi-plateformes | [XX]/100 | 15% | [XX] pts |
| **Score final** | | | **[XX]/100** |

---

## 🌡️ Thermomètre LLM

| Moteur IA | Note actuelle | Seuil requis | Statut |
|----------|--------------|-------------|--------|
| ChatGPT | [X.X★ / N avis] | 4,3★ | ✅ Actif / ❌ Non actif |
| Perplexity | [X.X★ TripAdvisor] | 4,1★ | ✅ Actif / ❌ Non actif |
| Gemini | [X.X★ Google Maps] | 3,9★ | ✅ Actif / ❌ Non actif |

---

## Ce que nous avons trouvé

### Présence sur [Plateforme]
| Élément | Valeur | Signal LLM |
|---------|--------|-----------|
| Type de compte | [Page pro / Compte personnel ⚠️] | [Fort / Faible] |
| Abonnés | [N] | [Contexte marché local] |
| Fréquence de publication | [X posts/semaine] | [Actif / Irrégulier / Inactif] |
| Dernier post | [date] | [Récent / ⚠️ > 3 mois] |
| Bio bilingue FR/EN | ✓ / ✗ | [Touristes accessibles / Invisible EN] |
| Infos de contact | ✓ / ✗ | [NAP signal présent / absent] |

### Présence sur les annuaires
| Plateforme | Statut | LLM alimenté |
|-----------|--------|-------------|
| Google Business Profile | ✅ Vérifiée / ⚠️ Auto / ❌ Absente | Gemini + ChatGPT |
| TripAdvisor | ✅ [X★, N avis] / ❌ Absent / N.A. | Perplexity |
| Pages Jaunes PF | ✅ / ❌ | Perplexity + Google |
| Site web | ✅ [url] / ❌ Absent | — |

---

## Les 3 Gaps Prioritaires

### Gap 1 — [Titre du gap le plus impactant]
**Problème :** [Description en 1-2 phrases]
**Ce que ça veut dire :** [Impact LLM concret — ex : "Vos clients touristes qui
demandent 'meilleur restaurant Moorea' à ChatGPT ne vous trouvent pas."]
**Délai de correction :** [X min / X heures / X semaines]

### Gap 2 — [Titre]
**Problème :** [...]
**Ce que ça veut dire :** [...]
**Délai de correction :** [...]

### Gap 3 — [Titre]
**Problème :** [...]
**Ce que ça veut dire :** [...]
**Délai de correction :** [...]

---

## Plan Avis (si note < seuil ChatGPT)

Pour apparaître dans les recommandations ChatGPT (seuil 4,3★) :
→ **[N] avis 5★ supplémentaires** nécessaires
→ Pour Perplexity (4,1★) : **[N] avis** _(ou déjà atteint ✅)_
→ Pour Gemini (3,9★) : **[N] avis** _(ou déjà atteint ✅)_

---

## Kit Quick Wins Contenu

[Inclure les templates générés par geo-social-content-quality
correspondant aux gaps détectés — uniquement les templates pertinents,
personnalisés avec les données réelles]

---

## Bloc sameAs JSON-LD (livrable technique)

[Reproduire le bloc JSON-LD généré par geo-social-cross-platform]
_À intégrer dans le futur site web — conservez ce document._

---

## Recommandations Prioritaires (classées par ROI)

1. **[Action 1 — impact maximum / effort minimum]**
   → [Description concrète] — [Délai estimé]

2. **[Action 2]**
   → [Description] — [Délai]

3. **[Action 3]**
   → [Description] — [Délai]

---

## Prochaine Étape

[CTA vers un appel de découverte. Pas de tarif. Ex : "Si vous voulez
comprendre exactement ce qui manque et comment y remédier,
je suis disponible pour un appel de 30 minutes."]

---
*Audit GEO Social v2.0 — IA-Agency Polynésie — [date]*
```

---

## Règles d'or

- Langue FR par défaut. Si la page analysée est en anglais → rapport bilingue FR/EN
- Mentionner les touristes si le secteur est tourisme / restauration / hôtellerie / activités
- Si le score est < 40 : insister sur le fait que cette situation est normale et réparable
- Jamais condescendant. On décrit une réalité de marché, pas un échec personnel.
- Jamais de tarif dans ce rapport
- Toujours mentionner ce qui fonctionne bien avant les gaps

---

## Output

Fichier : `GEO-SOCIAL-AUDIT-[nom]-[date].md`

Si invoqué depuis `/geo readiness` : passer les données à `geo-readiness` pour
générer le rapport complet de maturité.
