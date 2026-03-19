# Contexte stratégique — Fork geo-seo-claude
# Marché cible : Polynésie française

Ce fichier donne à Claude Code le contexte complet du projet.
Lire ce fichier avant toute tâche de développement ou d'audit.

---

## 1. Ce que ce fork est censé devenir

Ce n'est pas un simple clone du repo de Zoubair Trabzada.
C'est la base d'une **agence marketing IA locale** adaptée au marché polynésien,
avec des extensions qui n'existent pas dans le repo original.

L'objectif final : un seul outil qui permet à une personne de gérer
15 à 20 clients avec les marges d'un logiciel, pas d'une agence traditionnelle.

---

## 2. Limites du repo original à garder en tête

- L'outil suppose qu'une URL de site web existe en entrée → **non valide pour ~50% du marché local**
- C'est un outil d'audit uniquement → il ne produit pas de contenu, n'exécute pas les recommandations
- Le scoring est empirique (non validé scientifiquement) → ne pas le vendre comme une vérité absolue
- Pas de volet commercial → le rapport complet ne doit jamais mentionner de tarif

---

## 3. Spécificité marché — Polynésie française

### Tissu économique local
- Beaucoup de TPE/PME peu digitalisées
- Quelques grands comptes (hôtels, groupes touristiques)
- Marché petit et fermé — la réputation (bonne ou mauvaise) circule vite
- Fort potentiel tourisme et e-commerce

### Réalité digitale locale — point critique
**La majorité des petits commerces n'ont pas de site web.**
Ils utilisent leur page Facebook, Instagram, et de plus en plus TikTok
comme unique vitrine digitale.

Cela crée 3 types d'input que l'outil doit gérer :
- **Cas A** — Site web existant → flux d'audit GEO classique (déjà dans le repo)
- **Cas B** — Social only (Facebook/Instagram/TikTok) → nouveau flux à développer
- **Cas C** — Nom de marque seul, aucune présence détectable → nouveau flux à développer

### Langues
Les entreprises locales communiquent en **français et en anglais** selon la cible.
Les touristes (clients potentiels des hôtels/restos) cherchent en anglais sur ChatGPT.
Toute production de contenu doit être pensée **bilingue FR/EN par défaut**.

---

## 4. Extensions prioritaires à développer dans ce fork

### Extension 1 — geo-social (PRIORITÉ HAUTE)
Nouveau sous-agent qui accepte une URL Facebook, Instagram ou TikTok en entrée.

Ce qu'il doit faire :
- Extraire : nom de marque, description, type de contenu posté, fréquence de publication
- Détecter les signaux d'autorité existants (nombre d'abonnés, avis, engagement)
- Identifier les gaps (pas de site, pas de Google My Business, pas de schéma, etc.)
- Produire un score de maturité digitale (0-100) adapté au niveau réel de l'entreprise

Commande cible : `/geo audit https://facebook.com/nom-du-commerce`

