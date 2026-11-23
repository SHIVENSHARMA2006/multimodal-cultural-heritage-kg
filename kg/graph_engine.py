"""
High-Performance Embedded Cultural Heritage Knowledge Graph Engine.
Built on NetworkX with CIDOC-CRM alignment, dual-provenance E13 edge/attribute modeling,
cross-lingual Meetei Mayek script indexing, and subgraph extraction for GraphRAG.
"""
import os
import csv
import json
import networkx as nx
from typing import Dict, List, Optional, Any, Tuple
from kg.schema import (
    CIDOCClass,
    EvidenceModality,
    SourceReliabilityTier,
    DivergenceGrade,
    AccessLevel,
    SourceMetadata,
    E13AttributeAssignment,
    CommunityAnnotation,
    HeritageEntity
)
from kg.provenance import ProvenanceManager

class HeritageGraphEngine:
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = data_dir
        self.graph = nx.MultiDiGraph()
        self.entities: Dict[str, HeritageEntity] = {}
        self.alias_to_entity_id: Dict[str, str] = {}
        self.meitei_to_entity_id: Dict[str, str] = {}
        self.provenance = ProvenanceManager()
        self._load_datasets()

    def _determine_cidoc_class(self, entity_type: str) -> CIDOCClass:
        t = entity_type.lower()
        if any(x in t for x in ["monument", "artifact", "symbol", "structure", "place", "building"]):
            return CIDOCClass.E22_HUMAN_MADE_OBJECT
        elif any(x in t for x in ["king", "ruler", "person", "deity", "clan", "actor"]):
            return CIDOCClass.E39_ACTOR
        elif any(x in t for x in ["war", "battle", "event", "festival", "dance", "burning"]):
            return CIDOCClass.E5_EVENT
        elif any(x in t for x in ["script", "manuscript", "text", "corpus", "chronicle"]):
            return CIDOCClass.E73_INFORMATION_OBJECT
        elif any(x in t for x in ["place", "ground", "complex", "state"]):
            return CIDOCClass.E53_PLACE
        return CIDOCClass.E22_HUMAN_MADE_OBJECT

    def _normalize_key(self, text: str) -> str:
        return text.strip().lower()

    def _load_datasets(self):
        # 1. Load Sources Registry
        sources_path = os.path.join(self.data_dir, "sources_registry.csv")
        if os.path.exists(sources_path):
            with open(sources_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tier_str = row.get("reliability_tier", "B").strip().upper()
                    tier = SourceReliabilityTier.TIER_B
                    if tier_str == "A":
                        tier = SourceReliabilityTier.TIER_A
                    elif tier_str == "C":
                        tier = SourceReliabilityTier.TIER_C

                    sm = SourceMetadata(
                        source_id=row.get("source_id", "").strip(),
                        title=row.get("source_title", "").strip(),
                        url=row.get("source_url", "").strip(),
                        publisher=row.get("publisher", "").strip(),
                        reliability_tier=tier,
                        retrieval_date=row.get("retrieval_date", "2026-10-24").strip(),
                        caveats=row.get("notes", "").strip()
                    )
                    self.provenance.register_source(sm)

        # 2. Load Divergence Cases
        div_path = os.path.join(self.data_dir, "divergence_cases.csv")
        if os.path.exists(div_path):
            with open(div_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    g_str = row.get("grade", "none").strip().lower()
                    grade = DivergenceGrade.NONE
                    if g_str == "hard":
                        grade = DivergenceGrade.HARD
                    elif g_str == "soft":
                        grade = DivergenceGrade.SOFT

                    claim_ids = [c.strip() for c in row.get("claim_ids", "").split(";") if c.strip()]
                    self.provenance.register_divergence_group(
                        group_id=row.get("group_id", "").strip(),
                        entity_id=row.get("entity_id", "").strip(),
                        relation=row.get("relation", "").strip(),
                        divergence_type=row.get("divergence_type", "").strip(),
                        grade=grade,
                        claim_ids=claim_ids,
                        why_divergent=row.get("why_divergent", "").strip(),
                        expected_behavior=row.get("expected_system_behavior", "").strip(),
                        notes=row.get("notes", "").strip()
                    )

        # 3. Load Manipur Heritage Claims
        claims_path = os.path.join(self.data_dir, "manipur_heritage_claims.csv")
        if os.path.exists(claims_path):
            with open(claims_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    entity_id = row.get("entity_id", "").strip()
                    entity_name = row.get("entity_name", "").strip()
                    entity_type = row.get("entity_type", "Heritage Entity").strip()
                    aliases_raw = row.get("entity_aliases", "").strip()
                    aliases = [a.strip() for a in aliases_raw.split(";") if a.strip()] if aliases_raw else []
                    meitei_name = row.get("entity_name_meitei_script", "").strip() or None

                    if entity_id not in self.entities:
                        cidoc_cls = self._determine_cidoc_class(entity_type)
                        ent = HeritageEntity(
                            entity_id=entity_id,
                            canonical_name=entity_name,
                            cidoc_class=cidoc_cls,
                            entity_type=entity_type,
                            aliases=aliases,
                            name_meitei_script=meitei_name
                        )
                        self.entities[entity_id] = ent
                        self.graph.add_node(
                            entity_id,
                            name=entity_name,
                            cidoc_class=cidoc_cls.value,
                            entity_type=entity_type,
                            aliases=aliases,
                            meitei_name=meitei_name or ""
                        )
                        # Index aliases
                        self.alias_to_entity_id[self._normalize_key(entity_name)] = entity_id
                        for alias in aliases:
                            self.alias_to_entity_id[self._normalize_key(alias)] = entity_id
                        if meitei_name:
                            self.meitei_to_entity_id[meitei_name.strip()] = entity_id

                    # Create E13 Attribute Assignment
                    rel = row.get("relation", "").strip()
                    div_group = row.get("divergence_group_id", "").strip() or None
                    grade = DivergenceGrade.NONE
                    if div_group and div_group in self.provenance.divergence_registry:
                        grade = self.provenance.divergence_registry[div_group]["grade"]

                    tier_str = row.get("source_reliability_tier", "B").strip().upper()
                    tier = SourceReliabilityTier.TIER_B
                    if tier_str == "A":
                        tier = SourceReliabilityTier.TIER_A
                    elif tier_str == "C":
                        tier = SourceReliabilityTier.TIER_C

                    mod_str = row.get("evidence_modality", "text").strip()
                    try:
                        modality = EvidenceModality(mod_str)
                    except ValueError:
                        modality = EvidenceModality.TEXT

                    assignment = E13AttributeAssignment(
                        assignment_id=row.get("claim_id", "").strip(),
                        entity_id=entity_id,
                        relation=rel,
                        claim_text=row.get("claim_text", "").strip(),
                        claim_value_normalized=row.get("claim_value_normalized", "").strip(),
                        evidence_modality=modality,
                        source_id=row.get("source_id", "").strip(),
                        source_title=row.get("source_title", "").strip(),
                        source_url=row.get("source_url", "").strip(),
                        source_reliability_tier=tier,
                        claim_language=row.get("claim_language", "en").strip(),
                        divergence_group_id=div_group,
                        divergence_grade=grade,
                        access_level=AccessLevel.PUBLIC,
                        notes=row.get("notes", "").strip()
                    )

                    # Add attribute to entity
                    if rel not in self.entities[entity_id].attributes:
                        self.entities[entity_id].attributes[rel] = []
                    self.entities[entity_id].attributes[rel].append(assignment)

                    # Add edge or target node if relation points to another recognized entity or value
                    val_norm = assignment.claim_value_normalized
                    self.graph.add_edge(
                        entity_id,
                        val_norm,
                        relation=rel,
                        source=assignment.source_title,
                        divergence_grade=grade.value,
                        claim_id=assignment.assignment_id,
                        modality=modality.value
                    )

    def find_entity(self, query: str) -> Optional[HeritageEntity]:
        q = query.strip()
        if not q:
            return None
        # Exact ID match
        if q in self.entities:
            return self.entities[q]
        # Meetei Mayek script match
        if q in self.meitei_to_entity_id:
            return self.entities[self.meitei_to_entity_id[q]]
        # Canonical or alias match
        norm = self._normalize_key(q)
        if norm in self.alias_to_entity_id:
            return self.entities[self.alias_to_entity_id[norm]]
        # Substring / partial match
        for key, eid in self.alias_to_entity_id.items():
            if norm in key or key in norm:
                return self.entities[eid]
        return None

    def search_entities(self, query: str, limit: int = 10) -> List[HeritageEntity]:
        q = query.strip().lower()
        if not q:
            return list(self.entities.values())[:limit]
        results = []
        seen = set()
        for ent in self.entities.values():
            score = 0
            if q == ent.canonical_name.lower():
                score += 10
            elif q in ent.canonical_name.lower():
                score += 5
            elif ent.name_meitei_script and q in ent.name_meitei_script:
                score += 8
            elif any(q in a.lower() for a in ent.aliases):
                score += 4
            elif any(q in rel.lower() for rel in ent.attributes):
                score += 2

            if score > 0 and ent.entity_id not in seen:
                results.append((score, ent))
                seen.add(ent.entity_id)

        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]

    def get_subgraph(self, entity_id: str, depth: int = 1) -> Dict[str, Any]:
        """
        Extracts subgraph around entity_id for visual display and GraphRAG context.
        """
        if entity_id not in self.graph:
            return {"nodes": [], "edges": []}

        nodes_set = {entity_id}
        current_layer = {entity_id}
        for _ in range(depth):
            next_layer = set()
            for n in current_layer:
                if self.graph.has_node(n):
                    neighbors = set(self.graph.successors(n)) | set(self.graph.predecessors(n))
                    next_layer.update(neighbors)
            nodes_set.update(next_layer)
            current_layer = next_layer

        nodes_data = []
        for n in nodes_set:
            if n in self.entities:
                ent = self.entities[n]
                nodes_data.append({
                    "id": n,
                    "label": ent.canonical_name,
                    "meitei_name": ent.name_meitei_script or "",
                    "cidoc_class": ent.cidoc_class.value,
                    "type": ent.entity_type,
                    "has_divergence": ent.has_divergence()
                })
            else:
                nodes_data.append({
                    "id": n,
                    "label": str(n)[:40],
                    "meitei_name": "",
                    "cidoc_class": "Value",
                    "type": "AttributeValue",
                    "has_divergence": False
                })

        edges_data = []
        for u, v, k, data in self.graph.edges(nodes_set, keys=True, data=True):
            if v in nodes_set:
                edges_data.append({
                    "source": u,
                    "target": v,
                    "relation": data.get("relation", ""),
                    "modality": data.get("modality", "text"),
                    "divergence_grade": data.get("divergence_grade", "none"),
                    "source_title": data.get("source", "")
                })

        return {"nodes": nodes_data, "edges": edges_data}

    def get_statistics(self) -> Dict[str, Any]:
        total_claims = sum(
            len(assignments)
            for ent in self.entities.values()
            for assignments in ent.attributes.values()
        )
        modality_counts = {}
        divergence_counts = {"none": 0, "soft": 0, "hard": 0}

        for ent in self.entities.values():
            for assignments in ent.attributes.values():
                for a in assignments:
                    mod = a.evidence_modality.value
                    modality_counts[mod] = modality_counts.get(mod, 0) + 1
                    div = a.divergence_grade.value
                    divergence_counts[div] = divergence_counts.get(div, 0) + 1

        return {
            "total_entities": len(self.entities),
            "total_claims": total_claims,
            "total_sources": len(self.provenance.sources),
            "divergence_groups": len(self.provenance.divergence_registry),
            "modalities": modality_counts,
            "divergence_grades": divergence_counts,
            "community_annotations": len(self.provenance.community_annotations)
        }
