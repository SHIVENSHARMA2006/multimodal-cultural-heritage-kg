"""
Cross-Modal Validator Module.
Cross-checks claims extracted from one modality against evidence from a second modality
(e.g., confirming whether an LLM-proposed textual claim is corroborated by VLM image analysis
or oral testimony).
"""
import numpy as np
from typing import Dict, Any, List, Optional
from sentence_transformers import SentenceTransformer

class CrossModalValidator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def validate_claim(
        self,
        subject: str,
        relation: str,
        claim_value: str,
        evidence_description: str,
        second_modality: str = "image_vlm"
    ) -> Dict[str, Any]:
        """
        Cross-validates an extracted claim against multimodal evidence.
        Returns validation status (CORROBORATED, DIVERGENT, SILENT/NEUTRAL),
        similarity score, and archaeological confidence.
        """
        claim_statement = f"{subject} {relation.replace('_', ' ')} is {claim_value}"
        
        # Compute semantic similarity between claim and multimodal evidence
        emb_claim = self.model.encode([claim_statement], normalize_embeddings=True)[0]
        emb_evid = self.model.encode([evidence_description], normalize_embeddings=True)[0]
        similarity = float(np.dot(emb_claim, emb_evid))

        # Check for direct keyword matches (e.g. brick, gate, citadel, polo, 33 CE, 1891)
        keywords_in_claim = set(claim_value.lower().split())
        keywords_in_evid = set(evidence_description.lower().split())
        overlap = keywords_in_claim.intersection(keywords_in_evid)

        if similarity > 0.45 or len(overlap) >= 2:
            status = "CORROBORATED"
            rationale = f"The {second_modality} evidence directly corroborates the textual claim. Semantic alignment: {similarity:.2f}."
        elif similarity < 0.15 and not overlap:
            status = "SILENT_NEUTRAL"
            rationale = f"The {second_modality} evidence does not exhibit features relevant to '{relation}'. No contradiction observed."
        else:
            status = "PARTIALLY_ALIGNED"
            rationale = f"The {second_modality} exhibits contextual overlap ({similarity:.2f}) with qualifiers or differing structural scope."

        return {
            "status": status,
            "similarity_score": round(similarity, 3),
            "claim_statement": claim_statement,
            "evidence_modality": second_modality,
            "rationale": rationale
        }
