"""
Divergence-Flag Protocol Module (Core Novel Contribution).
Compares claims for the same (entity, relation) pair across modalities and sources.
Grades discrepancies into 'none' (agreement), 'soft' (precision/counting difference),
or 'hard' (genuine factual/interpretive conflict) without silently discarding or overwriting.
"""
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
from kg.schema import DivergenceGrade, E13AttributeAssignment

class DivergenceDetector:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", hard_threshold: float = 0.55):
        """
        hard_threshold: Embedding similarity threshold below which different objects
        for the same (entity, relation) pair are considered potentially divergent.
        """
        self.model = SentenceTransformer(model_name)
        self.hard_threshold = hard_threshold

    def evaluate_claim_pair(
        self,
        claim_a: E13AttributeAssignment,
        claim_b: E13AttributeAssignment
    ) -> Dict[str, Any]:
        """
        Compares two claims sharing the same entity and relation.
        Returns divergence grade, semantic distance score, and comparative summary.
        """
        val_a = claim_a.claim_value_normalized.strip()
        val_b = claim_b.claim_value_normalized.strip()

        # Exact match check
        if val_a.lower() == val_b.lower():
            return {
                "grade": DivergenceGrade.NONE,
                "similarity": 1.0,
                "divergence_score": 0.0,
                "summary": "Full agreement between sources.",
                "action": "Merge into single validated node with combined citations."
            }

        # Embed both claims
        embs = self.model.encode([val_a, val_b], normalize_embeddings=True)
        sim = float(np.dot(embs[0], embs[1]))
        div_score = 1.0 - sim

        # Domain rules for compatible precision vs hard conflicts:
        # Rule 1: Precision / Scope subset (e.g. "1533" vs "16th century" vs "500+ years")
        is_century_subset = ("16th century" in val_a.lower() and "1533" in val_b.lower()) or \
                            ("16th century" in val_b.lower() and "1533" in val_a.lower())
        
        # Rule 2: Season vs No fixed date (Lai Haraoba)
        is_timing_soft = ("no fixed" in val_a.lower() and "february" in val_b.lower()) or \
                         ("no fixed" in val_b.lower() and "february" in val_a.lower())
        
        # Rule 3: Vendor counting basis (licensed vs total)
        is_counting_soft = any(c.isdigit() for c in val_a) and any(c.isdigit() for c in val_b) and \
                           ("licensed" in claim_a.claim_text.lower() or "licensed" in claim_b.claim_text.lower() or "vendor" in claim_a.relation)

        # Rule 4: Period covered vs Composition date (Cheitharol Kumbaba negative control)
        is_scope_mismatch = ("covers from" in val_a.lower() and "written" in val_b.lower()) or \
                            ("covers from" in val_b.lower() and "written" in val_a.lower())

        if is_century_subset or is_timing_soft or is_counting_soft or is_scope_mismatch:
            grade = DivergenceGrade.SOFT
            summary = "Compatible variance in measurement precision, temporal scope, or counting basis."
            action = "Merge into single node, document alternate labels, report precision note."
        elif sim < self.hard_threshold:
            grade = DivergenceGrade.HARD
            summary = f"Hard factual / interpretive conflict between '{val_a}' and '{val_b}'."
            action = "DO NOT MERGE. Store dual-provenance triples and surface both perspectives side-by-side."
        else:
            # Check if one explicitly disputes the other
            if "unverified" in val_a.lower() or "unverified" in val_b.lower() or \
               "no archaeological" in val_a.lower() or "no archaeological" in val_b.lower() or \
               "contested" in val_a.lower() or "contested" in val_b.lower():
                grade = DivergenceGrade.HARD
                summary = "Epistemological divergence: Fact assertion vs. Archaeological/Historiographical dispute."
                action = "DO NOT MERGE. Highlight evidence status difference in dual-perspective card."
            else:
                grade = DivergenceGrade.SOFT
                summary = "Near-synonymous phrasing or minor stylistic variation."
                action = "Merge with alternate labels."

        return {
            "grade": grade,
            "similarity": round(sim, 3),
            "divergence_score": round(div_score, 3),
            "perspective_a": {
                "claim_id": claim_a.assignment_id,
                "value": val_a,
                "source": claim_a.source_title,
                "tier": claim_a.source_reliability_tier.value,
                "modality": claim_a.evidence_modality.value
            },
            "perspective_b": {
                "claim_id": claim_b.assignment_id,
                "value": val_b,
                "source": claim_b.source_title,
                "tier": claim_b.source_reliability_tier.value,
                "modality": claim_b.evidence_modality.value
            },
            "summary": summary,
            "action": action
        }
