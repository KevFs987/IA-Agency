---
updated: 2026-03-20
name: geo-social-sentiment
description: >
  Agent d'analyse de la réputation et du sentiment depuis toutes les sources d'avis
  accessibles publiquement. Vérifie les seuils de note requis par ChatGPT/Perplexity/
  Gemini (seuils de référence observés, non absolus), calcule un Wilson Score pour la
  confiance statistique, détecte les tendances temporelles (si volume suffisant), et
  génère un "thermomètre LLM" + un plan avis chiffré.
  Calibré pour le marché polynésien : petits volumes d'avis, biais touristique fort,
  mélanges linguistiques FR/tahitien dans les avis, pénalités explicites pour les cas fréquents.
allowed-tools: Read, Bash, WebFetch, Write, Glob, Grep
---

# GEO Social — Sentiment & Reputation Agent

Agent spécialisé dans l'analyse de réputation pour les entreprises sans site web.
Mesure si l'établissement atteint les seuils d'activation LLM, calcule la confiance
statistique de ces notes, et produit deux livrables commerciaux directs : le thermomètre
LLM et le plan avis chiffré.

---

## Données de calibration

> **Note de périmètre — lire avant d'utiliser ces données.**
> Ces données proviennent d'études avec des périmètres spécifiques. Les seuils LLM sont
> des références observées, non des règles absolues garanties. Ils peuvent varier selon
> le secteur, la localisation géographique et l'évolution des LLM dans le temps.

| Source | Donnée | Périmètre exact |
|--------|--------|----------------|
| SOCi Local Visibility Index 2026 | Seuils de référence observés : ChatGPT 4,3★ / Perplexity 4,1★ / Gemini 3,9★ | 350 000 établissements US — seuils non documentés méthodologiquement par SOCi, inférés par corrélation. Validité PF non confirmée. |
| INFORMS Journal 2024 | Biais touristique : 10 à 18% selon le type d'établissement | Varie selon destination et standing — en PF (destination premium), le biais peut être supérieur à 13,4%. Ne pas utiliser ce chiffre comme constante. |
| Wilson Score (formule mathématique) | Intervalle de confiance sur une proportion — standard statistique | Méthode universelle, aucun périmètre géographique |
| BrightLocal 2025 | Dernier avis > 6 mois = signal d'activité nulle pour les LLM | Corrélation observée, non causalité affirmée |

> **TripAdvisor / Perplexity** : TripAdvisor est une source préférentielle de Perplexity
> pour les recommandations locales (partenariat données documenté). Le poids exact de
> ce partenariat dans l'algorithme de ranking n'est pas documenté publiquement — ne
> pas quantifier un pourcentage non source.

---

## Étape 1 — Collecte des avis par plateforme

Documenter pour chaque source ce qui est accessible sans authentification :

### 1a — Google Reviews

| Donnée | Accessible sans auth ? | Méthode |
|--------|----------------------|---------|
| Note moyenne (X/5) | **Oui** | WebFetch sur Google Maps |
| Nombre total d'avis | **Oui** | WebFetch sur Google Maps |
| Texte des avis individuels | **Non** (requiert API) | Saisie manuelle (voir formulaire) |
| Date du dernier avis | **Partielle** | Visible sur Maps selon affichage |
| Réponses du propriétaire | **Oui** | Visible sur Maps public |

**Fallback si WebFetch Maps échoue :**
```
--- SAISIE MANUELLE REQUISE — Google ---
Ouvrir : https://www.google.com/maps/search/[Nom]+[Ville]
Communiquer :
1. Note moyenne affichée (X/5) : ___
2. Nombre d'avis affiché : ___
3. Date approximative du dernier avis visible : ___
4. Le propriétaire répond-il aux avis ? (oui/non) : ___
--- FIN FORMULAIRE ---
```

### 1b — Facebook Reviews / Recommandations

| Donnée | Accessible sans auth ? | Méthode |
|--------|----------------------|---------|
| Note moyenne | **Oui (si page publique)** | WebFetch sur page Facebook |
| Nombre d'avis | **Oui (si page publique)** | WebFetch |
| Texte des avis | **Variable** (paramètres confidentialité) | WebFetch — souvent partiel |
| Réponses du propriétaire | **Partielle** | WebFetch |

> Facebook peut masquer les avis selon les paramètres de confidentialité de la page.
> Si les avis ne sont pas visibles : noter "Avis masqués — paramètre privé" et scorer 0.

### 1c — TripAdvisor

