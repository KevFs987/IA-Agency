---
name: geo-prep-call
description: >
  Génère un briefing commercial complet avant un RDV avec un prospect.
  Profil du prospect, points faibles classés par priorité, questions à poser,
  objections probables avec réponses suggérées, et stratégie de closing.
  C'est ici, et seulement ici, que les tarifs peuvent apparaître.
version: 1.0.0
author: geo-seo-claude / IA-Agency Polynésie
tags: [geo, commercial, prep, rdv, briefing, closing, polynesie, vente]
allowed-tools: Read, Write, WebFetch, Bash, Glob
---

# GEO Prep-Call — Briefing Commercial Avant RDV

> **Usage** : `/geo prep-call <url-ou-nom>`
>
> Exemples :
> - `/geo prep-call https://hotel-kia-ora.pf`
> - `/geo prep-call "Restaurant Te Moana Moorea"`
> - `/geo prep-call PRO-004` (ID prospect CRM)

---

## Objectif

Transformer un RDV commercial en closing.
Ce document est **strictement confidentiel** — jamais partagé avec le prospect.
C'est le seul endroit où les tarifs peuvent apparaître.

---

## Phase 0 — Contexte depuis knowledge/ (optionnel)

Avant d'exécuter ce skill, charger le contexte disponible dans la base de connaissances.

1. `Glob("knowledge/marche/*.md")` + `Glob("knowledge/scoring/*.md")` + `Glob("knowledge/inspiration/*.md")`
2. Si notes présentes → `Read` les 1 à 3 plus récentes dont le champ `expires` est supérieur à la date du jour
3. Extraire les sections `## Implications scoring` et `## Idées d'implémentation`
4. Intégrer ces données dans l'analyse, les recommandations et les livrables de ce skill

→ **Si `knowledge/` est absent ou vide : passer directement à l'étape suivante (non-bloquant)**

---

## Étape 1 — Chargement du dossier prospect

Chercher dans `~/.geo-prospects/prospects.json` l'entrée correspondante.
Sinon, lancer un audit rapide pour reconstruire le profil.

Charger :
- Données d'audit (score, niveau, gaps)
- Notes CRM (interactions précédentes)
- Teaser report envoyé (si existant)
- Message d'outreach envoyé (si existant)
- Statut actuel dans le pipeline

---

## Étape 2 — Génération du Briefing

### Structure du document

---

