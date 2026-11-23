"""
CIDOC-CRM Aligned Prompt Templates for Open-World Entity and Relation Extraction.
Follows the WJoconde extraction-then-validation pattern (Definition -> Role -> Input -> Output Schema).
"""

EXTRACTION_SYSTEM_PROMPT = """You are an expert Cultural Heritage Knowledge Graph extractor specialized in low-resource and indigenous heritage domains (specifically Manipuri / Meitei cultural heritage).
Your task is to extract factual and interpretive claims from historical texts, archival surveys, gazetteers, and oral testimony into structured CIDOC-CRM aligned JSON triples.

CRITICAL INSTRUCTIONS:
1. Preserve conflicting or diverging claims faithfully. Never silently choose one version or overwrite competing accounts.
2. Every extracted triple MUST include:
   - subject (canonical entity name)
   - relation (CIDOC-CRM target property, e.g. depicts, made_from_material, has_type, located_in, built_by, founding_date)
   - object (normalized value)
   - evidence_excerpt (exact literal snippet supporting the claim)
   - extraction_confidence (float 0.0 to 1.0)
   - source_type (archival_text, manuscript, oral_testimony, monument_image)
3. Return output strictly as valid JSON matching the requested schema.
"""

EXTRACTION_USER_TEMPLATE = """Source Text:
\"\"\"{source_text}\"\"\"

Source Metadata:
- Source Title: {source_title}
- Source Reliability Tier: {source_tier}
- Language: {language}

Extract all candidate cultural heritage triples. Output valid JSON in the format:
{{
  "entities": [
    {{
      "name": "Entity Name",
      "aliases": ["Alias 1", "Alias 2"],
      "meitei_script": "Meetei Mayek glyphs if present, else null",
      "type": "Monument | Person | Event | Script | Practice"
    }}
  ],
  "triples": [
    {{
      "subject": "Entity Name",
      "relation": "relation_name",
      "object": "Value or Entity",
      "evidence_excerpt": "verbatim text snippet",
      "confidence": 0.95
    }}
  ]
}}
"""

CROSS_MODAL_VALIDATION_PROMPT = """You are a Cross-Modal Heritage Validator.
Given a textual claim extracted from archival or manuscript text and visual/audio evidence from a second modality,
determine whether the second modality SUPPORTS, CONTRADICTS, or is SILENT regarding the claim.

Textual Claim:
Subject: {subject}
Relation: {relation}
Object: {object}
Claim Text: {claim_text}

Multimodal Evidence:
Modality: {modality}
Description / Transcription: {evidence_description}

Output JSON:
{{
  "validation_status": "SUPPORTED | CONTRADICTED | NEUTRAL_SILENT",
  "confidence": 0.90,
  "rationale": "Detailed archaeological / historical rationale"
}}
"""