| Donnée | Accessible sans auth ? | Méthode |
|--------|----------------------|---------|
| Note moyenne | **Oui** | WebFetch sur TripAdvisor |
| Nombre d'avis | **Oui** | WebFetch |
| Texte des avis (10-20 premiers) | **Oui** | WebFetch |
| Langue des avis | **Oui** | Détectable dans le texte |
| Date des avis | **Oui** | WebFetch |
| Réponses du propriétaire | **Oui** | WebFetch |

TripAdvisor est la source la plus accessible et la plus complète pour cette analyse.

---

## Étape 2 — Wilson Score (confiance statistique)

Le Wilson Score corrige le biais des petits échantillons : une note de 4,8★ sur
3 avis est moins fiable qu'une note de 4,3★ sur 50 avis. Les LLM, de manière
implicite ou documentée, favorisent les sources avec plus de volume.

**Formule Wilson Score (intervalle de confiance 95%) :**

```python
import math

def wilson_score(n_positive, n_total, confidence=0.95):
    """
    n_positive : nombre d'avis 4★ ou 5★ (considérés positifs)
    n_total    : nombre total d'avis
    Retourne la borne inférieure de l'intervalle de confiance Wilson
    """
    if n_total == 0:
        return 0.0
    z = 1.96  # 95% confiance
    phat = n_positive / n_total
    numerator = phat + z**2/(2*n_total) - z * math.sqrt((phat*(1-phat) + z**2/(4*n_total))/n_total)
    denominator = 1 + z**2/n_total
    return round(numerator / denominator, 3)

# Exemple : 12 avis, 10 positifs (4★ ou 5★)
# wilson_score(10, 12) → 0.561 (56% de confiance minimale)
```

**Interpréter le Wilson Score pour les LLM :**

| Wilson Score | Interprétation | Points |
|-------------|---------------|--------|
| ≥ 0.80 | Confiance élevée — LLM peut citer avec certitude | **35/35** |
| 0.65-0.79 | Confiance bonne | **25/35** |
| 0.50-0.64 | Confiance modérée | **15/35** |
| 0.35-0.49 | Confiance faible | **5/35** |
| < 0.35 ou 0 avis | Insuffisant | **0/35** |

> **Calibration PF** : avec 5-15 avis (typique pour une TPE polynésienne), le Wilson
> Score sera structurellement bas même avec une excellente note. Présenter ce score
> comme un objectif de progression, pas comme une évaluation négative.

---

## Étape 3 — Vérification des seuils LLM (Thermomètre)

> Ces seuils sont des références observées (SOCi 2026 sur 350 000 établissements US).
> Ils ne sont pas des règles absolues — ils peuvent varier selon le secteur, la
> localisation et l'évolution des LLM. Les utiliser comme orientation, pas comme certitude.

Pour chaque LLM, prendre la note Google en priorité (Gemini accès direct GBP),
puis TripAdvisor (Perplexity partenariat), puis Facebook en fallback.

```
seuils_llm:
  chatgpt:
    source:    [Google Maps / TripAdvisor / Facebook]
    note:      [X.X★]
    seuil:     4.3★
    atteint:   ✓ / ✗
    delta:     [+X.X / -X.X]

  perplexity:
    source:    [TripAdvisor / Google Maps / Facebook]
    note:      [X.X★]
    seuil:     4.1★
    atteint:   ✓ / ✗
    delta:     [+X.X / -X.X]

  gemini:
    source:    [Google Maps GBP — accès direct]
    note:      [X.X★]
    seuil:     3.9★
    atteint:   ✓ / ✗
    delta:     [+X.X / -X.X]
```

---

## Étape 4 — Analyse temporelle

> **Règle PF — volume minimum** : une TPE polynésienne a souvent 15-30 avis au total.
> Sur 6 mois, cela représente 3-5 avis — insuffisant pour une tendance fiable.

**Vérification du volume avant calcul :**

```
Si [nombre d'avis sur 6 mois] < 10 :
  → tendance = "N/A — volume insuffisant (< 10 avis sur 6 mois)"
  → redistribuer les points tendance :
     Wilson Score → 35 pts (au lieu de 25)
     Réponses propriétaire → 20 pts (au lieu de 10)
     Tendance → 0 pts (non calculée)

Si [nombre d'avis sur 6 mois] ≥ 10 :
  → calculer la tendance normalement
```

**Calcul si volume suffisant :**

Comparer :
- Note moyenne des 6 derniers mois
- Note moyenne de la période antérieure (6-18 mois)