```markdown
# Briefing RDV — [Nom de l'entreprise]
📅 RDV prévu : [date si connue]
⏱ Durée recommandée : 30-45 minutes
🎯 Objectif : [Qualifier + proposer / Proposer / Closer selon le stade]

---

## 1. Profil du Prospect

| Élément | Détail |
|---------|--------|
| Entreprise | [Nom] |
| Secteur | [Secteur] |
| Localisation | [Ville / île] |
| Contact | [Prénom + rôle si connu — propriétaire, gérant, directeur marketing] |
| Source | [Comment tu les as trouvés — prospection, recommandation, inbound] |
| Historique contact | [Teaser envoyé le X / DM envoyé le X / aucun] |

### Ce qu'on sait d'eux

[2-3 phrases sur l'entreprise : taille apparente, ancienneté estimée,
clientèle cible (locaux / touristes / B2B), ton de leur communication,
points forts remarqués]

---

## 2. Situation Digitale (résumé de l'audit)

**Score de maturité : [XX]/100 — Niveau [X]/4**

| Ce qui fonctionne | Ce qui manque |
|------------------|---------------|
| [Point positif 1] | [Gap critique 1] |
| [Point positif 2] | [Gap critique 2] |
| [Point positif 3] | [Gap critique 3] |

### Les 3 douleurs à exploiter en RDV

**Douleur #1 — [Titre]**
> Ce qu'on a trouvé : [Fait précis]
> Comment le formuler au prospect : "[Reformulation en impact business —
> ex : 'Quand un touriste cherche votre type d'activité sur ChatGPT,
> il voit vos 3 concurrents avant de voir votre nom']"
> Niveau d'urgence : 🔴 Critique / 🟡 Important / 🟢 Moyen

**Douleur #2 — [Titre]**
> Ce qu'on a trouvé : [Fait précis]
> Comment le formuler au prospect : "[Reformulation]"
> Niveau d'urgence : [🔴 / 🟡 / 🟢]

**Douleur #3 — [Titre]**
> Ce qu'on a trouvé : [Fait précis]
> Comment le formuler au prospect : "[Reformulation]"
> Niveau d'urgence : [🔴 / 🟡 / 🟢]

---

## 3. Questions à Poser

L'objectif des questions : laisser le prospect **s'auto-convaincre**.
Poser des questions auxquelles la réponse naturelle crée une douleur.

### Questions d'ouverture (5-10 premières minutes)
1. "Comment vos clients vous trouvent-ils actuellement ?"
2. "Quelle proportion de votre clientèle vient des touristes ?"
3. "Est-ce que vous recevez des réservations / commandes directement depuis internet ?"

### Questions de qualification (comprendre le budget implicite)
4. "Vous avez déjà travaillé avec quelqu'un sur votre visibilité en ligne ?"
5. "Qu'est-ce qui vous a décidé à accepter cet appel ?"
6. "Si vous deviez doubler votre chiffre d'affaires d'ici un an, ça ressemblerait à quoi ?"

### Questions de douleur (après avoir montré les données)
7. "Quand vous cherchez '[type d'activité] [île]' sur Google, vous vous attendez
   à vous voir en premier ?" [montrer qu'ils ne sont pas là]
8. "Vous avez une idée du nombre de personnes qui ont cherché quelque chose
   comme ça le mois dernier ?" [réponse : des centaines / des milliers]
9. "Est-ce que ça vous dérange de savoir que ces personnes ont atterri
   chez votre concurrent ?"

### Questions de projection (vers la solution)
10. "Si on réglait ça ensemble, qu'est-ce que ça changerait concrètement pour vous ?"
11. "C'est quoi votre principale contrainte là : le temps, ou le budget ?"

---

## 4. Objections Probables & Réponses

### "Je n'ai pas le budget pour ça"

**Ce que ça veut vraiment dire :** "Je ne vois pas encore la valeur."
**Réponse suggérée :**
> "Je comprends. C'est pour ça que je vous pose la question différemment :
> combien vous coûte chaque client que vous ne captez pas ? Si vous avez
> [N] clients par mois, et qu'on peut augmenter ça de 20-30% avec une
> visibilité correcte, est-ce que l'investissement s'auto-finance ?"

---

### "On fait déjà de la pub Facebook / Google Ads"

**Ce que ça veut vraiment dire :** "On investit déjà dans le digital."
**Réponse suggérée :**
> "C'est très bien — ça veut dire que vous croyez déjà dans le digital.
> La différence c'est que la pub s'arrête dès que vous arrêtez de payer.
> Ce qu'on fait, c'est créer une présence organique permanente — vous
> continuez à apparaître même quand le budget pub est à zéro."

---

### "J'ai déjà quelqu'un qui s'en occupe / mon neveu fait ça"

**Ce que ça veut vraiment dire :** "Je ne veux pas payer pour ça."
**Réponse suggérée :**
> "Super. Est-ce que vous savez si votre site apparaît quand on cherche
> '[requête spécifique]' sur ChatGPT ?" [montrer que non]
> "C'est un aspect assez récent — les IA comme ChatGPT ne fonctionnent
> pas comme Google. C'est différent de ce qu'on faisait avant 2024."

---

### "C'est trop compliqué / j'ai pas le temps"

**Réponse suggérée :**
> "C'est exactement pour ça qu'on existe — pour que vous n'ayez pas à
> vous en occuper. Vous continuez à faire ce que vous faites bien.
> On s'occupe du reste."

---

### "Je vais réfléchir"

**Ce que ça veut vraiment dire :** "Je ne suis pas encore convaincu."
**Réponse suggérée :**
> "Bien sûr. À quoi vous allez réfléchir exactement ? [laisser répondre]
> C'est souvent une question sur X — est-ce qu'on peut l'adresser maintenant ?"

Ou :
> "Je comprends. Si dans 3 mois la situation est identique, est-ce que
> ça aurait des conséquences pour votre business ?" [créer l'urgence]

---

### "Vous n'êtes pas locaux / je préfère travailler avec quelqu'un d'ici"

[Si applicable]
**Réponse suggérée :**
> "Je travaille exclusivement avec des entreprises polynésiennes.
> C'est même pour ça que j'ai développé cet outil — il est pensé pour
> la réalité locale : les commerces sans site, Facebook comme vitrine,
> les touristes qui cherchent en anglais sur ChatGPT."

---

## 5. Structure Recommandée du RDV (30-45 min)

```
⏱ 0-5 min    — Introduction, ice-breaker, valider le temps disponible
⏱ 5-15 min   — Questions d'ouverture et de qualification (écouter 80%)
⏱ 15-25 min  — Présenter les données de l'audit (montrer, pas pitcher)
⏱ 25-35 min  — Questions de douleur, laisser le prospect réagir
⏱ 35-40 min  — Présenter la solution (si le terrain est préparé)
⏱ 40-45 min  — Prochaine étape concrète (pas "je réfléchis")
```

---

## 6. Offre à Proposer

[C'est ici que les tarifs apparaissent — UNIQUEMENT dans ce document]

Basé sur le niveau de maturité détecté ([X]/4), l'offre adaptée est :

### Si Niveau 0-1 (sans site, sans base) — Phase 1 de la roadmap

**Offre recommandée : "Démarrage Digital"**
- Google My Business créé et optimisé
- Site one-page FR/EN (depuis contenu social existant)
- Schema.org LocalBusiness + base SEO
- Configuration pour être visible sur ChatGPT / Perplexity
- Délai : 2-4 semaines

**Fourchette prix :** 300-600€ (one-shot)
**Argument ROI :** "Pour le coût d'un repas pour 2 par jour pendant 3 mois,
vous avez une présence digitale qui travaille pour vous 24h/24."

---

### Si Niveau 2-3 (site existant, SEO partiel) — Phase 2 de la roadmap

**Offre recommandée : "Optimisation & Visibilité IA"**
- Audit GEO complet
- Optimisation technique (schema, robots.txt, vitesse)
- Optimisation contenu pour citabilité IA
- llms.txt + configuration crawlers IA
- Rapport mensuel d'évolution

**Fourchette prix :** 500-1 200€/mois (retainer)
**Argument ROI :** "Chaque mois sans optimisation, vos concurrents avancent.
Le retainer, c'est un assistant marketing qui travaille en arrière-plan."

---

### Si grand compte (hôtel, groupe) — Phase 3

**Offre recommandée : "GEO Complet + Contenu"**
- Audit GEO complet
- Stratégie de contenu bilingue FR/EN
- Optimisation pour touristes anglophones
- Présence sur plateformes de réservation IA
- Rapport mensuel + accompagnement

**Fourchette prix :** 2 000-5 000€/mois
**Argument ROI :** "Une seule réservation directe supplémentaire par semaine
couvre l'investissement — sans les commissions Booking."

---

## 7. Prochaine Étape à Proposer

**Toujours terminer le RDV avec une action concrète.**

Options selon le résultat du RDV :
- ✅ Accord → "Je vous envoie le devis aujourd'hui, on se rappelle vendredi pour valider"
- 🟡 Intéressé mais pas décidé → "Je vous envoie un exemple de résultat pour une
  entreprise similaire. Vous voulez qu'on se rappelle dans une semaine ?"
- 🔴 Non → "Pas de souci. Vous avez ma carte. Si votre situation change,
  n'hésitez pas." [rester en bons termes — le marché est petit]

---
*Briefing confidentiel — IA-Agency Polynésie — [date]*
*Ne pas partager avec le prospect*
```

---

## Output

Fichier : `GEO-PREP-CALL-[nom-nettoyé]-[date].md`

Enregistrer dans le CRM :
```
/geo prospect note <id> "Prep-call généré le [date] — RDV prévu : [date si connue]"
```
