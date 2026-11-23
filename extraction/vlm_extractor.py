"""
VLM Triple Extractor for Visual Heritage Modalities.
Maps image visual features, materials, and iconography to CIDOC-CRM candidate triples.
"""
from typing import Dict, List, Any
from ingestion.vlm_caption_module import VLMCaptionModule

class VLMExtractor:
    def __init__(self, vlm_module: VLMCaptionModule):
        self.vlm = vlm_module

    def extract_from_image(self, image_path: str) -> Dict[str, Any]:
        """
        Runs visual analysis and outputs normalized candidate triples.
        """
        analysis = self.vlm.analyze_image(image_path)
        if not analysis.get("success"):
            return {"entities": [], "triples": []}

        entities = [{
            "name": analysis["title"],
            "aliases": [analysis.get("primary_entity_id", "")],
            "meitei_script": None,
            "type": "Monument"
        }]

        triples = []
        for cand in analysis.get("candidate_triples", []):
            triples.append({
                "subject": cand["subject"],
                "relation": cand["relation"],
                "object": cand["object"],
                "evidence_excerpt": analysis["caption"],
                "confidence": analysis.get("confidence", 0.90),
                "cidoc_property": cand.get("cidoc", "P2_has_type"),
                "modality": "image_vlm"
            })

        return {
            "entities": entities,
            "triples": triples,
            "caption": analysis["caption"],
            "iconography_tags": analysis["iconography_tags"]
        }
