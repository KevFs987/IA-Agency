# Goal — geo-outreach

## Objectif d'optimisation

Faire en sorte que chaque message de prospection soit suffisamment personnalisé
pour ne pas ressembler à un template, court enough pour être lu en entier,
et se termine par une invitation à l'échange sans jamais vendre.

## Seuil de qualité

**Target pass_rate : 0.85** (6/7 assertions minimum)

## Assertions testées

| ID | Assertion | Poids | Description |
|----|-----------|-------|-------------|
| A1 | assert_no_forbidden_words | CRITIQUE | Aucun mot interdit (tarif, prix, devis, solution, robots.txt, schema, SEO, GEO) |
| A2 | assert_three_versions | HAUTE | Contient exactement 3 versions (email, DM, WhatsApp) |
| A3 | assert_email_length | HAUTE | Version email ≤ 200 mots |
| A4 | assert_dm_length | HAUTE | Version DM ≤ 100 mots |
| A5 | assert_whatsapp_length | MOYENNE | Version WhatsApp ≤ 80 mots |
| A6 | assert_specific_problem | CRITIQUE | Mentionne un problème spécifique (pas générique) |
| A7 | assert_call_to_action | HAUTE | Invite à un échange de 20-30 minutes |

## Mots interdits (A1)

```
tarif, prix, devis, offre, prestation, contrat, facturation,
robots.txt, schema.org, llms.txt, sitemap, SEO, GEO,
balise, meta tag, PageSpeed, Core Web Vitals, audit complet
```

## Critères de personnalisation (A6)

Le message est considéré "spécifique" si il contient au moins un de :
- Nom exact de l'entreprise dans l'accroche
- Référence à une plateforme réelle (Google Maps, TripAdvisor, ChatGPT)
- Un problème formulé avec le secteur d'activité (restaurant, hôtel, etc.)
- Mention d'une localisation géographique (île, ville)

## Historique des itérations

| # | Modification | Pass rate | Décision |
|---|-------------|-----------|----------|
| 0 | Baseline | —% | — |

## Notes

- Les 3 versions DOIVENT être dans le même fichier output
- Un message trop long = poubelle. La concision est une assertion critique.
- La personnalisation est la différence entre spam et prospection efficace
