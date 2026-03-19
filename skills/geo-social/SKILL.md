---
name: geo-social
description: >
  Audit de présence digitale depuis une URL de réseau social (Facebook, Instagram, TikTok).
  Pour les entreprises sans site web — cas dominant en Polynésie française.
  Extrait : nom, description, abonnés, fréquence de publication, avis, signaux d'autorité.
  Identifie les gaps (site absent, GMB manquant, schema absent) et produit un score 0-100.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, social, facebook, instagram, tiktok, polynesie, local, audit]
allowed-tools: Read, Write, WebFetch, Bash
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
2. Un **score de maturité digitale** (0-100)
3. Les **gaps prioritaires** (ce qui manque et son impact)
4. Les **recommandations concrètes** adaptées au niveau réel

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

## Étape 4 — Calcul du Score de Maturité Digitale (0-100)

### Composantes du score

| Composante | Poids | Description |
|-----------|-------|-------------|
| Présence sociale active | 25% | Page existante, posts récents (< 2 semaines), engagement |
| Informations de contact | 20% | Adresse, téléphone, email accessibles |
| Présence hors-social | 20% | Google Maps, TripAdvisor, Pages Jaunes |
| Qualité du profil | 15% | Bio complète, catégorie, horaires, photos de couverture |
| Site web | 15% | Présent et fonctionnel |
| Signaux de confiance | 5% | Avis, note, ancienneté de la page |

### Barème par composante

**Présence sociale active (25 pts max)**
- Page existante : 5 pts
- Post dans les 7 derniers jours : 10 pts
- Post dans les 30 derniers jours : 5 pts
- Engagement visible (commentaires, likes) : 5 pts

**Informations de contact (20 pts max)**
- Numéro de téléphone visible : 7 pts
- Adresse physique visible : 7 pts
- Email ou formulaire de contact : 6 pts

**Présence hors-social (20 pts max)**
- Fiche Google My Business confirmée : 10 pts
- TripAdvisor / Pages Jaunes : 5 pts chacun

**Qualité du profil (15 pts max)**
- Bio / description complète (> 50 mots) : 5 pts
- Catégorie d'activité définie : 3 pts
- Horaires d'ouverture mentionnés : 4 pts
- Photos de couverture professionnelles : 3 pts

**Site web (15 pts max)**
- Site présent et fonctionnel : 10 pts
- HTTPS : 3 pts
- Mobile-friendly apparent : 2 pts

**Signaux de confiance (5 pts max)**
- Note moyenne ≥ 4/5 avec ≥ 10 avis : 5 pts
- Note moyenne ≥ 3.5/5 avec ≥ 5 avis : 3 pts
- Avis présents mais peu nombreux : 1 pt

### Score → Niveau de maturité

| Score | Niveau | Interprétation |
|-------|--------|----------------|
| 0-20 | Niveau 0-1 | Présence très limitée |
| 21-40 | Niveau 1 | Social only, bases manquantes |
| 41-60 | Niveau 1-2 | Social actif mais gaps importants |
| 61-80 | Niveau 2-3 | Bonne base, optimisation possible |
| 81-100 | Niveau 3-4 | Présence solide |

---

## Étape 5 — Génération du Rapport

### Structure du rapport

```markdown
# Audit Social — [Nom de l'entreprise]
**Plateforme analysée :** [Facebook / Instagram / TikTok]
**URL :** [url]
**Date :** [date]

---

## Score de Maturité Digitale : [XX]/100

[Une phrase de contexte : "Ce score reflète la visibilité digitale globale
de [nom] — pas seulement votre présence sur [plateforme], mais votre
capacité à être trouvé par de nouveaux clients en ligne."]

---

## Ce que nous avons trouvé

### Présence sur [Plateforme]
| Élément | Valeur | Évaluation |
|---------|--------|------------|
| Abonnés / Likes | [N] | [Bon / Moyen / Faible pour le marché local] |
| Fréquence de publication | [X posts/semaine] | [Actif / Irrégulier / Inactif] |
| Dernier post | [date ou estimation] | [Récent / Ancien] |
| Bio complète | ✓ / ✗ | [Note] |
| Infos de contact | ✓ / ✗ | [Note] |
| Lien vers site web | ✓ [url] / ✗ Absent | [Note] |

### Présence hors réseaux sociaux
| Plateforme | Statut | Impact |
|-----------|--------|--------|
| Google My Business | ✓ Présent ([note]/5, [N] avis) / ✗ Absent | [Impact] |
| TripAdvisor | ✓ / ✗ | [Impact] |
| Pages Jaunes | ✓ / ✗ | [Impact] |
| Site web | ✓ [url] / ✗ Absent | [Impact] |

---

## Les 3 Gaps Prioritaires

### Gap 1 — [Titre du gap le plus impactant]
**Problème :** [Description en 1-2 phrases, impact concret]
**Ce que ça veut dire pour vous :** [Traduction business — ex : "Vos clients
touristes qui cherchent 'restaurant Moorea' sur Google ne vous trouvent pas"]

### Gap 2 — [Titre]
**Problème :** [...]
**Ce que ça veut dire pour vous :** [...]

### Gap 3 — [Titre]
**Problème :** [...]
**Ce que ça veut dire pour vous :** [...]

---

## Recommandations Prioritaires

1. **[Action 1 — la plus urgente]**
   → [Description courte et concrète]

2. **[Action 2]**
   → [Description]

3. **[Action 3]**
   → [Description]

---

## Prochaine Étape

[CTA vers un appel de découverte. Pas de tarif. Ex : "Si vous voulez
comprendre exactement ce qui manque et comment y remédier,
je suis disponible pour un appel de 30 minutes."]

---
*Audit généré par IA-Agency Polynésie — [date]*
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
