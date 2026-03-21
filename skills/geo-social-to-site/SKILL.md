---
name: geo-social-to-site
description: >
  Récupère le contenu existant d'une page sociale (photos, descriptions, posts, avis)
  et génère les specs complètes d'un site one-page bilingue FR/EN.
  Le site réutilise ce que l'entreprise produit déjà — zéro création from scratch.
  Livrable : brief de site complet, prêt à transmettre à un développeur ou un générateur IA.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, social, site, one-page, brief, bilingue, polynesie, local, creation]
allowed-tools: Read, Write, WebFetch, Bash
---

# GEO Social-to-Site — Specs de Site depuis Contenu Social

> **Usage** : `/geo social-to-site <url-sociale>`
>
> Exemples :
> - `/geo social-to-site https://facebook.com/restaurant-te-moana`
> - `/geo social-to-site https://www.instagram.com/surf_tahiti/`
> - `/geo social-to-site https://tiktok.com/@pension-chez-marie`

---

## Philosophie

> "Vous produisez déjà du super contenu sur Instagram et TikTok.
> Je vous aide à ce que ce contenu travaille aussi pour vous sur Google
> et sur ChatGPT — là où vos futurs clients touristes cherchent
> avant même d'arriver en Polynésie."

L'entreprise a déjà fait le travail : photos, descriptions, présentation,
valeurs, ambiance. Notre rôle est de **réorganiser et structurer** ce contenu
pour qu'il fonctionne sur un site web — sans demander au client de tout refaire.

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Étape 1 — Extraction du contenu social

### 1.1 Récupération

Faire un WebFetch de l'URL sociale fournie.

Extraire tout ce qui est accessible publiquement :

**Informations de base**
- Nom officiel de l'entreprise / page
- Catégorie / type d'activité
- Description / bio
- Localisation (adresse, île, commune)
- Numéro de téléphone
- Email (si visible)
- Site web listé (si déjà un site → adapter le brief en upgrade)
- Horaires d'ouverture (si mentionnés)
- Langues de communication (FR / EN / tahitien)

**Contenu existant**
- Texte de présentation (bio, à propos)
- Types de produits / services mentionnés dans les posts
- Prix mentionnés (si visibles)
- Événements ou offres spéciales récurrentes
- Mots-clés récurrents dans les posts (ambiance, valeurs, promesses)
- Hashtags utilisés (révèlent la stratégie de positionnement)

**Signaux visuels**
- Nombre de photos / vidéos disponibles
- Thèmes visuels dominants (mer, lagon, cuisine, famille, nature...)
- Présence de photos professionnelles vs. photos de terrain
- Logo visible ?

**Signaux de confiance**
- Nombre d'abonnés / likes
- Note et avis (si disponibles)
- Mentions de presse ou partenaires

**Note** : Si le fetch retourne une page vide (login wall) :
→ Travailler avec les métadonnées Open Graph disponibles
→ Indiquer dans le brief : "Photos à fournir par le client"

---

## Étape 2 — Analyse du positionnement

À partir du contenu extrait, déduire :

**Cible client principale**
- Touristes internationaux (→ site bilingue FR/EN prioritaire)
- Touristes français (→ FR dominant, EN secondaire)
- Clients locaux (→ FR uniquement possible)
- Mix (→ full bilingue)

**Proposition de valeur unique**
Identifier EN UNE PHRASE ce qui différencie cette entreprise.
Ne pas inventer — se baser sur ce qui est déjà dit dans les posts/bio.

Exemples :
- "Seul restaurant de Moorea avec vue panoramique sur le lagon et le Mont Rotui"
- "Pension familiale tenue par des locaux depuis 1998"
- "École de surf avec instructeurs certifiés ISA, spécialisée débutants"

**Ton de communication**
- Formel / institutionnel
- Décontracté / familial
- Aventurier / sportif
- Luxe / premium
- Authentique / artisanal

---

## Étape 3 — Architecture du site one-page

### Structure standard (adaptable selon le secteur)

Le site one-page suit un flux narratif unique :

```
1. HERO                 — Accroche immédiate + proposition de valeur
2. CE QUE NOUS FAISONS — Services / offres en 3-4 points clés
3. POURQUOI NOUS        — Différenciateurs (ce qui nous rend uniques)
4. GALERIE              — Photos tirées des réseaux sociaux
5. TÉMOIGNAGES / AVIS  — Extraits d'avis Google/Facebook/TripAdvisor
6. INFOS PRATIQUES      — Horaires, tarifs, localisation, accès
7. CONTACT / CTA        — Bouton de réservation / formulaire / WhatsApp
```

### Adaptations par secteur

