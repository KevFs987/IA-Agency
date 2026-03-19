---
name: geo-outreach
description: >
  Génère un message de prospection personnalisé basé sur les problèmes
  spécifiques trouvés lors de l'audit. PAS un template générique.
  Chaque message est écrit pour une entreprise précise, avec ses problèmes réels.
  Disponible en FR et EN selon la cible. Formats : email, DM Facebook/Instagram, WhatsApp.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, outreach, prospection, email, message, commercial, polynesie]
allowed-tools: Read, Write, WebFetch, Bash, Glob
---

# GEO Outreach — Message de Prospection Personnalisé

> **Usage** : `/geo outreach <url-ou-nom>`
>
> Exemples :
> - `/geo outreach https://facebook.com/restaurant-te-moana`
> - `/geo outreach "Hôtel Kia Ora Rangiroa"`
> - `/geo outreach https://surf-school-tahiti.pf`

---

## ⚠️ Principe fondamental

**Ce message n'est pas un template.**

Un template générique se voit à 100m et va dans les spams.
Ce message est construit à partir des **vrais problèmes** trouvés lors de l'audit.
Le prospect doit sentir qu'on a regardé sa situation spécifique — parce que c'est le cas.

---

## Étape 1 — Chargement des données d'audit

Chercher dans `~/.geo-prospects/` si un audit existe pour ce prospect.
Sinon, lancer un audit rapide :
- URL site → `/geo quick`
- URL sociale → `geo-social`
- Nom → `geo-discover`

Extraire au minimum :
```
- Nom de l'entreprise
- Secteur d'activité
- Niveau de maturité (0-4)
- Score (0-100)
- Les 3 problèmes prioritaires (réels, pas génériques)
- 1-2 points positifs (authenticité)
- Canaux de contact disponibles (email, Facebook, Instagram, WhatsApp, téléphone)
- Langue probable de la cible (FR ou EN)
```

---

## Étape 2 — Déterminer le canal et la langue

### Canal recommandé par priorité

| Canal | Quand l'utiliser |
|-------|-----------------|
| **Email direct** | Si un email est disponible (site web, GMB, Pages Jaunes) |
| **DM Facebook** | Si la page Facebook est active et pas d'email trouvé |
| **DM Instagram** | Si compte Instagram actif et public, pas d'email |
| **WhatsApp** | Si numéro WhatsApp visible sur le profil (courant en Polynésie) |
| **Message Facebook** | Fallback si rien d'autre |

### Langue

| Cible | Langue |
|-------|--------|
| Commerce local, restaurant, service B2C local | Français |
| Hôtel, activité touristique, business expat | Français + version EN optionnelle |
| Activité visant touristes anglophones | Anglais en priorité |

---

## Étape 3 — Rédaction du message

### Structure universelle (adapter le ton au canal)

```
[Accroche personnalisée — UNE phrase qui montre qu'on connaît leur situation]

[Présentation très courte — 1-2 lignes max]

[Observation spécifique #1 — un problème réel trouvé, formulé en impact business]

[Observation spécifique #2 — optionnel si le message est court]

[Question d'invitation à l'échange — pas un pitch, pas une vente]

[Signature courte]
```

---

### Templates par canal (à personnaliser avec les données réelles)

#### Email — Ton professionnel

```
Objet : [Nom de l'entreprise] — [problème court en 5 mots]

Bonjour [Prénom si connu / nom du propriétaire si trouvé],

[Accroche : mentionner quelque chose de spécifique — leur page Facebook,
leur fiche Google Maps, une photo vue sur leur profil, un avis récent.]

Exemple : "Je suis tombé sur votre restaurant en cherchant les meilleures
tables de Moorea pour des amis qui arrivent en avril."

Je m'appelle [Prénom], je travaille sur la visibilité digitale des entreprises
polynésiennes — en particulier leur présence sur Google et les intelligences
artificielles que les touristes utilisent pour planifier leur voyage.

En regardant rapidement votre présence en ligne, j'ai remarqué [problème
spécifique réel — ex : "que votre restaurant n'apparaît pas dans les réponses
ChatGPT quand on cherche 'meilleur restaurant Moorea'"]. Pour un établissement
de votre qualité, c'est des réservations qui partent chez vos voisins.

Seriez-vous disponible pour un échange rapide de 20 minutes cette semaine ?
Je peux vous montrer exactement ce qui se passe et ce que ça représente.

Bonne continuation,
[Prénom]
IA-Agency — [téléphone]

[PS optionnel : "Je vous joins une courte analyse si vous voulez voir
les détails avant notre appel." → joindre le teaser-report]
```

