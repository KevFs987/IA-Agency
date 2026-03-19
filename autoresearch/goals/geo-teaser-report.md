# Goal — geo-teaser-report

## Objectif d'optimisation

Faire en sorte que chaque rapport teaser généré respecte à 100% la règle
"Révéler le problème. Taire la solution." et déclenche une envie d'appel.

## Seuil de qualité

**Target pass_rate : 0.85** (6/7 assertions minimum)

## Assertions testées

| ID | Assertion | Poids | Description |
|----|-----------|-------|-------------|
| A1 | assert_no_forbidden_words | CRITIQUE | Aucun mot interdit (tarif, prix, solution, plan d'action, robots.txt, schema, SEO, GEO, llms.txt, sitemap) |
| A2 | assert_score_present | HAUTE | Le rapport contient un score XX/100 |
| A3 | assert_three_problems | HAUTE | Exactement 3 problèmes critiques identifiés |
| A4 | assert_cta_present | HAUTE | Une question ouverte finale OU un appel à l'action vers un échange |
| A5 | assert_length_ok | MOYENNE | Moins de 800 mots (≈ 2 pages) |
| A6 | assert_no_solutions | CRITIQUE | Pas de liste de recommandations ou d'actions à faire |
| A7 | assert_positive_present | BASSE | Au moins 1 point positif mentionné (objectivité) |

## Mots interdits (A1)

```
tarif, prix, devis, coût, €, euro, offre, prestation,
plan d'action, recommandations, solutions, robots.txt,
schema.org, llms.txt, sitemap, SEO, GEO, balise, meta tag,
Google Search Console, Search Console, PageSpeed, Core Web Vitals
```

## Historique des itérations

| # | Modification | Pass rate | Décision |
|---|-------------|-----------|----------|
| 0 | Baseline | —% | — |

## Notes

- Le rapport doit pouvoir être lu par un propriétaire de commerce sans connaissances digitales
- Le ton doit être bienveillant, pas accusateur
- La question finale doit créer une curiosité, pas une pression commerciale
