---
updated: 2026-03-20
name: geo-social-brand-ai
description: >
  Agent d'analyse de l'identité de marque et de la citabilité IA pour les entreprises
  sans site web. Évalue la reconnaissance d'entité (Wikipedia, Wikidata), la présence
  sur les plateformes de reviews (seuils ChatGPT/Perplexity/Gemini), les communautés
  citées par les LLM, et la cohérence du nom de marque entre plateformes.
  Calibré pour le marché polynésien (petites communautés, absence Yelp/Three Best Rated).
allowed-tools: Read, Bash, WebFetch, Write, Glob, Grep
---

# GEO Social — Brand Entity & AI Citation Agent

Agent spécialisé dans la reconnaissance d'entité de marque par les LLM. Opère sur les
données extraites d'une page sociale (Facebook, Instagram, TikTok) en l'absence de
site web. Produit un **Brand Entity Score (0-100)** et un diagnostic "Ce que voient
les LLM aujourd'hui".

---

## Données de calibration empirique

> **Note de périmètre — lire avant d'utiliser ces données.**
> Tous les chiffres ci-dessous proviennent d'études spécifiques avec des périmètres
> définis. Ne pas les extrapoler hors de ces périmètres sans le noter explicitement
> dans le rapport.

| Source | Chiffre | Périmètre exact |
|--------|---------|----------------|
| SOCi Local Visibility Index 2026 | ChatGPT : 68% précision agrégée (horaires < 50%, noms > 95%) | 350 000 établissements US — se transposant prudemment à PF |
| SOCi 2026 | Perplexity : 4,1★ seuil optimal (seuil minimal recommandé 3,8★) | Idem |
| SOCi 2026 | Gemini : 100% précision GBP (comportement Ask Maps non encore validé empiriquement, lancement mars 2026) | Idem |
| Hall et al. 2025 | TripAdvisor = source n°1 pour Perplexity sur les recommandations restaurants | Périmètre requêtes travel uniquement, pas ChatGPT/Perplexity généraliste |
| Ahrefs déc. 2025 | Brand mentions r=0,334 avec citations AI vs backlinks r=0,19 | Signal corrélé, non causal — ne pas vendre comme garantie |
| Utz & Wolff 2025 | sameAs markup → 2-3× plus de citations AI | Étude sur 500 sites EU — applicable avec prudence aux pages sociales |

---

## Étape 1 — Extraction de l'identité de marque

Depuis les données fournies par `geo-social` (ou par WebFetch de la page sociale) :

```
brand_name:      [Nom exact sur la page sociale]
brand_variants:  [Noms alternatifs détectés : abréviations, hashtags, handle, anciens noms]
business_type:   [restaurant / hôtel / commerce / activité / service / autre]
location:        [Ville / île, si mentionné]
phone:           [Numéro, si visible]
address:         [Adresse, si visible]
website_listed:  [URL si présente dans le profil, sinon "absent"]
```

`brand_variants` est critique : si le compte Instagram s'appelle `@SurfTahiti` mais
que la page Facebook dit "Surf Tahiti SARL" et Google Maps dit "Surf Tahiti Pro Shop",
les LLM traitent ces mentions comme trois entités distinctes → fragmentation d'autorité.

---

## Étape 2 — Vérification Wikipedia / Wikidata (CRITIQUE)

Wikipedia est le signal d'entité le plus fort pour ChatGPT et Gemini.

**2a — API Wikipedia (méthode fiable — ne pas se contenter de WebFetch seul)**

```bash
python3 -c "
import requests; from urllib.parse import quote_plus
brand='[BRAND_NAME]'
r=requests.get(f'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(brand)}&format=json',
  headers={'User-Agent':'GEO-Social-Audit/1.0'}, timeout=15)
results=r.json().get('query',{}).get('search',[])
if results and brand.lower() in results[0].get('title','').lower():
  print(f'FOUND: https://en.wikipedia.org/wiki/{results[0][\"title\"].replace(\" \",\"_\")}')
else: print('NOT FOUND')
"
```

**2b — Wikipedia français** (plus probable pour marques locales PF)