---

#### DM Facebook / Instagram — Ton décontracté

```
Bonjour ! 👋

Je suis tombé sur votre [page / profil] en cherchant [contexte naturel].
Super contenu, [commentaire sincère sur quelque chose de spécifique].

Je travaille sur la visibilité digitale des commerces polynésiens,
notamment leur présence sur Google et les IA utilisées par les touristes.

Question directe : savez-vous si votre [restaurant / hôtel / boutique]
apparaît quand quelqu'un cherche "[requête typique]" sur ChatGPT ou Google ?

J'ai regardé rapidement et [observation spécifique en 1 phrase].

Si ça vous intéresse, on peut s'appeler 20 minutes pour que je vous
montre ce que j'ai trouvé — sans engagement.

[Prénom] 🤙
```

---

#### WhatsApp — Ton conversationnel

```
Bonjour [Prénom si connu],

Je m'appelle [Prénom], je travaille sur la visibilité digitale
des entreprises locales ici en Polynésie.

J'ai vu votre [page Facebook / fiche Google / profil] et j'ai
une observation à partager avec vous — elle concerne [problème
en 1 phrase, formulé positivement : "comment vous pourriez capter
plus de clients touristes qui cherchent sur Google"].

Vous avez 20 minutes cette semaine pour qu'on en parle ?

Merci,
[Prénom]
```

---

#### Email EN — Pour cibles touristiques anglophones

```
Subject: [Business name] — quick observation about your online visibility

Hi [Name],

I came across [business name] while [natural context — researching restaurants
in Moorea / looking for activities in Tahiti / etc.].

I help local Polynesian businesses show up where tourists are actually
looking — Google, ChatGPT, and other AI tools people use to plan their trips.

I took a quick look at your online presence and noticed [specific problem
in plain language — e.g., "your hotel doesn't appear in ChatGPT responses
when someone searches for 'overwater bungalows French Polynesia'"]. For a
property like yours, that's real bookings going to competitors.

Would you be open to a 20-minute call this week so I can show you exactly
what I found?

Best,
[First name]
IA-Agency — [phone]
```

---

## Étape 4 — Règles de personnalisation

### Ce qui DOIT être personnalisé (pas optionnel)

1. **L'accroche** — mentionner quelque chose de spécifique vu sur leur profil
   (un post récent, un avis, le nom d'un plat, une photo, leur classement TripAdvisor)

2. **Le problème** — être précis. Pas "votre présence en ligne est insuffisante"
   mais "votre restaurant n'apparaît pas quand on cherche 'meilleur poisson Papeete'
   sur Google Maps"

3. **Le secteur** — adapter le vocabulaire (réservation vs commande vs visite vs stage)

### Ce qui doit RESTER HORS du message

- ❌ Tarifs ou fourchettes de prix
- ❌ Explications techniques (robots.txt, schema.org, etc.)
- ❌ Solutions détaillées
- ❌ Trop d'informations (max 150-200 mots pour email, 80-100 pour DM)
- ❌ Formules génériques ("votre entreprise mérite mieux" → poubelle)

---

## Étape 5 — Output

Générer **3 versions** du message pour que l'utilisateur choisisse :

1. **Version email** (ton professionnel)
2. **Version DM** (ton conversationnel)
3. **Version courte WhatsApp** (ultra-court)

Si la langue est mixte : générer aussi les versions EN.

Fichier : `GEO-OUTREACH-[nom-nettoyé]-[date].md`

Structure du fichier :
```markdown
# Messages de Prospection — [Nom de l'entreprise]
Date : [date]

## Contexte utilisé
- Score : [XX]/100
- Problème principal : [...]
- Canal recommandé : [...]

---

## Version 1 — Email (FR)
[message complet]

---

## Version 2 — DM Facebook / Instagram (FR)
[message complet]

---

## Version 3 — WhatsApp (FR)
[message complet]

---

## Version Email (EN) — si applicable
[message complet]
```

Enregistrer dans le CRM :
```
/geo prospect note <id> "Outreach rédigé le [date] — canal recommandé : [canal]"
```
