# Goal — geo-proposal

## Objectif d'optimisation

Faire en sorte que chaque proposition commerciale soit structurée, personnalisée,
présente des options claires (pas une liste infinie de services), et se termine
par une prochaine étape concrète.

## Seuil de qualité

**Target pass_rate : 0.85** (6/7 assertions minimum)

## Assertions testées

| ID | Assertion | Poids | Description |
|----|-----------|-------|-------------|
| A1 | assert_client_name | CRITIQUE | Mentionne le nom du client / de l'entreprise cible |
| A2 | assert_options_present | HAUTE | Contient au minimum 2 options tarifaires différentes |
| A3 | assert_next_step | HAUTE | Contient une prochaine étape concrète (pas un vague "à discuter") |
| A4 | assert_no_jargon | MOYENNE | Pas de jargon technique incompréhensible pour un non-initié |
| A5 | assert_problem_recap | HAUTE | Rappelle les problèmes identifiés lors de l'audit (preuve de personnalisation) |
| A6 | assert_timeline | MOYENNE | Mentionne un délai de livraison estimé |
| A7 | assert_length_ok | BASSE | Moins de 1 500 mots (proposition lisible en < 5 minutes) |

## Jargon à éviter (A4)

```
robots.txt, sitemap.xml, schema.org, llms.txt, Core Web Vitals,
PageSpeed Insights, Search Console, canonical, hreflang,
structured data, JSON-LD, Open Graph
```

## Historique des itérations

| # | Modification | Pass rate | Décision |
|---|-------------|-----------|----------|
| 0 | Baseline | —% | — |

## Notes

- La proposition est générée APRÈS le closing oral — c'est la formalisation écrite
- Les options tarifaires DOIVENT apparaître ici (contrairement au teaser-report)
- Maximum 3 options pour éviter la paralysie du choix
- Le recap des problèmes prouve qu'on a écouté, pas juste envoyé un template