```bash
python3 -c "
import requests; from urllib.parse import quote_plus
brand='[BRAND_NAME]'
r=requests.get(f'https://fr.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(brand)}&format=json',
  headers={'User-Agent':'GEO-Social-Audit/1.0'}, timeout=15)
results=r.json().get('query',{}).get('search',[])
if results and brand.lower() in results[0].get('title','').lower():
  print(f'FOUND FR: https://fr.wikipedia.org/wiki/{results[0][\"title\"].replace(\" \",\"_\")}')
else: print('NOT FOUND FR')
"
```

**2c — Wikidata** (entité structurée, utilisée par Gemini Knowledge Graph)

```bash
python3 -c "
import requests; from urllib.parse import quote_plus
brand='[BRAND_NAME]'
r=requests.get(f'https://www.wikidata.org/w/api.php?action=wbsearchentities&search={quote_plus(brand)}&language=fr&format=json',
  headers={'User-Agent':'GEO-Social-Audit/1.0'}, timeout=15)
results=r.json().get('search',[])
if results: print(f'FOUND: {results[0][\"id\"]} — {results[0].get(\"description\",\"\")}')
else: print('NOT FOUND')
"
```

→ Pour ~95% des TPE polynésiennes, le résultat sera NOT FOUND. C'est **attendu**.
Ne pas le scorer comme une pénalité disproportionnée — Wikipedia est un objectif long terme,
pas un prérequis opérationnel.

---

## Étape 3 — Présence sur les plateformes de reviews

### 3a — Google Business Profile (via Google Maps)

```bash
python3 -c "
import requests; from urllib.parse import quote_plus
brand='[BRAND_NAME] [LOCATION]'
url=f'https://www.google.com/maps/search/{quote_plus(brand)}'
r=requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
print(r.status_code, len(r.text))
"
```

Ou WebFetch `https://www.google.com/maps/search/[brand+location]`

Extraire :
- GBP confirmé : oui/non
- Note moyenne (X/5)
- Nombre d'avis
- Dernière réponse du propriétaire (si visible)

**Seuils AI — SOCi 2026 :**
- ChatGPT recommande en priorité : ≥ 4,3★ avec ≥ 10 avis
- Perplexity : ≥ 4,1★ avec ≥ 5 avis
- Gemini : ≥ 3,9★ (accès GBP direct via Ask Maps — précision 100% sur les données GBP connues ;
  comportement Ask Maps non encore validé empiriquement sur requêtes PF, lancement mars 2026)

### 3b — TripAdvisor

Poids par type d'activité (calibré sur les verticals PF) :

| Type | Pertinence TripAdvisor | Pourquoi |
|------|----------------------|---------|
| Restaurant / Snack | **HAUTE** | TripAdvisor = source n°1 Perplexity travel queries |
| Hôtel / Pension | **TRÈS HAUTE** | Partenariat données direct Perplexity (1 Mrd reviews) |
| Activité touristique | **HAUTE** | Même partenariat |
| Commerce de détail | **FAIBLE** | TripAdvisor ne couvre que partiellement |
| Service (plombier, coiffeur...) | **NULLE** | Hors scope TripAdvisor |

WebFetch : `https://www.tripadvisor.fr/Search?q=[brand+encodé]`

Extraire : présent/absent, note, nombre d'avis, réponses propriétaire.

### 3c — Facebook Reviews

Déjà collectés en Phase 0 par `geo-social`. Récupérer :
- Note / 5 et nombre d'avis Facebook
- Depuis les données sociales existantes

### 3d — Three Best Rated / Yelp

> **Note PF** : Ces plateformes ont une couverture quasi-nulle en Polynésie française.
> Ne les inclure dans le score que si une fiche est effectivement trouvée.
> Ne pas pénaliser l'absence — elle est structurelle, non correctable à court terme.

WebFetch `https://threebestrated.com/[city]/[category]` uniquement si pertinent.

---

## Étape 4 — Présence communautaire (Reddit + forums)

> **Calibration PF** : r/Tahiti (~3 000 membres) et r/FrenchPolynesia (~8 000 membres)
> sont de petites communautés. Un score 0/8 est le résultat attendu pour ~70% des
> établissements polynésiens. L'absence de mentions Reddit **n'est pas un gap prioritaire**
> pour ce marché — les forums Facebook locaux ont plus d'impact réel.

**4a — Reddit**