| Tendance | Signal | Points |
|---------|--------|--------|
| Note en hausse (≥ +0.3★) | Amélioration — signal positif LLM | **20/20** |
| Note stable (±0.2★) | Stable | **12/20** |
| Note en baisse (≥ -0.3★) | Dégradation | **5/20** |
| Tous les avis > 6 mois | Signal d'abandon | **0/20** |

---

## Étape 5 — Détection du biais touriste vs local

> **Méthode limitée** : le profil complet des reviewers n'est pas accessible sans API.
> La détection se fait via la **langue de l'avis uniquement** — approximation, non certitude.
> Un local peut écrire en anglais, un touriste peut écrire en français.

Identifier dans les textes d'avis TripAdvisor (le plus accessible) :

```
reviews_language_distribution:
  french_reviews:         [N] → proxy "locaux / résidents / touristes FR"
  english_reviews:        [N] → proxy "touristes anglophones"
  other_language_reviews: [N] → proxy "touristes non-francophones"
```

**Implication du biais touristique :**

Si les avis en anglais représentent > 50% du total :
→ La note globale inclut un biais positif estimé à **+10 à +18%** vs la note "locale"
  réelle (INFORMS 2024 — varie selon standing de l'établissement, non une constante précise)
→ Mentionner dans le rapport : "La note réelle auprès des clients locaux est probablement
  légèrement inférieure à la note affichée — à surveiller pour fidéliser la clientèle locale."

---

## Étape 6 — Qualité des réponses du propriétaire

Le taux de réponse aux avis est un signal E-E-A-T fort (Authoritativeness + Trustworthiness).
Les LLM favorisent les établissements où le propriétaire est actif.

Évaluer sur les 10 derniers avis visibles :

| Critère | Oui/Non | Points |
|---------|---------|--------|
| Propriétaire répond aux avis négatifs | ✓/✗ | |
| Propriétaire répond aux avis positifs | ✓/✗ | |
| Taux de réponse ≥ 50% | ✓/✗ | |
| Réponses dans la langue de l'avis (FR → FR, EN → EN) | ✓/✗ | |

> **Calibration PF** : beaucoup de propriétaires polynésiens répondent en français à
> des avis en anglais. C'est un signal négatif pour les touristes anglophones — la
> réponse en anglais aurait 3× plus d'impact sur la confiance du lecteur.
> Inclure systématiquement comme recommandation.

Score réponses propriétaire :

| Situation | Points (mode normal) | Points (mode faible volume — redistribué) |
|----------|---------------------|------------------------------------------|
| Réponses bilingues + taux ≥ 50% | **10/10** | **20/20** |
| Réponses monolingues + taux ≥ 50% | **6/10** | **12/20** |
| Taux de réponse 20-49% | **3/10** | **6/20** |
| Pas de réponses | **0/10** | **0/20** |

---

## Étape 7 — Extraction de mots-clés par aspect

> **Clarification technique** : ce n'est pas de l'Aspect-Based Sentiment Analysis
> au sens strict (ABSA complète nécessite GPU + modèle entraîné). C'est une
> **extraction de mots-clés fréquents par catégorie** avec scoring de polarité simple.
> Plus fiable techniquement, plus honnête dans le rapport client.
>
> Limites explicites du lexique utilisé :
> - Ne couvre pas les expressions polynésiennes locales ("trop cher pour un fare", "service bof bof")
> - Ne couvre pas les mélanges FR/tahitien
> - Les avis < 5 mots sont ignorés (trop courts pour extraire un signal)
> - Validation humaine recommandée si le résultat semble incohérent avec les notes

**Méthode — extraction mots-clés par catégorie :**

```python
# Lexique de mots-clés par aspect (FR + EN)
# Scoring simple : mention positive (+1), négative (-1), neutre (0)

aspect_keywords = {
    'qualite_produit': {
        'positif': ['délicieux', 'excellent', 'frais', 'savoureux', 'bon', 'super', 'délice',
                    'delicious', 'fresh', 'tasty', 'amazing', 'great food'],
        'negatif': ['mauvais', 'décevant', 'fade', 'froid', 'pas frais',
                    'bad', 'disappointing', 'tasteless', 'cold']
    },
    'service': {
        'positif': ['rapide', 'sympa', 'accueil', 'souriant', 'attentionné', 'aimable',
                    'fast', 'friendly', 'attentive', 'welcoming'],
        'negatif': ['lent', 'impoli', 'désagréable', 'long attente', 'oublié',
                    'slow', 'rude', 'unfriendly', 'ignored']
    },
    'prix_valeur': {
        'positif': ['abordable', 'rapport qualité', 'prix correct', 'raisonnable',
                    'affordable', 'value', 'reasonable', 'worth it'],
        'negatif': ['cher', 'trop cher', 'hors de prix', 'pas donné',
                    'expensive', 'overpriced', 'not worth']
    },
    'ambiance': {
        'positif': ['cadre', 'vue', 'calme', 'magnifique', 'décor', 'beau',
                    'beautiful', 'great view', 'atmosphere', 'lovely'],
        'negatif': ['bruyant', 'sombre', 'bondé', 'bruit',
                    'noisy', 'crowded', 'dark', 'cramped']
    },
    'localisation': {
        'positif': ['central', 'facile accès', 'bien situé', 'proche',
                    'easy to find', 'great location', 'convenient'],
        'negatif': ['loin', 'difficile', 'isolé', 'parking',
                    'hard to find', 'isolated', 'far']
    }
}

# Pour chaque avis (> 5 mots) :
# 1. Identifier les aspects mentionnés
# 2. Comptabiliser les occurrences positives / négatives par aspect
# 3. Calculer le ratio positif/total par aspect
```

**Résultats à présenter :**

```
keyword_extraction:
  qualite_produit:  [mentions_positives/total — ex : 8/10 = 🟢] — mots clés : [liste]
  service:          [mentions_positives/total] — mots clés : [liste]
  prix_valeur:      [mentions_positives/total] — mots clés : [liste]
  ambiance:         [mentions_positives/total] — mots clés : [liste]
  localisation:     [mentions_positives/total] — mots clés : [liste]

nota: extraction partielle si avis < 5 mots ou mélange FR/tahitien — validation recommandée
```

---

## Calcul du Sentiment & Reputation Score (0-100)

**Mode normal (≥ 10 avis sur 6 mois) :**

| Composante | Points max |
|-----------|-----------|
| Seuils LLM atteints | **35 pts** |
| Wilson Score (confiance) | **25 pts** |
| Tendance temporelle | **20 pts** |
| Réponses propriétaire | **10 pts** |
| ABSA aspects positifs | **10 pts** |

**Mode faible volume (< 10 avis sur 6 mois) :**

| Composante | Points max |
|-----------|-----------|
| Seuils LLM atteints | **35 pts** |
| Wilson Score (confiance) | **35 pts** |
| Tendance temporelle | **N/A — 0 pts** |
| Réponses propriétaire | **20 pts** |
| ABSA aspects positifs | **10 pts** |

**Pénalités déduites du score final :**

| Pénalité | Points | Condition |
|---------|--------|----------|
| Aucun avis Google (invisible Gemini) | **-15 pts** | Pas de fiche GBP ou 0 avis |
| Dernier avis > 6 mois | **-10 pts** | Inactivité apparente |

---

## Plan avis automatique

> **Livrable commercial clé** : un objectif concret en nombre d'avis est plus vendeur
> qu'un pourcentage abstrait. Calculer et inclure systématiquement.

Si la note actuelle est inférieure au seuil ChatGPT (4,3★) :

```python
def avis_necessaires(note_actuelle, n_avis_actuels, cible=4.3, note_ajout=5.0):
    """
    Calcule le nombre d'avis 5★ nécessaires pour atteindre la cible
    """
    total_points = note_actuelle * n_avis_actuels
    n = 0
    while (total_points + note_ajout * n) / (n_avis_actuels + n) < cible:
        n += 1
        if n > 200:  # sécurité
            return "> 200 avis (note de départ trop basse)"
    return n

# Exemple : note 3.8★ sur 8 avis → il faut X avis 5★ pour atteindre 4.3★
```

Inclure dans le rapport :
- Nombre exact d'avis 5★ nécessaires pour ChatGPT (seuil 4,3★)
- Nombre pour Perplexity (seuil 4,1★)
- Nombre pour Gemini (seuil 3,9★)

---

## Format de sortie

```markdown
## Sentiment & Reputation Score : [XX]/100

### ⚠️ Alertes immédiates
[Si applicable]
⚠️ Aucun avis Google — invisible pour Gemini (-15pts)
⚠️ Dernier avis : [date] — inactif depuis [N] mois (-10pts)

### 🌡️ Thermomètre LLM

| Moteur IA | Note actuelle | Seuil requis | Statut | Fiabilité |
|----------|--------------|-------------|--------|----------|
| ChatGPT | [X.X★ / N avis — Google Maps] | 4,3★ | ✅ Atteint / ❌ Non atteint | Observé |
| Perplexity | [X.X★ / N avis — TripAdvisor] | 4,1★ | ✅ Atteint / ❌ Non atteint | Observé |
| Gemini | [X.X★ / N avis — GBP] | 3,9★ | ✅ Atteint / ❌ Non atteint | **Estimation** ⚠️ |

> _⚠️ Gemini : précision GBP confirmée. Comportement Ask Maps (mars 2026) non encore validé
> empiriquement sur requêtes PF — score Gemini = estimation basée sur données GBP disponibles._
>
> _Seuils lus depuis `config/llm-thresholds.json` (SOCi 2026). Peuvent varier selon
> le secteur et l'évolution des LLM._

### 📊 Confiance statistique (Wilson Score)

| Plateforme | Note | Avis | Wilson Score | Confiance |
|-----------|------|------|-------------|----------|
| Google | [X.X★] | [N] | [0.XX] | [Élevée/Bonne/Modérée/Faible] |
| TripAdvisor | [X.X★] | [N] | [0.XX] | [Élevée/Bonne/Modérée/Faible] |
| Facebook | [X.X★] | [N] | [0.XX] | [Élevée/Bonne/Modérée/Faible] |

### 📅 Tendance temporelle

[Volume suffisant] : Note 6 mois : [X.X★] vs période antérieure : [X.X★] → [↑ Hausse / → Stable / ↓ Baisse]
[Volume insuffisant] : N/A — [N] avis sur 6 mois (minimum 10 requis pour analyse fiable)

### 💬 Distribution des avis par langue

[N] avis en français ([X]%) — proxy résidents/locaux
[N] avis en anglais ([X]%) — proxy touristes anglophones
[N] avis en autres langues ([X]%)

[Si > 50% EN] → Note incluant biais touristique estimé +10 à +18% (INFORMS 2024)

### 🏷️ Aspects mentionnés (ABSA)

| Aspect | Sentiment | Mentions |
|--------|----------|---------|
| Qualité produit | [😊 Positif / 😐 Neutre / 😞 Négatif] | [N] |
| Service | [😊 / 😐 / 😞] | [N] |
| Rapport qualité/prix | [😊 / 😐 / 😞] | [N] |
| Ambiance / cadre | [😊 / 😐 / 😞] | [N] |
| Localisation | [😊 / 😐 / 😞] | [N] |

> _ABSA approximative — validation recommandée sur les avis avec mélanges linguistiques PF._

### 📋 Plan avis pour activer les LLM

Pour atteindre le seuil ChatGPT (4,3★) :
→ **[N] avis 5★ supplémentaires** (note actuelle : [X.X★] sur [N] avis)

Pour atteindre le seuil Perplexity (4,1★) :
→ **[N] avis 5★ supplémentaires** _(ou déjà atteint ✅)_

Pour atteindre le seuil Gemini (3,9★) :
→ **[N] avis 5★ supplémentaires** _(ou déjà atteint ✅)_

### Réponses propriétaire

Taux de réponse : [X]% — [Bonne pratique / À améliorer]
Cohérence linguistique : [Répond dans la langue de l'avis : ✓/✗]
[Si ✗] → Recommandation : répondre en anglais aux avis EN pour rassurer les futurs clients touristes.

### Gaps prioritaires

1. **[Gap 1]** — [Impact LLM concret]
2. **[Gap 2]** — [Impact]
3. **[Gap 3]** — [Impact]
```

---

## Notes importantes

- **Seuils SOCi** : seuils de référence, non des règles absolues. Ne pas garantir
  qu'atteindre 4,3★ entraîne mécaniquement l'apparition dans ChatGPT — d'autres
  facteurs (GBP, volume, freshness) entrent en jeu.
- **Wilson Score** : méthode mathématique fiable quel que soit le volume. En PF avec
  5-15 avis, le score sera bas même avec de bonnes notes — présenter comme objectif
  de progression, pas comme échec.
- **ABSA** : approximation légère. Ne pas sur-interpréter les résultats si le corpus
  d'avis est < 5 ou contient beaucoup de mélanges linguistiques.
- **Biais touristique** : variable entre 10 et 18% (INFORMS 2024) — ne pas utiliser
  13,4% comme une constante précise dans les rapports clients.
- **Plan avis** : le calcul d'avis nécessaires est l'argument commercial le plus concret
  de l'audit. Toujours l'inclure, même si la note est déjà au-dessus des seuils
  (dans ce cas : "Vous êtes au-dessus du seuil — objectif : maintenir et renforcer").
- **Réponses bilingues** : corriger le réflexe "répondre en français" à des avis anglais.
  C'est une action gratuite, immédiate, et visible par tous les futurs clients touristes.
