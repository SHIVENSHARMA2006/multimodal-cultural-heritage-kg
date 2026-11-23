"""
CIDOC-CRM (ISO 21127) Aligned Schema for Multimodal Cultural Heritage Knowledge Graph.
Defines entity classes, property types, provenance records, and access tiers.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
import datetime

class CIDOCClass(str, Enum):
    E22_HUMAN_MADE_OBJECT = "E22_Human_Made_Object"  # Monuments, manuscripts, artifacts
    E53_PLACE = "E53_Place"                          # Geographical places, sites
    E39_ACTOR = "E39_Actor"                          # Historical figures, deities, clans, groups
    E5_EVENT = "E5_Event"                            # Wars, rituals, ceremonies, burnings
    E73_INFORMATION_OBJECT = "E73_Information_Object"# Texts, manuscripts, oral narratives
    E13_ATTRIBUTE_ASSIGNMENT = "E13_Attribute_Assignment" # Claim assignment event (dual-provenance)

class EvidenceModality(str, Enum):
    TEXT = "text"
    MANUSCRIPT_HTR = "manuscript_htr"
    IMAGE_VLM = "image_vlm"
    AUDIO_ASR = "audio_asr"
    ARCHIVE_CATALOGUE = "archive_catalogue"
    VIDEO = "video"

class SourceReliabilityTier(str, Enum):
    TIER_A = "A"  # Government, intergovernmental, academic, national library
    TIER_B = "B"  # Cited encyclopedia, scholarly paper, established cultural media
    TIER_C = "C"  # Tertiary, exam-prep, travel blog (used strictly to document competing claims)

class DivergenceGrade(str, Enum):
    NONE = "none"   # Sources agree -> merged
    SOFT = "soft"   # Precision or counting-basis difference -> merged with alternate labels & note
    HARD = "hard"   # Genuine factual/interpretive conflict -> NOT merged; dual-provenance preserved

class AccessLevel(str, Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    SACRED_NOT_MACHINE_QUERYABLE = "sacred-not-machine-queryable"

@dataclass
class SourceMetadata:
    source_id: str
    title: str
    url: str
    publisher: str
    reliability_tier: SourceReliabilityTier
    retrieval_date: str = "2026-10-24"
    caveats: str = ""

@dataclass
class E13AttributeAssignment:
    """
    Modeled on CIDOC-CRM E13 Attribute Assignment.
    Represents a claim about a property as its own event with source, basis, confidence, and timestamp.
    """
    assignment_id: str
    entity_id: str
    relation: str
    claim_text: str
    claim_value_normalized: str
    evidence_modality: EvidenceModality
    source_id: str
    source_title: str
    source_url: str
    source_reliability_tier: SourceReliabilityTier
    claim_language: str = "en"
    divergence_group_id: Optional[str] = None
    divergence_grade: DivergenceGrade = DivergenceGrade.NONE
    access_level: AccessLevel = AccessLevel.PUBLIC
    confidence: float = 0.95
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    evidence_media_id: Optional[str] = None
    notes: str = ""

@dataclass
class CommunityAnnotation:
    """
    Additive community review layer (Section 6.4 & Section 16).
    Never overwrites or deletes an archival claim.
    """
    annotation_id: str
    entity_id: str
    divergence_group_id: str
    reviewer_name: str
    reviewer_role: str  # e.g., 'Village Elder', 'Cultural Custodian', 'Heritage Scholar'
    adjudication_text: str
    recommended_weight: float = 1.0  # Weight applied in community-grounded queries
    data_sovereignty_consent: bool = True
    access_level_recommendation: AccessLevel = AccessLevel.PUBLIC
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

@dataclass
class HeritageEntity:
    entity_id: str
    canonical_name: str
    cidoc_class: CIDOCClass
    entity_type: str
    aliases: List[str] = field(default_factory=list)
    name_meitei_script: Optional[str] = None
    description: str = ""
    access_level: AccessLevel = AccessLevel.PUBLIC
    media_pointers: List[str] = field(default_factory=list)
    attributes: Dict[str, List[E13AttributeAssignment]] = field(default_factory=dict)
    community_annotations: List[CommunityAnnotation] = field(default_factory=list)

    def get_relations(self) -> List[str]:
        return list(self.attributes.keys())

    def has_divergence(self, relation: Optional[str] = None) -> bool:
        if relation:
            assignments = self.attributes.get(relation, [])
            return any(a.divergence_grade == DivergenceGrade.HARD for a in assignments)
        return any(
            any(a.divergence_grade == DivergenceGrade.HARD for a in assignments)
            for assignments in self.attributes.values()
        )