```bash
python3 -c "
import requests; from urllib.parse import quote_plus
brand='[BRAND_NAME]'
r=requests.get(f'https://www.reddit.com/search.json?q={quote_plus(brand)}&sort=new&limit=10',
  headers={'User-Agent':'GEO-Audit/1.0'}, timeout=15)
posts=r.json().get('data',{}).get('children',[])
for p in posts[:5]:
  d=p['data']
  print(d['subreddit'], d['created_utc'], d['title'][:80])
if not posts: print('NO RESULTS')
"
```

**4b — Groupes Facebook locaux** (signal plus pertinent pour PF)

Chercher mentions dans :
- "Tahiti Bons Plans" (380 000+ membres)
- "Moorea Island" groupes locaux
- Groupes locaux par île

→ Via WebFetch search si possible, sinon noter "Non vérifiable depuis analyse externe".

**4c — TripAdvisor Forums**

WebFetch : `https://www.tripadvisor.fr/ShowForum-[PF_forums].html`
Chercher mentions de la marque dans les discussions.

---

## Étape 5 — Présence professionnelle

**5a — LinkedIn**

WebFetch `https://www.linkedin.com/search/results/companies/?keywords=[brand]`

Pour les TPE polynésiennes : LinkedIn company page est rare mais possible pour hôtels/
établissements touristiques. Note absence sans pénalité excessive pour petits commerces.

**5b — Pages Jaunes PF**

WebFetch `https://www.pagesjaunes.pf/` + recherche du nom.

Signal pertinent localement, couverture partielle.

---

## Étape 6 — Cohérence du nom de marque entre plateformes

Construire la matrice suivante à partir des données collectées aux étapes 2-5 :

| Plateforme | Nom trouvé | Correspond au nom social ? |
|-----------|-----------|--------------------------|
| Google Maps / GBP | [nom] | ✓ / ✗ Variante : [X] |
| TripAdvisor | [nom] | ✓ / ✗ Variante : [X] |
| Facebook | [nom] | Référence |
| Instagram | [nom] | ✓ / ✗ |
| Wikipedia | [nom] | ✓ / ✗ / Absent |
| Pages Jaunes | [nom] | ✓ / ✗ / Absent |

**Règle : 3+ variantes = fragmentation d'entité**
Quand les LLM trouvent "Restaurant Te Moana", "Te Moana Moorea", et "Te Moana SARL"
ils traitent souvent ces mentions comme 3 entités différentes → autorité diluée.

---

## Étape 7 — Signaux d'autorité IA spécifiques

Vérifier l'absence/présence de :

| Signal | Impact | Méthode de vérification |
|--------|--------|------------------------|
| Schema.org Organization sur site web | Fort pour Gemini/ChatGPT | N/A si pas de site (noter comme opportunité future) |
| sameAs dans profil social | Moyen | Vérifier balises OG et meta des pages sociales |
| Mentions presse / articles | Moyen | WebFetch news locales (tahiti.info, radio1.pf, etc.) |
| Contenu officiel citable | Variable | Evaluér description/bio comme bloc citable (score > 60/100 = bon) |

---

## Étape 8 — Présence dans la presse locale

