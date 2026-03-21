---
name: geo-discover
description: >
  Recherche et reconstruction de la présence digitale complète d'une entreprise
  à partir de son nom seul (sans URL). Cherche sur Google Maps, TripAdvisor,
  Facebook, Instagram, Wikipedia, Pages Jaunes, et toute trace publique.
  Produit un profil de présence digitale + score de maturité.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, discover, recherche, nom-marque, polynesie, local, presences]
allowed-tools: Read, Write, WebFetch, Bash
---

# GEO Discover — Reconstruction de Présence par Nom de Marque

> **Usage** : invoqué par `/geo audit "Nom de l'entreprise"` ou `/geo readiness "Nom"`
>
> Exemples :
> - `/geo audit "Resto Te Moana Moorea"`
> - `/geo readiness "Hôtel Kia Ora"`
> - `/geo audit "Surf School Tahiti"`

---

## Objectif

Reconstruire le profil digital complet d'une entreprise à partir de son nom seul.
Cas typique : un commerce local que quelqu'un recommande à l'oral, mais dont
on ne connaît ni le site ni les réseaux.

Cela répond au cas C du marché polynésien :
**Nom de marque seul, aucune présence détectable a priori.**

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Étape 1 — Nettoyage et préparation du nom

```
Input reçu : "Resto Te Moana Moorea"

Extraire :
- Nom court probable : "Te Moana"
- Localisation probable : "Moorea" (si mentionnée)
- Type d'activité probable : "Resto" → restaurant
- Variantes de recherche à tester :
  - "Te Moana Moorea"
  - "Restaurant Te Moana"
  - "Te Moana restaurant Moorea"
  - "te moana" (minuscules pour certaines APIs)
```

Encoder le nom pour les URLs : remplacer les espaces par `+` ou `%20`.

---

## Étape 2 — Recherche multi-plateformes

Lancer les recherches suivantes en parallèle (WebFetch) :

### 2.1 Google Maps
```
URL : https://www.google.com/maps/search/[nom+encodé]+[localisation]
Extraire depuis le HTML :
- Nom exact de la fiche
- Adresse
- Note /5 et nombre d'avis
- Catégorie
- Site web associé
- Numéro de téléphone
- Horaires
- Photos (nombre)
```

### 2.2 TripAdvisor
```
URL : https://www.tripadvisor.fr/Search?q=[nom+encodé]
Extraire :
- Présence ou non dans les résultats
- Note et nombre d'avis si présent
- Classement local si mentionné
```

### 2.3 Facebook
```
URL : https://www.facebook.com/search/pages/?q=[nom+encodé]
Extraire :
- Page officielle probable (nom + localisation)
- Abonnés
- Note si présente
```

### 2.4 Instagram
```
URL : https://www.instagram.com/[nom-sans-espaces]/ (variantes)
Tester les handles probables :
- [nomcourt] (ex: temoana)
- [nomcourt][ville] (ex: temoanamoorea)
- [type][nomcourt] (ex: restotemoana)
```

### 2.5 Pages Jaunes Polynésie
```
URL : https://www.pagesjaunes.pf/annuaires/recherche?quoi=[nom]&ou=polynesie
Extraire :
- Présence ou non
- Adresse, téléphone si présents
```

### 2.6 Wikipedia (entité)
```
URL : https://fr.wikipedia.org/w/api.php?action=query&list=search&srsearch=[nom]&format=json
Vérifier si une entrée Wikipedia existe pour ce nom ou cette entreprise.
Rare pour les petits commerces, mais pertinent pour les hôtels de luxe.
```

### 2.7 Site web direct (tentatives)
Tester les URLs probables :
```
https://[nomcourt].pf
https://[nomcourt].com
https://[nomcourt].fr
https://www.[nomcourt].pf
```
Si une URL répond (status 200) → noter et passer à geo-technical pour analyse rapide.

### 2.8 Google Search (recherche générale)
```
WebFetch : https://www.google.com/search?q=[nom+encodé]+polynésie+française
Analyser les premiers résultats organiques :
- Site officiel ? → URL
- Réseaux sociaux ? → URLs
- Articles de presse mentionnant l'entreprise ?
- Avis sur Booking / Airbnb / Expedia si hôtel / location
```

### 2.9 Vérification de l'empreinte IA (Perplexity)

```
WebFetch : https://www.perplexity.ai/search?q=[nom+encodé]+[localisation]

Objectif : mesurer ce que les IA génératives "savent" sur l'entreprise,
et détecter les erreurs ou informations obsolètes.

Contexte : les LLMs ont une précision de ~68% sur les données d'établissements
locaux dans les marchés peu digitalisés (SOCi Local Search Report 2026).
32% des informations peuvent être incorrectes, obsolètes, ou confondues
avec un autre établissement.

Analyser :
- L'entreprise est-elle citée dans les résultats Perplexity ?
- Nom affiché : correspond au nom réel ? (risque de confusion avec homonymes)
- Adresse / localisation : correcte ou obsolète ?
- Téléphone : correct ou numéro périmé ?
- Horaires : si mentionnés, correspondent-ils aux données Google Maps ?
- Informations erronées : prix, menu, services qui n'existent plus ?
- L'IA confond-elle avec une autre entreprise du même secteur ?

Classer le résultat en 3 catégories :
- ✅ Conforme — informations présentes et correctes
- ⚠️ Partiel — présente mais avec erreurs ou infos manquantes
- ❌ Absent ou erroné — non cité ou informations fausses
```

---

## Étape 3 — Consolidation du profil

Après toutes les recherches, construire le profil consolidé :