**Restaurant / Bar**
```
Hero → Menu signature (3 plats emblématiques) → Histoire / Chef → Galerie plats+ambiance
→ Avis clients → Réservation + Carte Google Maps
```

**Hôtel / Pension**
```
Hero → Chambres (3 types max) → Expériences incluses → Galerie → Avis → Disponibilités + Contact
```

**Activité nautique / Excursion**
```
Hero → Ce qu'on propose (activités + durée + prix) → Sécurité / certifications
→ Galerie action → Avis → Réservation
```

**Commerce / Artisan**
```
Hero → Produits phares (3-6) → Notre histoire / savoir-faire → Galerie → Où nous trouver
→ Horaires + Contact
```

---

## Étape 4 — Génération des specs

### Format du brief de site

```markdown
# Brief Site One-Page — [Nom de l'entreprise]
**Source :** [URL sociale analysée]
**Date :** [date]
**Destination :** Développeur / Générateur IA (Webflow, Framer, WordPress, Gamma...)

---

## 1. Informations essentielles

| Élément | Valeur |
|---------|--------|
| Nom officiel | [Nom] |
| Secteur | [Restaurant / Hôtel / Activité / Commerce] |
| Localisation | [Adresse ou zone, île] |
| Langues du site | FR principal + EN secondaire / Full bilingue |
| Ton | [Décontracté / Professionnel / Luxe / Familial] |
| Cible principale | [Touristes internationaux / Locaux / Mix] |

---

## 2. Proposition de valeur (à mettre en Hero)

**FR :** [Phrase d'accroche principale — max 10 mots]
**EN :** [English version — adapted for tourist search intent]

**Sous-titre FR :** [1-2 phrases de contexte]
**Sous-titre EN :** [English version]

**CTA principal FR :** [Ex : "Réserver une table", "Nous contacter", "Voir nos offres"]
**CTA principal EN :** [Ex : "Book a Table", "Contact Us", "See Our Offers"]

---

## 3. Contenu de chaque section

### Section 1 — Hero
- Visuel recommandé : [Description de la photo idéale tirée des réseaux]
- Titre : [FR] / [EN]
- Sous-titre : [FR] / [EN]
- Bouton CTA : [FR] / [EN] → lien vers [Section 7 / WhatsApp / Formulaire]

### Section 2 — Ce que nous proposons
*[Adapter le titre selon le secteur : "Notre menu" / "Nos chambres" / "Nos activités"]*

| Offre | Description FR | Description EN | Prix (si applicable) |
|-------|---------------|----------------|---------------------|
| [Offre 1] | [Texte FR 20-30 mots] | [Text EN] | [Prix ou "Sur demande"] |
| [Offre 2] | [Texte FR] | [Text EN] | [...] |
| [Offre 3] | [Texte FR] | [Text EN] | [...] |

*Données sources : [mentions dans les posts / bio]*
*À confirmer avec le client : [éléments manquants]*

### Section 3 — Pourquoi nous ?
3 arguments différenciateurs, tirés du contenu social :

**Argument 1**
- Icône suggérée : [emoji ou icône]
- Titre FR : [...]  / EN : [...]
- Texte FR : [1-2 phrases] / EN : [...]
- Source : [basé sur : post du X / bio / avis client]

**Argument 2** [même format]

**Argument 3** [même format]

### Section 4 — Galerie
Recommandations visuelles basées sur le contenu détecté :

| # | Type de photo | Source recommandée | Note |
|---|---------------|-------------------|------|
| 1 | [Ex : Vue panoramique du restaurant] | [Disponible sur Facebook] | Photo phare — mettre en avant |
| 2 | [Ex : Plat signature] | [À demander au client] | Idéalement sur fond neutre |
| 3 | [Ex : Ambiance salle] | [Disponible sur Instagram] | |
| 4-6 | [Ex : Équipe / terrain] | [À demander] | |

**Nombre de photos recommandées :** 6-12
**Format :** Paysage 16:9 pour les grands formats, carré 1:1 pour la grille

### Section 5 — Avis clients
*Si des avis sont disponibles sur Facebook/Google/TripAdvisor :*

Sélectionner 2-3 avis représentatifs :
```
[Avis 1] — [Source] — [Note /5]
"[Texte de l'avis]"

