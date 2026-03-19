"""
Autoresearch test suite — geo-outreach

Assertions:
  A1 assert_no_forbidden_words  — CRITIQUE
  A2 assert_three_versions      — HAUTE
  A3 assert_email_length        — HAUTE
  A4 assert_dm_length           — HAUTE
  A5 assert_whatsapp_length     — MOYENNE
  A6 assert_specific_problem    — CRITIQUE
  A7 assert_call_to_action      — HAUTE

Usage:
  python autoresearch/tests/check_outreach.py --batch autoresearch/examples/geo-outreach/ --json
"""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _base import Assertion, main, count_words

FORBIDDEN_WORDS = [
    r"\btarif\b", r"\bprix\b", r"\bdevis\b", r"\bco[uû]t\b",
    r"\beuro\b", r"€",
    r"\boffre\b", r"\bprestation\b", r"\bcontrat\b", r"\bfacturation\b",
    r"\brobots\.txt\b", r"\bschema\.org\b", r"\bllms\.txt\b", r"\bsitemap\b",
    r"\bSEO\b", r"\bGEO\b",
    r"\baudit complet\b",
    r"\bbalise\b", r"\bmeta tag\b", r"\bPageSpeed\b", r"\bCore Web Vitals\b",
]

# Specificity signals — at least one must be present
SPECIFIC_PATTERNS = [
    r"\b(Google Maps|TripAdvisor|ChatGPT|Perplexity|Google My Business|GMB)\b",
    r"\b(restaurant|hôtel|hotel|boutique|commerce|activité|excursion|pension)\b",
    r"\b(Tahiti|Moorea|Bora Bora|Papeete|Raiatea|Rangiroa|Polynésie|polynesie)\b",
    r"\b(Facebook|Instagram|TikTok)\b",
    r"(?i)\breservation\b|\bréservation\b|\bréserver\b",
]

CTA_PATTERNS = [
    r"\b(20 minutes|30 minutes|15 minutes)\b",
    r"\b(disponible|libre|joignable)\b.*\b(semaine|appel|call|échange)\b",
    r"\b(appel|échange|call)\b.*\b(disponible|semaine|cette)\b",
    r"\bsans engagement\b",
    r"\b(répondez|contactez|écrivez|appelez)\b",
]

VERSION_HEADERS = [
    r"(?i)version\s*[1①]\s*[-—]?\s*(email|e-mail|mail|courriel)",
    r"(?i)version\s*[2②]\s*[-—]?\s*(DM|message|facebook|instagram|réseau)",
    r"(?i)version\s*[3③]\s*[-—]?\s*(whatsapp|sms|court|ultra)",
    # Alternative: Email / DM / WhatsApp section headers
    r"(?i)##\s*.*email",
    r"(?i)##\s*.*DM",
    r"(?i)##\s*.*whatsapp",
]


def _extract_version_block(text: str, version_num: int) -> str:
    """Extract the text block for a given version number."""
    patterns = {
        1: [r"(?i)(version\s*1|##\s*.*email[^#]*)", r"(?i)(email.*fr|email\s*[\-—])", r"(?i)objet\s*:"],
        2: [r"(?i)(version\s*2|##\s*.*DM|##\s*.*facebook|##\s*.*instagram)"],
        3: [r"(?i)(version\s*3|##\s*.*whatsapp|##\s*.*sms|##\s*.*court)"],
    }
    for p in patterns.get(version_num, []):
        m = re.search(p, text)
        if m:
            start = m.start()
            # Find the next version header or end of doc
            next_h = re.search(r"\n##\s", text[start + 10:])
            end = start + 10 + next_h.start() if next_h else len(text)
            return text[start:end]
    return ""


def assert_no_forbidden_words(text: str) -> bool:
    for pattern in FORBIDDEN_WORDS:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True


def assert_three_versions(text: str) -> bool:
    """Check that the file contains at least 3 distinct message versions."""
    found = 0
    for pattern in VERSION_HEADERS:
        if re.search(pattern, text):
            found += 1
    return found >= 3


def assert_email_length(text: str) -> bool:
    block = _extract_version_block(text, 1)
    if not block:
        # Try to find any "Objet :" section which indicates an email
        m = re.search(r"(?i)objet\s*:", text)
        if not m:
            return True  # No email version found, skip
        # Take 300 words after the Objet line
        block = text[m.start():m.start() + 1500]
    words = count_words(block)
    return words <= 250  # Version header + body ≤ 200 words, plus some overhead


def assert_dm_length(text: str) -> bool:
    block = _extract_version_block(text, 2)
    if not block:
        return True  # No DM version found, skip
    # Remove the header line
    lines = [l for l in block.split("\n") if l.strip() and not l.startswith("#")]
    words = count_words(" ".join(lines))
    return words <= 130  # 100 words + overhead


def assert_whatsapp_length(text: str) -> bool:
    block = _extract_version_block(text, 3)
    if not block:
        return True  # No WhatsApp version found, skip
    lines = [l for l in block.split("\n") if l.strip() and not l.startswith("#")]
    words = count_words(" ".join(lines))
    return words <= 110  # 80 words + overhead


def assert_specific_problem(text: str) -> bool:
    """At least one specificity signal must be present."""
    for pattern in SPECIFIC_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def assert_call_to_action(text: str) -> bool:
    for pattern in CTA_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


ASSERTIONS = [
    Assertion("A1", "assert_no_forbidden_words", "CRITIQUE", assert_no_forbidden_words),
    Assertion("A2", "assert_three_versions", "HAUTE", assert_three_versions),
    Assertion("A3", "assert_email_length", "HAUTE", assert_email_length),
    Assertion("A4", "assert_dm_length", "HAUTE", assert_dm_length),
    Assertion("A5", "assert_whatsapp_length", "MOYENNE", assert_whatsapp_length),
    Assertion("A6", "assert_specific_problem", "CRITIQUE", assert_specific_problem),
    Assertion("A7", "assert_call_to_action", "HAUTE", assert_call_to_action),
]

if __name__ == "__main__":
    main(ASSERTIONS, "geo-outreach")
