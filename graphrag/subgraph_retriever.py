"""
Subgraph and Multimodal Chunk Retrieval Engine.
Retrieves entity neighborhoods, connected attributes, divergence flags,
and attached multimodal evidence (images, audio snippets, manuscript folios).
"""
import os
import glob
from typing import Dict, List, Any, Optional
from kg.graph_engine import HeritageGraphEngine
from kg.schema import HeritageEntity, E13AttributeAssignment, DivergenceGrade

class SubgraphRetriever:
    def __init__(self, engine: HeritageGraphEngine):
        self.engine = engine

    def retrieve_context(self, entity: HeritageEntity, relation_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves all relevant claims, divergence groups, and multimodal media
        associated with an entity and optional relation hint.
        """
        eid = entity.entity_id
        subgraph = self.engine.get_subgraph(eid, depth=1)

        # Collect claims
        relevant_assignments: List[E13AttributeAssignment] = []
        has_hard_divergence = False
        divergence_details = []

        # Find if specific queried relation matches
        matched_rel_assignments = []
        if relation_hint:
            for rel, assignments in entity.attributes.items():
                if relation_hint.lower() in rel.lower() or rel.lower() in relation_hint.lower():
                    matched_rel_assignments.extend(assignments)

        if matched_rel_assignments:
            relevant_assignments = matched_rel_assignments
            # Check if this specific queried relation has hard divergence
            for a in matched_rel_assignments:
                if a.divergence_grade == DivergenceGrade.HARD:
                    has_hard_divergence = True
                    if a.divergence_group_id:
                        div_info = self.engine.provenance.get_divergence_info(a.divergence_group_id)
                        if div_info and div_info not in divergence_details:
                            divergence_details.append(div_info)
        else:
            # Fallback to all assignments
            for rel, assignments in entity.attributes.items():
                for a in assignments:
                    relevant_assignments.append(a)
                    if a.divergence_grade == DivergenceGrade.HARD:
                        has_hard_divergence = True
                        if a.divergence_group_id:
                            div_info = self.engine.provenance.get_divergence_info(a.divergence_group_id)
                            if div_info and div_info not in divergence_details:
                                divergence_details.append(div_info)

        # Collect multimodal evidence
        multimodal_evidence = self._find_multimodal_evidence(entity)

        # Collect community annotations if any
        annotations = self.engine.provenance.get_annotations_for_entity(eid)

        return {
            "entity": entity,
            "assignments": relevant_assignments,
            "has_hard_divergence": has_hard_divergence,
            "divergence_details": divergence_details,
            "subgraph": subgraph,
            "multimodal_evidence": multimodal_evidence,
            "community_annotations": annotations
        }

    def _find_multimodal_evidence(self, entity: HeritageEntity) -> List[Dict[str, Any]]:
        evidence = []
        name = entity.canonical_name.lower()
        eid = entity.entity_id.lower()

        # Check images
        for img_path in glob.glob("data/images/*.*"):
            fname = os.path.basename(img_path).lower()
            if not fname.endswith(('.jpg', '.jpeg', '.png')):
                continue
            if "kangla" in name and "kangla" in fname:
                evidence.append({
                    "modality": "image_vlm",
                    "title": os.path.basename(img_path),
                    "path": img_path,
                    "description": "Historical monument image of Kangla Palace Citadel and architectural features."
                })
            elif "sanggai yumpham" in name and ("sanggai" in fname or "citadel" in fname):
                evidence.append({
                    "modality": "image_vlm",
                    "title": os.path.basename(img_path),
                    "path": img_path,
                    "description": "Meitei imperial doorway architecture of Sanggai Yumpham."
                })

        # Check manuscripts
        for ms_path in glob.glob("data/manuscripts/*.*"):
            fname = os.path.basename(ms_path).lower()
            if not fname.endswith(('.jpg', '.jpeg', '.png')):
                continue
            if ("puya" in name or "subika" in name or "meitei mayek" in name or "script" in name):
                evidence.append({
                    "modality": "manuscript_htr",
                    "title": os.path.basename(ms_path),
                    "path": ms_path,
                    "description": "Historical Meetei Mayek manuscript folio showing ancient script and cosmological diagrams."
                })

        # Check audio
        for aud_path in glob.glob("data/audio/*.wav"):
            fname = os.path.basename(aud_path).lower()
            if "kangla" in name and "kangla" in fname:
                evidence.append({
                    "modality": "audio_asr",
                    "title": os.path.basename(aud_path),
                    "path": aud_path,
                    "description": "Oral testimony of village elder regarding traditional origins of Kangla."
                })
            elif "sankirtana" in name and "sankirtana" in fname:
                evidence.append({
                    "modality": "audio_asr",
                    "title": os.path.basename(aud_path),
                    "path": aud_path,
                    "description": "Sankirtana ritual chant recording with Khol drum and cymbals."
                })
            elif "lai haraoba" in name and "lai_haraoba" in fname:
                evidence.append({
                    "modality": "audio_asr",
                    "title": os.path.basename(aud_path),
                    "path": aud_path,
                    "description": "Traditional Maibi ritual song performance from Lai Haraoba ceremony."
                })

        return evidence
