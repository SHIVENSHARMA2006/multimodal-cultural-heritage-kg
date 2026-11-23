"""
Text Cleaning, Normalization and Script Analysis for Manipuri Heritage Corpora.
Handles Unicode normalization, Meetei Mayek vs Latin script detection,
and historical alias/spelling resolution.
"""
import re
import unicodedata
from typing import Dict, List, Tuple, Optional

# Meetei Mayek Unicode Blocks:
# U+ABC0 to U+ABFF (Meetei Mayek)
# U+AAE0 to U+AAFF (Meetei Mayek Extensions)
MEETEI_MAYEK_PATTERN = re.compile(r'[\uABC0-\uABFF\uAAE0-\uAAFF]')

# Known historical alias & transliteration maps for Meitei Heritage entities
KNOWN_ALIAS_CLUSTERS = {
    "pamheiba": ["pamheiba", "garib niwaz", "gharib nawaz", "gareeb nawaz"],
    "bhagyachandra": ["bhagyachandra", "rajarshi bhagyachandra", "ching-thang khomba", "chingthang khomba", "jai singh"],
    "kangla": ["kangla", "kangla fort", "kangla palace", "imphal kangla"],
    "sanggai yumpham": ["sanggai yumpham", "sangkai eempham", "kangla citadel", "citadel of kangla"],
    "tikendrajit": ["tikendrajit", "bir tikendrajit", "jubraj tikendrajit", "tikendrajit singh"],
    "cheitharol kumbaba": ["cheitharol kumbaba", "cheitharon kumbaba", "royal chronicle", "manipur court chronicle"],
    "mapal kangjeibung": ["mapal kangjeibung", "imphal polo ground", "outer polo ground"],
    "manung kangjeibung": ["manung kangjeibung", "inner polo ground", "manung kangjei bung"],
    "kangla sha": ["kangla sha", "kanglasha", "dragon lion of kangla"],
    "puya meithaba": ["puya meithaba", "puya mei thaba", "burning of the puyas", "puya burning"]
}

class TextNormalizer:
    @staticmethod
    def normalize_text(text: str) -> str:
        if not text:
            return ""
        # Standardize Unicode (NFKC)
        normalized = unicodedata.normalize("NFKC", text)
        # Collapse whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized

    @staticmethod
    def detect_script(text: str) -> str:
        """
        Detects whether text contains Meetei Mayek script, Latin transliteration, or Bengali-Assamese script.
        """
        if not text:
            return "unknown"
        if MEETEI_MAYEK_PATTERN.search(text):
            return "meetei_mayek"
        # Check for Bengali script (used historically for Manipuri in 19th-20th centuries)
        if re.search(r'[\u0980-\u09FF]', text):
            return "bengali_script"
        if re.search(r'[A-Za-z]', text):
            return "latin"
        return "other"

    @staticmethod
    def resolve_alias_cluster(surface_form: str) -> str:
        """
        Maps spelling variations and royal titles to canonical heritage entity name.
        """
        cleaned = surface_form.lower().strip()
        for canonical, aliases in KNOWN_ALIAS_CLUSTERS.items():
            if cleaned in aliases or any(alias in cleaned for alias in aliases):
                return canonical
        return cleaned

    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """
        Extracts year candidates, century references, and date expressions.
        """
        date_patterns = [
            r'\b\d{1,4}\s*(?:CE|AD|BC|BCE)?\b',
            r'\b\d{1,2}(?:st|nd|rd|th)\s+century\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,\s*\d{4})?\b'
        ]
        results = []
        for p in date_patterns:
            matches = re.findall(p, text, re.IGNORECASE)
            results.extend(matches)
        return list(set(results))
