# Goal — geo-social

## Objectif d'optimisation

Faire en sorte que chaque audit social extrait les données clés d'une page
sociale, calcule un score 0-100 justifié, identifie les 3 gaps prioritaires
en langage client, et reste exploitable même quand les réseaux bloquent le fetch.

## Seuil de qualité

**Target pass_rate : 0.85** (6/7 assertions minimum)

## Assertions testées

| ID | Assertion | Poids | Description |
|----|-----------|-------|-------------|
| A1 | assert_score_present | CRITIQUE | Contient un score XX/100 clairement affiché |
| A2 | assert_platform_detected | HAUTE | Mentionne la plateforme analysée (Facebook / Instagram / TikTok) |
| A3 | assert_three_gaps | HAUTE | Contient exactement 3 gaps prioritaires numérotés |
| A4 | assert_hors_social_checked | HAUTE | Mentionne l'état de Google My Business au minimum |
| A5 | assert_no_tarif | CRITIQUE | Aucune mention de tarif ou de prix |
| A6 | assert_cta_present | HAUTE | Contient un CTA vers un échange ou un appel |
| A7 | assert_graceful_degradation | MOYENNE | Si données limitées, le rapport le mentionne explicitement et continue |

## Mots interdits (A5)

```
tarif, prix, devis, €, euro, coût, offre, prestation, contrat
```

## Critères de dégradation gracieuse (A7)

Le rapport mentionne explicitement si les données sont partielles :
- "Données partiellement accessibles"
- "Accès limité à la page"
- "Analyse basée sur les métadonnées disponibles"
- Tout équivalent clair

## Historique des itérations

| # | Modification | Pass rate | Décision |
|---|-------------|-----------|----------|
| 0 | Baseline | —% | — |

## Notes

- Les réseaux sociaux bloquent souvent le scraping — le skill doit gérer ce cas sans planter
- Le score doit être justifié par les composantes (présence sociale, contact, hors-social, etc.)
- Les gaps doivent parler business, pas technique
- Toujours mentionner les points positifs avant les gaps
