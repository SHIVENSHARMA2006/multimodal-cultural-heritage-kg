"""
Cross-Lingual Query Translation and Intent Alignment Module.
Translates and normalizes user queries submitted in Meetei Mayek script,
Latin transliteration, or English into aligned KG search concepts.
"""
import re
from typing import Dict, Any, List, Optional
from ingestion.text_normalize import TextNormalizer, MEETEI_MAYEK_PATTERN
from kg.graph_engine import HeritageGraphEngine

SCRIPT_CONCEPT_MAP = {
    "ꯀꯪꯂꯥ": "Kangla Fort",
    "ꯁꯡꯒꯥꯏ ꯌꯨꯝꯐꯝ": "Sanggai Yumpham",
    "ꯀꯪꯂꯥꯁꯥ": "Kangla Sha",
    "ꯃꯅꯨꯡ ꯀꯥꯡꯖꯩꯕꯨꯡ": "Manung Kangjeibung",
    "ꯃꯄꯥꯜ ꯀꯥꯡꯖꯩꯕꯨꯡ": "Mapal Kangjeibung",
    "ꯁꯒꯣꯜ ꯀꯥꯡꯖꯩ": "Sagol Kangjei",
    "ꯃꯤꯇꯩ ꯃꯌꯦꯛ": "Meitei Mayek",
    "ꯃꯤꯇꯩ ꯄꯨꯌꯥ": "Puya",
    "ꯄꯨꯌꯥ ꯃꯩ ꯊꯥꯕꯥ": "Puya Meithaba",
    "ꯆꯩꯊꯥꯔꯣꯜ ꯀꯨꯝꯕꯥꯕꯥ": "Cheitharol Kumbaba",
    "ꯂꯥꯏ ꯍꯔꯥꯎꯕꯥ": "Lai Haraoba",
    "ꯁꯪꯀꯤꯔꯇꯟ": "Sankirtana of Manipur",
    "ꯏꯃꯥ ꯀꯩꯊꯦꯜ": "Ima Keithel",
    "ꯇꯤꯀꯦꯟꯗ꯭ꯔꯖꯤꯠ": "Tikendrajit Singh"
}

KEYWORD_ENTITY_MAP = {
    "sankirtana": "E012",
    "sanggai yumpham": "E002",
    "manung kangjeibung": "E003",
    "mapal kangjeibung": "E004",
    "oldest polo ground": "E004",
    "marjing": "E006",
    "horses and polo": "E006",
    "deity": "E006",
    "sagol kangjei": "E005",
    "puya meithaba": "E009",
    "puyas burned": "E009",
    "burning of the puya": "E009",
    "cheitharol kumbaba": "E010",
    "royal chronicle": "E010",
    "pamheiba": "E011",
    "gareeb nawaz": "E011",
    "garib niwaz": "E011",
    "gharib nawaz": "E011",
    "lai haraoba": "E013",
    "classical dance": "E014",
    "raas leela": "E014",
    "raas dance": "E014",
    "govindajee": "E015",
    "ching-thang khomba": "E016",
    "bhagyachandra": "E016",
    "kiyamba": "E017",
    "british take possession": "E018",
    "possession of kangla": "E018",
    "anglo-manipur war": "E018",
    "1891": "E018",
    "tikendrajit": "E019",
    "khongjom": "E020",
    "ima keithel": "E021",
    "nupi lan": "E022",
    "state archives": "E023",
    "mission for manuscripts": "E024",
    "digitizemanipur": "E025",
    "archives or projects": "E026",
    "manuscripts exist": "E026",
    "manuscripts in manipur": "E026",
    "parratt papers": "E027",
    "speech resources": "E028",
    "indicvoices-r": "E028",
    "indicvoices": "E029",
    "speech-translation": "E030",
    "mann ki baat": "E030",
    "vaani": "E031",
    "kangla sha": "E033",
    "meitei mayek": "E007",
    "meetei mayek": "E007",
    "kangla": "E001"
}

