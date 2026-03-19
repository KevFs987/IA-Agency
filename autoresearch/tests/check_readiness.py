"""
Autoresearch test suite — geo-readiness

Assertions:
  A1 assert_level_present      — CRITIQUE
  A2 assert_detection_table    — HAUTE
  A3 assert_action_plan        — HAUTE
  A4 assert_no_tarif           — CRITIQUE
  A5 assert_cta_present        — HAUTE
  A6 assert_no_jargon          — MOYENNE
  A7 assert_positive_tone      — BASSE

Usage:
  python autoresearch/tests/check_readiness.py --batch autoresearch/examples/geo-readiness/ --json
"""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _base import Assertion, main

TARIF_PATTERNS = [
    r"\btarif\b", r"\bprix\b", r"\bdevis\b",
    r"\b\d+\s*[€$]\b", r"[€$]\s*\d+",
    r"\bco[uû]t\b.*\b\d+\b",
    r"\bfacturation\b",
]

# Jargon that should NOT appear in client-facing sections
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

NEGATIVE_PHRASES = [
    r"vous n.avez pas compris",
    r"erreur grave",
    r"catastrophique",
    r"incompétence",
    r"très mauvais",
    r"\bhonte\b",
    r"scandaleux",
    r"vous avez tout faux",
    r"désastreux",
]

CTA_PATTERNS = [
    r"\b(appel|échange|call|discussion|conversation)\b.*\b(minutes|disponible|libre)\b",
    r"\b(disponible|joignable)\b.*\b(appel|échange|30|20)\b",
    r"\bsans engagement\b",
    r"\b(réservez|répondez|contactez|écrivez)\b",
    r"\b(calendrier|agenda|rdv|rendez-vous)\b",
    r"\bprochaine [eé]tape\b",
]

ACTION_PATTERNS = [
    r"^\s*\d+\.\s+\*?\*?.{10,}",  # numbered actions
    r"^\s*[-*]\s+.{10,}",          # bullet actions
    r"\b(créer|ouvrir|configurer|installer|ajouter|optimiser|compléter|vérifier)\b",
    r"\bAction\b|\bÉtape\b|\bTo do\b",
]


def assert_level_present(text: str) -> bool:
    """Must contain a level 0-4 designation."""
    # Look for "Niveau X" or "Level X" or "Niveau X/4"
    patterns = [
        r"\bNiveau\s+[0-4]\b",
        r"\bNiveau\s+[0-4]\s*/\s*4\b",
        r"\bLevel\s+[0-4]\b",
        r"\b[Nn]iveau\s+actuel\s*:\s*[0-4]\b",
        r"Niveau\s+[0-4]\s*[—\-]\s*\w",  # "Niveau 1 — Social Only"
    ]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False


def assert_detection_table(text: str) -> bool:
    """Must contain a table listing presence signals."""
    # Look for markdown table with presence indicators
    has_table = bool(re.search(r"\|.*\|.*\|", text))
    if not has_table:
        return False
    # Table must mention at least some presence channels
    channels = [
        r"Google\s*My\s*Business|GMB",
        r"Facebook|Instagram|TikTok",
        r"site\s*web|Site\s*Web",
        r"TripAdvisor",
    ]
    mentions = sum(1 for c in channels if re.search(c, text, re.IGNORECASE))
    return mentions >= 2


def assert_action_plan(text: str) -> bool:
    """Must contain concrete action items."""
    for pattern in ACTION_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        if len(matches) >= 2:
            return True
    return False


def assert_no_tarif(text: str) -> bool:
    """Must not mention prices. Exception: the cost table is allowed in full readiness report."""
    # Check for actual price numbers with currency
    for pattern in TARIF_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True


def assert_cta_present(text: str) -> bool:
    for pattern in CTA_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def assert_no_jargon(text: str) -> bool:
    """Technical jargon should not appear in client-facing sections."""
    # We allow jargon in internal tables/code blocks — check only prose sections
    # Remove code blocks first
    clean = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    clean = re.sub(r"`[^`]+`", "", clean)
    # Remove table rows (allow jargon in table cells for checklist)
    clean = re.sub(r"^\|.*\|$", "", clean, flags=re.MULTILINE)

    for pattern in JARGON_PATTERNS:
        if re.search(pattern, clean, re.IGNORECASE):
            return False
    return True


def assert_positive_tone(text: str) -> bool:
    """Must not contain condescending or extremely negative phrases."""
    for pattern in NEGATIVE_PHRASES:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True


ASSERTIONS = [
    Assertion("A1", "assert_level_present", "CRITIQUE", assert_level_present),
    Assertion("A2", "assert_detection_table", "HAUTE", assert_detection_table),
    Assertion("A3", "assert_action_plan", "HAUTE", assert_action_plan),
    Assertion("A4", "assert_no_tarif", "CRITIQUE", assert_no_tarif),
    Assertion("A5", "assert_cta_present", "HAUTE", assert_cta_present),
    Assertion("A6", "assert_no_jargon", "MOYENNE", assert_no_jargon),
    Assertion("A7", "assert_positive_tone", "BASSE", assert_positive_tone),
]

if __name__ == "__main__":
    main(ASSERTIONS, "geo-readiness")