```json
{
  "nom": "[Nom trouvé]",
  "nom_input": "[Nom tel que saisi]",
  "secteur": "[restaurant / hôtel / commerce / service / activité]",
  "localisation": "[Ville / île]",
  "presences": {
    "site_web": {
      "url": null,
      "statut": "absent | présent | présent-partiel"
    },
    "google_maps": {
      "present": true,
      "note": 4.2,
      "avis": 87,
      "adresse": "...",
      "telephone": "..."
    },
    "facebook": {
      "url": "...",
      "abonnes": 1200
    },
    "instagram": {
      "url": null,
      "statut": "non trouvé"
    },
    "tripadvisor": {
      "present": false
    },
    "pages_jaunes": {
      "present": true
    },
    "wikipedia": {
      "present": false
    },
    "perplexity_ia": {
      "statut": "conforme | partiel | absent_ou_errone",
      "est_citee": true,
      "discordances": ["liste des erreurs détectées — vide si conforme"]
    }
  },
  "score_maturite": 35,
  "niveau": 1,
  "gaps_prioritaires": [
    "Site web absent",
    "Pas de présence TripAdvisor malgré activité touristique",
    "Instagram non trouvé"
  ]
}
```

---

## Étape 4 — Calcul du Score

Utiliser la même grille que `geo-social` :

| Composante | Poids | Critères |
|-----------|-------|----------|
| Présence sociale active | 25% | Facebook ou Instagram avec posts récents |
| Informations de contact | 20% | Téléphone, adresse accessibles quelque part |
| Présence hors-social | 20% | Google Maps, TripAdvisor, Pages Jaunes |
| Qualité des profils | 15% | Descriptions complètes, photos |
| Site web | 15% | Présent et fonctionnel |
| Signaux de confiance | 5% | Avis, note, ancienneté |

---

## Étape 5 — Rapport de Découverte

```markdown
# Audit de Découverte — [Nom de l'entreprise]
**Recherche effectuée sur :** Google Maps, Facebook, Instagram, TripAdvisor, Pages Jaunes, Web
**Date :** [date]

---

## Ce que nous avons trouvé

### Score de Maturité Digitale : [XX]/100 — Niveau [X]/4

[1-2 phrases de contexte adaptées au secteur et au niveau]

### Présences détectées

| Plateforme | Statut | Détails |
|-----------|--------|---------|
| Site web | ✓ [url] / ✗ Absent / ? Non trouvé | [Note] |
| Google My Business | ✓ [note]/5 — [N] avis / ✗ Absent | [Note] |
| Facebook | ✓ [N] abonnés / ✗ Absent | [Note] |
| Instagram | ✓ / ✗ / ? | [Note] |
| TikTok | ✓ / ✗ / ? | [Note] |
| TripAdvisor | ✓ / ✗ | [Note] |
| Pages Jaunes | ✓ / ✗ | [Note] |
| Wikipedia | ✓ / ✗ | [Note] |
| **Perplexity / IA** | ✅ Conforme / ⚠️ Partiel / ❌ Absent ou erroné | [Détail des erreurs si applicable] |

### Informations de contact trouvées

| Information | Valeur | Source |
|------------|--------|--------|
| Téléphone | [numéro] / Non trouvé | [Source] |
| Adresse | [adresse] / Non trouvée | [Source] |
| Email | [email] / Non trouvé | [Source] |

---

## Empreinte IA — Ce que ChatGPT / Perplexity savent sur vous

> ℹ️ Les IA génératives utilisées par vos clients ont une précision d'environ 68% sur les
> données d'établissements locaux. 1 information sur 3 peut être incorrecte ou obsolète.

[Si statut = ✅ Conforme]
→ "Les informations que les IA affichent sur [nom] sont exactes et à jour. ✅"

[Si statut = ⚠️ Partiel]
→ "Les IA mentionnent [nom] mais avec des informations incorrectes :"
   - [Lister chaque discordance détectée]
→ "Un client qui planifie son voyage peut recevoir une mauvaise adresse,
   un numéro obsolète, ou des horaires erronés."

[Si statut = ❌ Absent ou erroné]
→ "Les IA génératives ne citent pas [nom] ou le confondent avec un autre établissement."
→ "Cela signifie que vos futurs clients touristes, s'ils posent la question sur ChatGPT,
   ne vous trouvent pas — ou reçoivent des informations sur un concurrent."

---

## Les 3 Gaps Prioritaires

[Même format que geo-social]

---

## Ce qui fonctionne déjà

[Valoriser ce qui est bien fait — ton positif]

---

## Recommandations Prioritaires

[3 actions concrètes, dans l'ordre d'impact]

---

## Prochaine Étape

[CTA appel 30 min — pas de tarif]

---
*Rapport généré par IA-Agency Polynésie — [date]*
```

---

## Gestion des cas difficiles

### Si aucune trace n'est trouvée
→ Niveau 0 confirmé
→ Message adapté : "Nous n'avons trouvé aucune trace digitale de [nom].
Cela ne signifie pas que l'entreprise n'existe pas — mais pour vos futurs clients,
elle est actuellement invisible sur internet."

### Si plusieurs entreprises portent le même nom
→ Demander une précision : "Plusieurs entreprises portent ce nom.
Pouvez-vous préciser : ville / île / type d'activité ?"
→ Ou lister les correspondances trouvées et demander laquelle analyser

### Si l'entreprise est introuvable mais le nom est très spécifique
→ Tenter avec des variantes orthographiques
→ Mentionner dans le rapport : "La recherche a été effectuée avec plusieurs
variantes du nom. Si l'entreprise utilise un nom différent en ligne,
merci de nous le préciser."

---

## Output

Fichier : `GEO-DISCOVER-[nom-nettoyé]-[date].md`

Données JSON consolidées : passées à `geo-readiness` si invoqué en amont.