class QueryTranslator:
    def __init__(self, engine: HeritageGraphEngine):
        self.engine = engine

    def process_query(self, query: str) -> Dict[str, Any]:
        raw_query = query.strip()
        if not raw_query:
            return {
                "original_query": "",
                "detected_script": "unknown",
                "translated_concept": None,
                "matched_entities": [],
                "primary_entity": None,
                "detected_relation": None
            }
        script = TextNormalizer.detect_script(raw_query)
        detected_entities = []
        translated_concept = None

        # 1. Meetei Mayek script check
        if script == "meetei_mayek":
            for mayek_term, canonical in SCRIPT_CONCEPT_MAP.items():
                if mayek_term in raw_query:
                    ent = self.engine.find_entity(canonical)
                    if ent and ent not in detected_entities:
                        detected_entities.append(ent)
                        translated_concept = canonical

        # 2. Domain Keyword Matching (priority order)
        q_lower = raw_query.lower()
        for kw, eid in KEYWORD_ENTITY_MAP.items():
            if kw in q_lower:
                ent = self.engine.entities.get(eid)
                if ent and ent not in detected_entities:
                    detected_entities.append(ent)
                    break

        # 3. Canonical name & alias search
        if not detected_entities:
            for eid, ent in self.engine.entities.items():
                if ent in detected_entities:
                    continue
                if ent.canonical_name.lower() in q_lower:
                    detected_entities.append(ent)
                    break
                for alias in ent.aliases:
                    if alias.lower() in q_lower:
                        detected_entities.append(ent)
                        break
                if detected_entities:
                    break

        # 4. Fuzzy fallback
        if not detected_entities:
            fuzzy = self.engine.search_entities(raw_query, limit=2)
            if fuzzy:
                detected_entities = fuzzy

        # 5. Fine-grained Relation Detection
        detected_relation = None
        if "unesco" in q_lower or "inscribed" in q_lower or "representative list" in q_lower:
            detected_relation = "unesco_inscription"
        elif "mean" in q_lower or "meaning" in q_lower or "etymology" in q_lower:
            detected_relation = "etymology"
        elif "manage" in q_lower:
            detected_relation = "managed_by"
        elif "possession" in q_lower or "capture" in q_lower:
            detected_relation = "event"
        elif "taught" in q_lower or "curriculum" in q_lower or "students" in q_lower:
            detected_relation = "revival"
        elif "script" in q_lower:
            if "speech-translation" in q_lower or "mann ki baat" in q_lower:
                detected_relation = "script"
            elif "letter" in q_lower:
                detected_relation = "letter_count"
            elif "age" in q_lower or "how old" in q_lower:
                detected_relation = "age"
            else:
                detected_relation = "script"
        elif "hanged" in q_lower or "execution" in q_lower:
            if "how many" in q_lower:
                detected_relation = "executions"
            else:
                detected_relation = "execution_date"
        elif "khongjom day" in q_lower:
            detected_relation = "khongjom_day"
        elif "credited" in q_lower or "raas leela form" in q_lower:
            detected_relation = "attributed_to"
        elif "recognise" in q_lower or "classical dance" in q_lower:
            detected_relation = "classification"
        elif "established" in q_lower or "founded" in q_lower or "foundation" in q_lower:
            if "archives" in q_lower:
                detected_relation = "establishment"
            elif "kangla" in q_lower:
                detected_relation = "founding_date"
            elif "ima keithel" in q_lower:
                detected_relation = "founding"
            else:
                detected_relation = "founding_date"
        elif "launched" in q_lower or "ministry" in q_lower:
            detected_relation = "sponsoring_agency"
        elif "five categories" in q_lower or "categories of raas" in q_lower:
            detected_relation = "categories"
        elif "deity" in q_lower or "horse" in q_lower:
            detected_relation = "cultural_significance"
        elif "convert" in q_lower or "vaishnavism" in q_lower:
            detected_relation = "conversion"
        elif "reign" in q_lower or "reigned" in q_lower:
            if "end" in q_lower:
                detected_relation = "reign_end"
            else:
                detected_relation = "reign"
        elif "museums" in q_lower:
            detected_relation = "contains"
        elif "burned" in q_lower or "burning" in q_lower:
            detected_relation = "date"
        elif "oldest" in q_lower and "polo" in q_lower:
            detected_relation = "oldest_polo_ground"
        elif "introduced" in q_lower and "sagol" in q_lower:
            detected_relation = "origin"
        elif "vendor" in q_lower:
            detected_relation = "vendor_count"
        elif "held" in q_lower or "timing" in q_lower:
            detected_relation = "timing"
        elif "status" in q_lower and "1891" in q_lower:
            detected_relation = "political_outcome"
        elif "run" in q_lower or "coverage" in q_lower or "until what year" in q_lower:
            detected_relation = "coverage_end"
        elif "how many manuscripts" in q_lower:
            detected_relation = "manuscript_count"
        elif "hours of speech" in q_lower or "hours" in q_lower:
            detected_relation = "corpus_size"
        elif "archives or projects hold" in q_lower or "manuscripts relevant" in q_lower:
            detected_relation = "preservation_location"
        elif "video" in q_lower or "duration" in q_lower or "how long" in q_lower:
            detected_relation = "video_duration"

        return {
            "original_query": raw_query,
            "detected_script": script,
            "translated_concept": translated_concept,
            "matched_entities": detected_entities,
            "primary_entity": detected_entities[0] if detected_entities else None,
            "detected_relation": detected_relation
        }