### Extension 2 — geo-discover (PRIORITÉ HAUTE)
Nouveau sous-agent qui accepte un simple nom de marque en entrée (pas d'URL).

Ce qu'il doit faire :
- Rechercher toutes les traces digitales existantes :
  Google Maps, TripAdvisor, Pages Jaunes, Facebook, Instagram, Wikipedia, etc.
- Reconstruire un profil de présence digitale complet
- Identifier le niveau de maturité et les gaps prioritaires

Commande cible : `/geo audit "Resto Te Moana Moorea"`

### Extension 3 — geo-readiness (PRIORITÉ HAUTE)
Nouveau rapport qui remplace le GEO Score classique pour les entreprises sans site web.

Le rapport positionne l'entreprise sur un spectre de maturité à 5 niveaux :
- Niveau 0 — Présence zéro (aucune trace digitale)
- Niveau 1 — Social only (Facebook/Instagram/TikTok uniquement)
- Niveau 2 — Site basique sans SEO
- Niveau 3 — Site avec SEO traditionnel
- Niveau 4 — GEO-ready (cible finale)

Pour chaque niveau : plan d'action concret + estimation de coût.
Ce rapport est à la fois l'outil de prospection ET le premier livrable client.

Commande cible : `/geo readiness <url ou nom>`

### Extension 4 — geo-social-to-site (PRIORITÉ MOYENNE)
Agent qui récupère le contenu existant d'une page sociale (photos, descriptions, posts)
et génère les specs d'un site one-page bilingue FR/EN.
Le site réutilise le contenu que l'entreprise produit déjà sur ses réseaux.

### Extension 5 — Volet contenu (PRIORITÉ MOYENNE)
- `/geo write-article <url> <topic>` — article optimisé pour les blocs citables (134-167 mots)
- `/geo rewrite-page <url>` — réécriture E-E-A-T d'une page existante
- `/geo content-calendar <url> <months>` — calendrier éditorial basé sur les gaps détectés

### Extension 6 — Volet commercial / sales (PRIORITÉ HAUTE)
C'est la couche qui transforme l'outil en machine à prospecter.

Règle d'or commerciale à intégrer dans tous les rapports :
**Révéler le problème. Taire la solution.**
Un rapport livré en prospection ne doit jamais mentionner de tarif.

Commandes à développer :
- `/geo prospect <niche> <ville>` — scrape une liste d'entreprises locales,
  lance un `/geo quick` sur chacune, filtre les scores sous 50, génère une liste priorisée
- `/geo outreach <url>` — génère un message de prospection personnalisé
  basé sur les problèmes spécifiques trouvés (pas un template générique)
- `/geo teaser-report <url>` — rapport PDF volontairement incomplet,
  2 pages max, montre le score + 3 problèmes, se coupe net avec un CTA vers un appel.
  NE PAS inclure les solutions. NE PAS mentionner de tarif.
- `/geo prep-call <url>` — briefing commercial avant RDV :
  profil du prospect, points faibles classés par priorité, questions à poser,
  objections probables avec réponses suggérées

---

## 5. Architecture cible du teaser-report

Ce que le rapport de prospection DOIT montrer :
- Le score global (ex : 34/100)
- Les 3 problèmes critiques nommés (sans expliquer comment les résoudre)
- L'impact business estimé ("vos clients touristes ne vous trouvent pas sur ChatGPT")
- Une question ouverte finale qui invite à l'appel

Ce que le rapport de prospection NE DOIT PAS contenir :
- Les solutions détaillées
- Le plan d'action complet
- Toute mention de tarif ou de prestation

---

## 6. Stratégie commerciale — l'audit sniper

Flux de prospection automatisé :
1. `/geo prospect "restaurants" "Papeete"` → liste de 20 leads scorés
2. `/geo outreach <url prospect>` → message personnalisé envoyé
3. `/geo teaser-report <url prospect>` → PDF 2 pages crée la douleur
4. Appel déclenché par le prospect
5. `/geo prep-call <url prospect>` → tu arrives préparé
6. Closing — le tarif n'apparaît que dans ce contexte oral, jamais dans un PDF

---

## 7. Feuille de route en 3 phases

### Phase 1 — 0 à 6 mois
- Produit : site one-page + Google My Business via IA
- Cible : commerces et restaurants locaux (volume, besoin criant, vitrine)
- Ticket : 300 à 600 €
- Rôle de l'outil : prospection uniquement (teaser-report + outreach)

### Phase 2 — 6 à 18 mois
- Produit : SEO + contenu IA en retainer mensuel
- Cible : PME avec base digitale existante
- Ticket : 500 à 1 200 €/mois
- Rôle de l'outil : livraison + monitoring continu

### Phase 3 — 18 mois+
- Produit : GEO complet + tourisme grands comptes
- Cible : hôtels, groupes, SaaS locaux
- Ticket : 2 000 à 5 000 €/mois
- Rôle de l'outil : central, full-stack agence

---

## 8. Pitch adapté au marché polynésien

Pour les commerces sans site web :
"Vous produisez déjà du super contenu sur Instagram et TikTok.
Je vous aide à ce que ce contenu travaille aussi pour vous sur Google
et sur ChatGPT — là où vos futurs clients touristes cherchent
avant même d'arriver en Polynésie."

Pour les hôtels avec un site existant :
"J'ai analysé votre visibilité sur ChatGPT et Perplexity.
Quand un touriste américain cherche 'best overwater bungalow French Polynesia',
vous n'apparaissez pas dans les réponses. Voici pourquoi et comment y remédier."

---

## 9. Ce que ce fork apporte au repo original

Ces extensions sont universelles — pas seulement utiles en Polynésie.
Le cas "Social only" existe dans tous les marchés émergents :
Afrique subsaharienne, Caraïbes, îles du Pacifique, TPE en Europe.

L'objectif à terme : soumettre une Pull Request au repo de Zoubair
avec les agents geo-social et geo-discover comme contribution open source.

---

## 10. Contraintes de développement

- Respecter l'architecture existante : skills dans /skills, agents dans /agents
- Chaque nouvelle commande doit avoir son propre SKILL.md dans /skills/geo-[nom]/
- Les nouveaux agents vont dans /agents/
- Le routage se fait dans /geo/SKILL.md — mettre à jour ce fichier pour chaque nouvelle commande
- Maintenir la compatibilité avec l'installateur install.sh existant
- Tester chaque nouvelle skill sur un site .pf (domaine polynésien) avant de merger

---

*Ce fichier est la mémoire stratégique du projet.
Le mettre à jour à chaque décision importante.*