"""
Autoresearch test suite — geo-proposal

Assertions:
  A1 assert_client_name      — CRITIQUE
  A2 assert_options_present  — HAUTE
  A3 assert_next_step        — HAUTE
  A4 assert_no_jargon        — MOYENNE
  A5 assert_problem_recap    — HAUTE
  A6 assert_timeline         — MOYENNE
  A7 assert_length_ok        — BASSE

Usage:
  python autoresearch/tests/check_proposal.py --batch autoresearch/examples/geo-proposal/ --json
"""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _base import Assertion, main, count_words

JARGON_PATTERNS = [
    r"\brobots\.txt\b",
    r"\bschema\.org\b",
    r"\bllms\.txt\b",
    r"\bCore Web Vitals\b",
    r"\bSearch Console\b",
    r"\bPageSpeed\b",
    r"\bcanonical\b",
    r"\bhreflang\b",
    r"\bJSON-LD\b",
    r"\bOpen Graph\b",
]

# Signals that the proposal recaps client-specific problems
PROBLEM_RECAP_SIGNALS = [
    r"\b(vous avez|votre|vos)\b.*\b(problème|gap|lacune|absent|manquant|invisible)\b",
    r"\b(nous avons constaté|nous avons identifié|lors de notre analyse|lors de l.audit)\b",
    r"\b(votre situation|votre cas|votre contexte)\b",
    r"\b(comme vu|tel que constaté|d.après notre analyse)\b",
    r"\b(vous n.apparaissez pas|vous êtes absent|vous n.êtes pas visible)\b",
]

NEXT_STEP_PATTERNS = [
    r"\b(prochaine [eé]tape|next step)\b",
    r"\b(pour d[eé]marrer|pour commencer|pour lancer)\b",
    r"\b(signez?|validez?|r[eé]pondez?|confirmez?)\b.*\b(proposition|accord|devis)\b",
    r"\b(votre r[eé]ponse|votre accord|votre validation)\b",
    r"\b(appel de d[eé]marrage|kick.?off|réunion de lancement)\b",
    r"\b(nous pouvons commencer|nous démarrons)\b",
]

TIMELINE_PATTERNS = [
    r"\b\d+\s*(?:jour|semaine|mois|week|day)\b",
    r"\b(?:jour|semaine|mois)\s+\d+\b",
    r"\bJ\+\d+\b",
    r"\bdélai\b",
    r"\blivraison\b.*\b\d+\b",
    r"\b\d+\s*à\s*\d+\s*(?:jours?|semaines?|mois)\b",
]

OPTION_PATTERNS = [
    # Pricing tiers, packages, formulas
    r"\b(Formule|Offre|Pack|Option|Forfait)\s+[A-Z\d]",
    r"###?\s+(?:Formule|Offre|Option|Pack|Niveau|Tier)",
    r"\b(Essentiel|Starter|Pro|Premium|Business|Standard|Complet)\b.*\b\d+\b",
    # At least 2 price mentions
    r"\d+\s*[€$]",
    # Options labeled 1 and 2
    r"\bOption\s*[12]\b",
    r"\bFormule\s*[12]\b",
]


def _count_price_mentions(text: str) -> int:
    return len(re.findall(r"\d[\s.,]?\d*\s*[€$]|[€$]\s*\d[\s.,]?\d*", text))


def assert_client_name(text: str) -> bool:
    """The proposal must be addressed to a specific client (not generic)."""
    # Look for "Proposition pour [Name]" or "Préparé pour [Name]" in the header
    patterns = [
        r"(?i)(proposition|proposal|devis|offre)\s+(pour|for|à|to)\s+\S+",
        r"(?i)(prépar[eé]\s+pour|prepared\s+for|destiné\s+à)\s+\S+",
        r"(?i)^#\s+.*(?:Proposition|Devis|Offre).*\b\w{3,}\b",
        r"(?i)client\s*:\s*\S+",
        r"(?i)entreprise\s*:\s*\S+",
    ]
    for p in patterns:
        if re.search(p, text, re.MULTILINE):
            return True
    # Last resort: the document title mentions a proper noun (capitalized word in h1)
    h1 = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if h1 and len(h1.group(1).split()) >= 2:
        return True
    return False


def assert_options_present(text: str) -> bool:
    """Must contain at least 2 pricing options."""
    # Check for option headers
    option_headers = 0
    for pattern in OPTION_PATTERNS[:-2]:  # Exclude the raw count patterns
        if re.search(pattern, text, re.IGNORECASE):
            option_headers += 1

    if option_headers >= 2:
        return True

    # Check for at least 2 price mentions
    price_count = _count_price_mentions(text)
    return price_count >= 2


def assert_next_step(text: str) -> bool:
    for pattern in NEXT_STEP_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def assert_no_jargon(text: str) -> bool:
    # Remove code blocks
    clean = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    clean = re.sub(r"`[^`]+`", "", clean)
    for pattern in JARGON_PATTERNS:
        if re.search(pattern, clean, re.IGNORECASE):
            return False
    return True


def assert_problem_recap(text: str) -> bool:
    for pattern in PROBLEM_RECAP_SIGNALS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def assert_timeline(text: str) -> bool:
    for pattern in TIMELINE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def assert_length_ok(text: str) -> bool:
    clean = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
    return count_words(clean) <= 1500


ASSERTIONS = [
    Assertion("A1", "assert_client_name", "CRITIQUE", assert_client_name),
    Assertion("A2", "assert_options_present", "HAUTE", assert_options_present),
    Assertion("A3", "assert_next_step", "HAUTE", assert_next_step),
    Assertion("A4", "assert_no_jargon", "MOYENNE", assert_no_jargon),
    Assertion("A5", "assert_problem_recap", "HAUTE", assert_problem_recap),
    Assertion("A6", "assert_timeline", "MOYENNE", assert_timeline),
    Assertion("A7", "assert_length_ok", "BASSE", assert_length_ok),
]

if __name__ == "__main__":
    main(ASSERTIONS, "geo-proposal")