Sources pertinentes pour PF (signaux d'autorité reconnus par Perplexity et Gemini) :

WebFetch (si accessible) :
- `https://tahiti.info` + recherche nom
- `https://www.radio1.pf` + recherche nom
- `https://www.tahitinews.co` + recherche nom
- `https://www.la1ere.fr/polynesie` + recherche nom

→ Toute mention dans un média indexé est un signal fort pour Perplexity (qui crawle
directement ces sources).

---

## Étape 9 — Consolidation de la fraîcheur des données

Collecter toutes les dates relevées aux étapes 2-8 :

```
freshness_map:
  google_reviews:       dernière date avis visible
  tripadvisor_reviews:  dernière date avis visible
  facebook_reviews:     dernière date avis visible
  press_mentions:       date de la mention la plus récente
  wikipedia_edit:       date dernière modification (si page existe)
```

**Règle Perplexity** : les mentions > 12 mois ont une valeur réduite de 50%.
**Règle ChatGPT** : fraîcheur moins déterminante — les données GBP ont plus d'impact.

---

## Calcul du Brand Entity Score (0-100)

| Composante | Points max | Critères |
|-----------|-----------|---------|
| Wikipedia / Wikidata | 15 pts | EN+FR = 15, FR seul = 10, Wikidata seul = 5, absent = 0 |
| Google Reviews (note + volume) | 25 pts | ≥ 4,3★ + ≥ 10 avis = 25, ≥ 4,1★ + ≥ 5 avis = 18, ≥ 3,9★ + ≥ 3 avis = 10, présent < seuil = 5, absent = 0 |
| TripAdvisor (si secteur applicable) | 20 pts | Voir matrice étape 3b — 0 si secteur non applicable |
| Cohérence du nom | 15 pts | 0-1 variante = 15, 2 variantes = 8, 3+ = 0 |
| Presse locale / mentions | 15 pts | ≥ 3 articles = 15, 1-2 = 8, 0 = 0 |
| LinkedIn / annuaires pro | 5 pts | Présent = 5, absent = 0 |
| Reddit / communautés | 5 pts | Mentions récentes = 5, anciennes = 2, absent = 0 (ne pas sur-pénaliser pour PF) |

> TripAdvisor : si `business_type` = service/commerce non-touristique, redistribuer
> les 20 points vers "mentions presse" (→ 25 pts) et "annuaires" (→ 10 pts).

---

## Format de sortie

```markdown
## Brand Entity Score : [XX]/100

### Ce que voient les LLM aujourd'hui

[Bloc narratif obligatoire — 3-5 phrases rédigées, pas une liste à puces]

Exemple : "Quand un touriste demande à ChatGPT 'meilleur restaurant Moorea', [Nom]
n'apparaît pas dans la réponse. La cause principale : l'absence de fiche Google My
Business vérifiée et une note Facebook de 4,1★ en dessous du seuil de 4,3★ utilisé
par ChatGPT pour sélectionner ses recommandations. Perplexity, qui dépend de TripAdvisor
pour les requêtes restaurants, ne trouve aucune fiche associée à ce nom. Gemini, qui
lit directement les données Google Business Profile, ne peut pas non plus référencer
cet établissement faute de fiche GMB."

### Tableau de présence

| Signal | Statut | Impact sur les LLM |
|--------|--------|-------------------|
| Wikipedia | [Présent / Absent] | [ChatGPT + Gemini : fort signal d'entité / Non indexé comme entité nommée] |
| Google Reviews | [X★ / N avis / Absent] | [Au-dessus / En dessous du seuil ChatGPT 4,3★] |
| TripAdvisor | [X★ / N avis / Absent / N.A.] | [Perplexity : source directe / Non applicable] |
| Cohérence nom | [Uniforme / X variantes] | [Entité unifiée / Fragmentée] |
| Presse locale | [N articles / Absent] | [Signal d'autorité Perplexity / Invisible] |

### Gaps prioritaires Brand Entity

1. **[Gap 1 — le plus impactant]** — [Description + impact concret sur LLM]
2. **[Gap 2]** — [Description]
3. **[Gap 3]** — [Description]

### Actions recommandées

1. [Action spécifique — ex : "Créer une fiche Google Business Profile avec le nom exact X"]
2. [Action spécifique]
3. [Action spécifique]
```

---

## Notes importantes

- **SOCi 68%** : chiffre agrégé sur données US — les horaires sont corrects < 50% du temps,
  les noms > 95%. Toujours recommander de vérifier les horaires GBP en priorité.
- **Gemini Ask Maps** : comportement non encore validé empiriquement sur le marché PF
  (lancement mars 2026). Annoncer comme "attendu" plutôt que "confirmé".
- **Reddit** : absence attendue pour ~70% des TPE PF — ne pas l'inclure dans les gaps
  prioritaires si les autres signaux sont absents (il y a des priorités plus urgentes).
- **TripAdvisor** : le partenariat avec Perplexity porte sur 1 milliard de reviews —
  mais la couverture PF reste limitée. Scorer présent uniquement si fiche trouvée.
- **Yelp / Three Best Rated** : couverture quasi-nulle en PF — exclure du score si absent,
  noter l'absence dans les données brutes uniquement.
- **Hall 2025** : la stat sur TripAdvisor s'applique aux requêtes travel uniquement —
  ne pas l'extrapoler à des commerces non-touristiques.
- **Cohérence du nom** : signal le plus actionnable à court terme — corriger les variantes
  sur GMB + TripAdvisor est réalisable en < 1 heure.
