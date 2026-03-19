"""
Autoresearch test suite — geo-teaser-report

Assertions:
  A1 assert_no_forbidden_words  — CRITIQUE
  A2 assert_score_present       — HAUTE
  A3 assert_three_problems      — HAUTE
  A4 assert_cta_present         — HAUTE
  A5 assert_length_ok           — MOYENNE
  A6 assert_no_solutions        — CRITIQUE
  A7 assert_positive_present    — BASSE

Usage:
  python autoresearch/tests/check_teaser.py --batch autoresearch/examples/geo-teaser-report/ --json
"""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _base import Assertion, main, count_words

FORBIDDEN_WORDS = [
    r"\btarif\b", r"\bprix\b", r"\bdevis\b", r"\bco[uû]t\b",
    r"\beuro\b", r"€",
    r"\boffre\b", r"\bprestation\b",
    r"\bplan d.action\b",
    r"\brecommandations?\b",
    r"\brobots\.txt\b", r"\bschema\.org\b", r"\bllms\.txt\b", r"\bsitemap\b",
    r"\bSEO\b", r"\bGEO\b",
    r"\bbalise\b", r"\bmeta tag\b",
    r"\bSearch Console\b", r"\bPageSpeed\b", r"\bCore Web Vitals\b",
]

SOLUTION_PATTERNS = [
    r"^\s*[-*]\s+.{10,}",  # bullet point lists (recommendations)
    r"^\s*\d+\.\s+.{10,}",  # numbered action lists
    r"\b(vous devez|vous devriez|il faut|je vous conseille)\b",
    r"\b(étape \d|step \d)\b",
    r"\b(pour remédier|pour corriger|pour améliorer)\b",
    r"\b(mise en place|implementer|déployer|configurer)\b",
]

CTA_PATTERNS = [
    r"\b(disponible|joignable)\b.*\b(appel|échange|conversation|discussion|call)\b",
    r"\b(appel|échange|call)\b.*\b(disponible|libre|minutes)\b",
    r"\b(réservez|répondez|contactez|écrivez)\b",
    r"\b(calendrier|agenda|rdv|rendez-vous)\b",
    r"\b(30 minutes|20 minutes|15 minutes)\b",
    r"\bsans engagement\b",
]

POSITIVE_PATTERNS = [
    r"\b(bonne|bien|excellent|super|solide|actif|présent|visible)\b",
    r"✓|✅",
    r"\bce qui fonctionne\b",
    r"\bpoints? positifs?\b",
    r"\bforcé\b|\batout\b|\bforces?\b",
]


def assert_no_forbidden_words(text: str) -> bool:
    text_lower = text.lower()
    for pattern in FORBIDDEN_WORDS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return False
    return True


def assert_score_present(text: str) -> bool:
    # Looking for patterns like "34/100" or "Score : 34/100" or "XX/100"
    return bool(re.search(r"\b\d{1,3}/100\b", text))


def assert_three_problems(text: str) -> bool:
    # Look for 3 numbered problems or "Problème #1", "Problème #2", "Problème #3"
    count_hash = len(re.findall(r"Probl[eè]me\s*#?\s*[123]", text, re.IGNORECASE))
    if count_hash >= 3:
        return True
    # Also accept bold numbered patterns: **1.**, **Problème 1**
    count_bold = len(re.findall(r"\*\*\s*(?:Probl[eè]me\s*)?[123][.\s]", text))
    if count_bold >= 3:
        return True
    # Accept ⚠ or — separators with at least 3 sections named as problems
    count_sections = len(re.findall(
        r"(?:^|\n)#+\s*(?:⚠|Probl[eè]me|Problématique|Point critique|Issue)",
        text, re.IGNORECASE
    ))
    return count_sections >= 3


def assert_cta_present(text: str) -> bool:
    for pattern in CTA_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def assert_length_ok(text: str) -> bool:
    # Remove YAML frontmatter if present
    clean = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
    return count_words(clean) <= 800


def assert_no_solutions(text: str) -> bool:
    # Check for solution-giving patterns — but only in "problème" sections
    # Allow action bullet points ONLY in the final CTA section
    # Split at the CTA section marker
    parts = re.split(r"(?i)(la suite|prochaine[s]? [eé]tape|CTA|contact)", text, maxsplit=1)
    body = parts[0] if parts else text

    for pattern in SOLUTION_PATTERNS:
        if re.search(pattern, body, re.IGNORECASE | re.MULTILINE):
            # Exception: single-line bullets with very short content are ok (like "✓ point positif")
            matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
            # If there are more than 2 matches, likely a recommendation list
            if len(matches) > 2:
                return False
    return True


def assert_positive_present(text: str) -> bool:
    for pattern in POSITIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


ASSERTIONS = [
    Assertion("A1", "assert_no_forbidden_words", "CRITIQUE", assert_no_forbidden_words),
    Assertion("A2", "assert_score_present", "HAUTE", assert_score_present),
    Assertion("A3", "assert_three_problems", "HAUTE", assert_three_problems),
    Assertion("A4", "assert_cta_present", "HAUTE", assert_cta_present),
    Assertion("A5", "assert_length_ok", "MOYENNE", assert_length_ok),
    Assertion("A6", "assert_no_solutions", "CRITIQUE", assert_no_solutions),
    Assertion("A7", "assert_positive_present", "BASSE", assert_positive_present),
]

if __name__ == "__main__":
    main(ASSERTIONS, "geo-teaser-report")