[Avis 2] — [Source] — [Note /5]
"[Texte de l'avis]"
```

*Si pas d'avis disponibles :*
→ Indiquer : "Section avis à alimenter — demander au client 2-3 témoignages"

### Section 6 — Infos pratiques

| Info | Valeur FR | Valeur EN |
|------|-----------|-----------|
| Adresse | [...] | [...] |
| Horaires | [...] | [...] |
| Téléphone | [...] | *same* |
| Email | [...] | *same* |
| Parking / Accès | [...] | [...] |
| Carte Google Maps | Embed du point GPS | *same* |

### Section 7 — Contact / Réservation

**Option recommandée selon le secteur :**
- Restaurant → Bouton réservation (lien vers TheFork / Google / formulaire) + WhatsApp
- Hôtel → Formulaire de demande de disponibilité + lien Booking si applicable
- Activité → Formulaire de réservation avec date + nombre de personnes
- Commerce → Formulaire de contact simple + horaires bien visibles

**Texte CTA FR :** [...]
**Texte CTA EN :** [...]

---

## 4. SEO — Métadonnées

### Page principale (FR)
```
<title>[Nom] — [Type d'activité] à [Localisation] | [Île]</title>
<meta description="[Description 150-160 chars incluant : nom, activité, lieu, proposition de valeur]">
```

### Page EN (ou attribut hreflang)
```
<title>[Name] — [Activity type] in [Location], [Island], French Polynesia</title>
<meta description="[Description in English — adapted for tourist search queries]">
```

### Schema.org recommandé
```json
{
  "@context": "https://schema.org",
  "@type": "[Restaurant / LodgingBusiness / TouristAttraction / Store]",
  "name": "[Nom officiel]",
  "description": "[Description 1-2 phrases]",
  "url": "[URL du futur site]",
  "telephone": "[Numéro]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Adresse]",
    "addressLocality": "[Ville / Commune]",
    "addressRegion": "Polynésie française",
    "addressCountry": "PF"
  },
  "sameAs": [
    "[URL Facebook]",
    "[URL Instagram]",
    "[URL Google Maps si disponible]",
    "[URL TripAdvisor si disponible]"
  ]
}
```

---

## 5. Recommandations techniques

| Élément | Recommandation | Pourquoi |
|---------|---------------|---------|
| Plateforme | Webflow / Framer / WordPress + Elementor | Facilité de maintenance par le client |
| Hébergement | OVH / Infomaniak (serveurs FR) | Conformité RGPD, latence réduite |
| Domaine | [nom].pf (si dispo) ou [nom].com | .pf renforce le positionnement local |
| HTTPS | Obligatoire | Confiance + référencement |
| Mobile-first | Oui — 70%+ du trafic touristique est mobile | |
| Vitesse | Images < 200 Ko, WebP | Core Web Vitals |
| Google Analytics | GA4 minimal | Suivi du trafic |
| Google Search Console | Vérifier dès la mise en ligne | Indexation rapide |

---

## 6. Ce qu'on a — Ce qu'il manque

### Disponible depuis les réseaux sociaux
- [x] Nom, description, localisation
- [x] [Liste de ce qui a pu être extrait]

### À collecter auprès du client
- [ ] [Élément manquant 1 — ex : "Logo en haute résolution (format PNG fond transparent)"]
- [ ] [Élément manquant 2 — ex : "Menu complet avec prix à jour"]
- [ ] [Élément manquant 3 — ex : "Horaires d'ouverture détaillés"]
- [ ] [Élément manquant 4 — ex : "Email de contact professionnel"]
- [ ] [Photos haute résolution — [N] photos recommandées]

---

## 7. Prochaines étapes suggérées

1. Partager ce brief avec le client pour validation (15-20 min)
2. Collecter les éléments manquants (liste section 6)
3. Choisir la plateforme de création
4. Créer le domaine `.pf` ou `.com`
5. Développement : [2-5 jours selon la plateforme]
6. Mise en ligne + vérification Google Search Console
7. Soumettre à Google Maps + TripAdvisor si pas encore fait
8. Optionnel : `/geo write-article <url> "<sujet>"` pour le premier article de blog

---
*Brief généré par IA-Agency Polynésie — [date]*
*Ce document est la propriété de [Nom de l'entreprise]*
```

---

## Règles d'or

- **Réutiliser, pas recréer** — tout le contenu doit venir du social ou être clairement marqué "à demander"
- **Jamais inventer** des infos (prix, horaires, certifications) — marquer `[À CONFIRMER]`
- **Bilingue systématique** si la cible inclut des touristes
- **Schema.org toujours inclus** — c'est ce qui permet d'être cité par les IA
- **Le brief doit être compréhensible par quelqu'un qui n'a pas vu les réseaux** — tout le contexte est dans le document

---

## Output

Fichier : `SITE-BRIEF-[nom-nettoyé]-[date].md`

Enregistrer dans le CRM :
```
/geo prospect note <id> "Brief site one-page généré le [date]"
/geo prospect status <id> qualified
```
