---
title: Architecture agents geo-social v2.0
category: agents
updated: 2026-03-20
expires: 2027-03-20
tags: [geo-social, agents, llm, architecture, polynesie]
---

# Architecture des 5 agents spécialisés geo-social

## Contexte

La v1.0 de `geo-social` effectuait un audit séquentiel en un seul skill.
La v2.0 introduit 5 agents spécialisés lancés en parallèle, calqués sur
l'architecture du full audit `/geo audit <url>`.

**Cas d'usage** : entreprises sans site web (40-50% du marché polynésien)
dont la seule vitrine digitale est une ou plusieurs pages sociales.

---

## Les 5 agents — rôles et périmètres

### 1. geo-social-brand-ai
**Fichier** : `agents/geo-social-brand-ai.md`
**Rôle** : reconnaissance d'entité de marque par les LLM
**Analyse** :
- Wikipedia / Wikidata (signal entité fort pour ChatGPT + Gemini)
- Review platforms (seuils SOCi 2026 : ChatGPT 4,3★ / Perplexity 4,1★ / Gemini 3,9★)
- Communautés Reddit/Facebook locaux (calibré PF : r/Tahiti ~3K, r/FrenchPolynesia ~8K)
- Cohérence du nom de marque (fragmentation d'entité = autorité diluée)
- Presse locale (tahiti.info, radio1.pf — sources Perplexity)

**Output** : Brand Entity Score (0-100) + narrative "Ce que voient les LLM aujourd'hui"

**Calibrations PF clés** :
- Reddit absent = attendu pour ~70% des TPE PF — ne pas pénaliser
- Yelp / Three Best Rated = couverture quasi-nulle en PF — ne scorer que si fiche trouvée
- Gemini Ask Maps = comportement non encore validé empiriquement (lancement mars 2026)

---

### 2. geo-social-local-listings
**Fichier** : `agents/geo-social-local-listings.md`
**Rôle** : couverture des annuaires et plateformes locales
**Analyse** :
- Google Business Profile (GBP) — levier n°1, alimente Gemini directement
- TripAdvisor — partenariat direct Perplexity, poids variable selon secteur
- Pages Jaunes PF — signal local Perplexity + backlink Google
- Bing Maps — source cartographique primaire ChatGPT
- Foursquare — data aggregator → Bing → ChatGPT

**Chaîne LLM documentée** :
```
GBP → Gemini (direct) + ChatGPT (via Bing)
TripAdvisor → Perplexity (partenariat) + ChatGPT (web crawl)
Foursquare → Bing Maps → ChatGPT
Pages Jaunes PF → Perplexity (crawl) + Google (backlink)
```

**Output** : Local Listings Score (0-100) + carte flux LLM

**Calibrations PF clés** :
- GBP non vérifiée = poids < 30% vs vérifiée
- TripAdvisor poids 0 pour services non-touristiques (coiffeur, plombier...)
- Apple Maps / Yelp = couverture quasi-nulle PF — action de faible priorité

---

### 3. geo-social-cross-platform
**Fichier** : `agents/geo-social-cross-platform.md`
**Rôle** : cohérence NAP (Name, Address, Phone) et unification d'entité
**Analyse** :
- Matrice comparative NAP sur toutes les plateformes détectées
- Variantes de nom (scoring gradué : 1 variante = -5pts, 2 = -15pts, 3+ = -30pts)
- Détermination du nom canonique (référence = registre du commerce PF)
- Liens croisés entre plateformes (signal entité unifiée pour LLM)
- Génération JSON-LD sameAs (fort corrélation avec citations AI — Utz & Wolff 2025)
- Fiches orphelines / doublons GBP (délai suppression : 1-4 semaines)

**Output** : Cross-Platform Score (0-100) + bloc JSON-LD sameAs prêt à l'emploi

**Calibrations PF clés** :
- Variantes trilingues FR/tahitien/EN = légitime culturellement, problématique techniquement
- Numéros sans +689 = confusant pour parsers E.164 des LLM
- Scraping Facebook/Instagram/TikTok : 40-60% d'échec WebFetch → fallback saisie manuelle guidée
- Score Social only plafonné à ~60/100 structurellement

---

### 4. geo-social-content-quality
**Fichier** : `agents/geo-social-content-quality.md`
**Rôle** : qualité du contenu social comme signal E-E-A-T
**Analyse** :
- Type de compte (personnel vs page pro — pénalité -10pts si personnel)
- Fréquence de publication (seuils adaptés TPE PF : 2-3 posts/semaine = normal)
- Densité d'information par post (prix, horaires, contact, CTA)
- Signaux E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
- Blocs citables : bio + posts épinglés (standard 134-167 mots — Georgia Tech/Princeton 2024)
- Bilingue FR/EN (pondéré 20pts — fort pour tourisme PF)
- Contenu evergreen vs contenu périmé épinglé

**Output** : Content Quality Score (0-100) + kit quick wins (3 templates bilingues personnalisés)

**Standards adoptés** :
- 134-167 mots pour bios/descriptions (Georgia Tech/Princeton 2024) — pas BrightEdge 40-60 mots
- Instagram Graph API non utilisable sans OAuth → métadonnées publiques uniquement
- ABSA non disponible ici — voir geo-social-sentiment

**Calibrations PF clés** :
- Compte personnel très fréquent → mentionner que conversion gratuite, 10 min, non destructive
- Dernier post > 3 mois = pénalité -10pts (signal d'abandon LLM)
- Bilingue FR/EN sous-pondéré sans tourisme — réduire à 10pts pour services locaux purs

---

### 5. geo-social-sentiment
**Fichier** : `agents/geo-social-sentiment.md`
**Rôle** : réputation et sentiment depuis sources d'avis publiques
**Analyse** :
- Collecte notes/avis Google Maps, Facebook Reviews, TripAdvisor (accessibilité documentée)
- Wilson Score (confiance statistique — fiable même avec 5-15 avis)
- Vérification seuils LLM par plateforme (ChatGPT 4,3★ / Perplexity 4,1★ / Gemini 3,9★)
- Analyse temporelle (si ≥ 10 avis sur 6 mois — sinon : N/A + redistribution des points)
- Détection biais touriste via langue des avis (EN = proxy touriste, approximation)
- Réponses propriétaire (taux + cohérence linguistique)
- ABSA légère (regex + lexique, sans GPU)

**Output** : Sentiment Score (0-100) + thermomètre LLM + plan avis chiffré

**Plan avis** : calcule exactement combien d'avis 5★ supplémentaires pour atteindre chaque seuil LLM

**Calibrations PF clés** :
- Biais touristique : entre 10 et 18% (INFORMS 2024) — pas une constante précise
- Wilson Score bas avec peu d'avis = normal et attendu en PF → présenter comme objectif
- ABSA partielle sur français polynésien avec mélanges linguistiques → validation humaine recommandée
- Réponses EN à avis EN = recommandation systématique (souvent ignoré en PF)
- Pénalité -15pts si aucun avis Google (invisible Gemini)

---

## Formule d'agrégation du Score GEO Social

```
Score GEO Social = (
  score_sentiment       × 0.25 +
  score_local_listings  × 0.25 +
  score_brand_ai        × 0.20 +
  score_content_quality × 0.15 +
  score_cross_platform  × 0.15
)
```

**Justification des pondérations** :
- Sentiment + Listings = 50% → ce sont les deux leviers les plus directs sur les LLM
- Brand AI = 20% → important mais plus long terme (Wikipedia, presse)
- Content + Cross-platform = 30% → leviers d'optimisation continue

---

## Sources de recherche principales

| Source | Donnée clé | Statut |
|--------|-----------|--------|
| SOCi Local Visibility Index 2026 | Seuils de référence LLM (observés, non absolus) | Corrélation US → prudence PF |
| Georgia Tech / Princeton 2024 | Blocs citables 134-167 mots | Adopté comme standard repo |
| INFORMS Journal 2024 | Biais touristique 10-18% | Varie par établissement/destination |
| Utz & Wolff 2025 | sameAs markup corrélé citations AI | Corrélation observée, non causalité |
| BrightLocal 2025 | NAP inconsistency corrélé ranking local | Corrélation, nombreuses variables |
| Hall et al. 2025 | TripAdvisor source n°1 Perplexity travel | Périmètre travel uniquement |
| Ahrefs déc. 2025 | Brand mentions r=0,334 vs backlinks r=0,19 | Corrélé, non causal |

---

## Livrables clients générés automatiquement

| Livrable | Source | Usage |
|---------|--------|-------|
| Thermomètre LLM | geo-social-sentiment | Argument commercial visuel |
| Plan avis chiffré | geo-social-sentiment | "Il vous faut 8 avis 5★ pour ChatGPT" |
| JSON-LD sameAs | geo-social-cross-platform | Déployable sur futur site one-page |
| Kit quick wins contenu | geo-social-content-quality | 3 templates bilingues FR/EN |
| Narrative LLM | geo-social-brand-ai | "Voici ce que voit ChatGPT sur vous" |

---

## Implications scoring

Ces 5 agents permettent à `geo-social` d'atteindre le même niveau de profondeur
analytique que le full audit `/geo audit` pour les entreprises sans site web.
Le score GEO Social résultant est directement comparable au GEO Score standard —
permettant un suivi de progression vers le niveau 4 (GEO-ready).

---

## Idées d'implémentation

- **Auto-packaging** : l'étape 2.5 du skill construit le `social_context` JSON
  une seule fois et le passe à tous les agents → évite les WebFetch redondants
- **Fallback gracieux** : si un agent échoue, le score est calculé sur les 4 restants
  avec repondération proportionnelle → pas de rapport bloqué
- **Mode rapide** : si `--quick` est passé en argument, n'exécuter que les agents
  listings et sentiment (les deux plus impactants à 50%) → rapport en < 2 min
