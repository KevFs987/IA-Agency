"""
Autoresearch test suite — geo-social

Assertions:
  A1 assert_score_present         — CRITIQUE
  A2 assert_platform_detected     — HAUTE
  A3 assert_three_gaps            — HAUTE
  A4 assert_hors_social_checked   — HAUTE
  A5 assert_no_tarif              — CRITIQUE
  A6 assert_cta_present           — HAUTE
  A7 assert_graceful_degradation  — MOYENNE (only when data is partial)

Usage:
  python autoresearch/tests/check_social.py --batch autoresearch/examples/geo-social/ --json
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
    r"\boffre\b.*\b\d+\b",
    r"\bfacturation\b",
]

PLATFORMS = [
    r"\bFacebook\b",
    r"\bInstagram\b",
    r"\bTikTok\b",
]

HORS_SOCIAL_SIGNALS = [
    r"\bGoogle\s*My\s*Business\b|\bGMB\b",
    r"\bGoogle\s*Maps?\b",
    r"\bTripAdvisor\b",
    r"\bPages?\s*Jaunes?\b",
]

GAP_PATTERNS = [
    r"\bGap\s+[123]\b",
    r"\bGap\s+[#]?\s*[123]\b",
    r"^#+\s*Gap\b",
    r"Lacune\s+[123]",
    r"Point\s+manquant\s+[123]",
    # Also accept numbered sections that read as gaps
    r"^\s*###?\s+\d+[\.\s]",
]

CTA_PATTERNS = [
    r"\b(appel|échange|call|discussion|30 minutes|20 minutes)\b",
    r"\b(disponible|joignable|libre)\b.*\b(appel|semaine|échange)\b",
    r"\bsans engagement\b",
    r"\b(répondez|contactez|écrivez|appelez)\b",
    r"\bProchaine [EeÉé]tape\b",
    r"\bNext [Ss]tep\b",
]

DEGRADATION_SIGNALS = [
    r"donn[ée]es? partiellement\s+accessibles?",
    r"acc[eè]s\s+limit[eé]",
    r"analyse\s+bas[eé]e?\s+sur\s+les?\s+m[eé]tadonn[eé]es?",
    r"login\s+wall",
    r"page\s+inaccessible",
    r"informations?\s+limit[eé]es?",
]


def assert_score_present(text: str) -> bool:
    return bool(re.search(r"\b\d{1,3}/100\b", text))


def assert_platform_detected(text: str) -> bool:
    for p in PLATFORMS:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False


def assert_three_gaps(text: str) -> bool:
    """At least 3 gaps/priority issues must be identified."""
    # Check for "Gap 1/2/3" style
    for pattern in GAP_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        if len(matches) >= 3:
            return True

    # Check for "Les 3 Gaps Prioritaires" section with subsections
    if re.search(r"(?i)(3\s+gaps?\s+prioritaires|3\s+lacunes|trois\s+gaps?)", text):
        # Count subsections under it
        gaps_section = re.search(r"(?i)(gaps?\s+prioritaires?|lacunes?\s+prioritaires?)", text)
        if gaps_section:
            after = text[gaps_section.start():]
            subsections = re.findall(r"^###?\s+", after, re.MULTILINE)
            if len(subsections) >= 3:
                return True

    # Count sections starting with "### Gap" or "### Problème"
    sections = re.findall(
        r"^###?\s+(?:Gap|Lacune|Probl[eè]me|Point|Manque)\b",
        text, re.MULTILINE | re.IGNORECASE
    )
    return len(sections) >= 3


def assert_hors_social_checked(text: str) -> bool:
    """Must mention at least Google My Business or Google Maps."""
    for signal in HORS_SOCIAL_SIGNALS[:2]:  # GMB or Google Maps required
        if re.search(signal, text, re.IGNORECASE):
            return True
    return False


def assert_no_tarif(text: str) -> bool:
    for pattern in TARIF_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True


def assert_cta_present(text: str) -> bool:
    for pattern in CTA_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def assert_graceful_degradation(text: str) -> bool:
    """
    If the report mentions access issues, it must also mention graceful degradation.
    If there are no access issues mentioned, this assertion passes by default.
    """
    has_access_issue = bool(re.search(
        r"(?i)(inaccessible|bloqué|login|wall|403|404|impossible\s+d.accéder|données?\s+indisponibles?)",
        text
    ))
    if not has_access_issue:
        return True  # No issue to degrade from — pass

    for signal in DEGRADATION_SIGNALS:
        if re.search(signal, text, re.IGNORECASE):
            return True
    return False


ASSERTIONS = [
    Assertion("A1", "assert_score_present", "CRITIQUE", assert_score_present),
    Assertion("A2", "assert_platform_detected", "HAUTE", assert_platform_detected),
    Assertion("A3", "assert_three_gaps", "HAUTE", assert_three_gaps),
    Assertion("A4", "assert_hors_social_checked", "HAUTE", assert_hors_social_checked),
    Assertion("A5", "assert_no_tarif", "CRITIQUE", assert_no_tarif),
    Assertion("A6", "assert_cta_present", "HAUTE", assert_cta_present),
    Assertion("A7", "assert_graceful_degradation", "MOYENNE", assert_graceful_degradation),
]

if __name__ == "__main__":
    main(ASSERTIONS, "geo-social")
