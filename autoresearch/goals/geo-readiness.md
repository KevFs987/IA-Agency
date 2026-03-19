# Goal — geo-readiness

## Objectif d'optimisation

Faire en sorte que chaque rapport readiness positionne clairement l'entreprise
sur le spectre 0-4, explique les gaps en langage client (pas technique),
et présente un chemin concret vers le niveau suivant.

## Seuil de qualité

**Target pass_rate : 0.85** (6/7 assertions minimum)

## Assertions testées

| ID | Assertion | Poids | Description |
|----|-----------|-------|-------------|
| A1 | assert_level_present | CRITIQUE | Contient "Niveau X/4" ou "Niveau X" clairement identifié (0-4) |
| A2 | assert_detection_table | HAUTE | Contient un tableau de présence (site, GMB, Facebook, etc.) |
| A3 | assert_action_plan | HAUTE | Contient des actions concrètes pour atteindre le niveau suivant |
| A4 | assert_no_tarif | CRITIQUE | Aucune mention de tarif ou de prix dans le rapport |
| A5 | assert_cta_present | HAUTE | Contient un CTA vers un appel de découverte |
| A6 | assert_no_jargon | MOYENNE | Pas de jargon technique (robots.txt, schema.org, llms.txt) dans les parties visibles client |
| A7 | assert_positive_tone | BASSE | Ne contient pas de formulations négatives ou condescendantes |

## Mots interdits (A4 + A6)

```
tarif, prix, devis, €, euro, coût, facturation,
robots.txt (dans sections client), schema.org (dans sections client),
llms.txt (dans sections client), Core Web Vitals
```

## Formulations condescendantes à éviter (A7)

```
"vous n'avez pas compris", "erreur grave", "catastrophique",
"incompétence", "très mauvais", "honte", "scandaleux"
```

## Historique des itérations

| # | Modification | Pass rate | Décision |
|---|-------------|-----------|----------|
| 0 | Baseline | —% | — |

## Notes

- Le rapport est à la fois outil de prospection ET premier livrable client
- Le niveau doit être clairement visible dès le résumé exécutif
- Les actions concrètes doivent être réalisables par le propriétaire en autonomie
- Le CTA ne doit jamais mentionner de tarif — seulement inviter à l'échange
