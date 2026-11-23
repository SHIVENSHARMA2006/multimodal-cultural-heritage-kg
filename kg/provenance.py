"""
Dual-Provenance and Divergence Storage Manager.
Implements CIDOC-CRM E13 Attribute Assignment pattern to maintain conflicting claims
side-by-side with full source provenance, preventing silent arbitration.
"""
from typing import Dict, List, Optional, Tuple
from kg.schema import (
    E13AttributeAssignment,
    CommunityAnnotation,
    SourceMetadata,
    DivergenceGrade,
    SourceReliabilityTier,
    AccessLevel,
    EvidenceModality
)

class ProvenanceManager:
    def __init__(self):
        self.sources: Dict[str, SourceMetadata] = {}
        self.divergence_registry: Dict[str, Dict] = {}
        self.community_annotations: List[CommunityAnnotation] = []

    def register_source(self, source: SourceMetadata):
        self.sources[source.source_id] = source

    def get_source(self, source_id: str) -> Optional[SourceMetadata]:
        return self.sources.get(source_id)

    def register_divergence_group(
        self,
        group_id: str,
        entity_id: str,
        relation: str,
        divergence_type: str,
        grade: DivergenceGrade,
        claim_ids: List[str],
        why_divergent: str,
        expected_behavior: str,
        notes: str = ""
    ):
        self.divergence_registry[group_id] = {
            "group_id": group_id,
            "entity_id": entity_id,
            "relation": relation,
            "divergence_type": divergence_type,
            "grade": grade,
            "claim_ids": claim_ids,
            "why_divergent": why_divergent,
            "expected_behavior": expected_behavior,
            "notes": notes
        }

    def get_divergence_info(self, group_id: str) -> Optional[Dict]:
        return self.divergence_registry.get(group_id)

    def add_community_annotation(self, annotation: CommunityAnnotation) -> bool:
        """
        Appends an additive community review annotation without modifying or deleting
        underlying archival claims.
        """
        self.community_annotations.append(annotation)
        return True

    def get_annotations_for_entity(self, entity_id: str) -> List[CommunityAnnotation]:
        return [ann for ann in self.community_annotations if ann.entity_id == entity_id]

    def get_annotations_for_group(self, group_id: str) -> List[CommunityAnnotation]:
        return [ann for ann in self.community_annotations if ann.divergence_group_id == group_id]
