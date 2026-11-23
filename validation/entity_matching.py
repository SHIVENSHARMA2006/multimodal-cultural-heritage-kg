"""
Embedding-Based Entity Matching Module.
Computes semantic similarity between extracted entity mentions and existing KG entities
to prevent duplicate node pollution and resolve aliases across languages and scripts.
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from sentence_transformers import SentenceTransformer
from kg.graph_engine import HeritageGraphEngine
from kg.schema import HeritageEntity

class EntityMatcher:
    def __init__(self, engine: HeritageGraphEngine, model_name: str = "all-MiniLM-L6-v2", threshold: float = 0.55):
        self.engine = engine
        self.threshold = threshold
        self.model = SentenceTransformer(model_name)
        self.entity_cache: List[Tuple[str, str, np.ndarray]] = []
        self._build_index()

    def _build_index(self):
        """
        Pre-computes embeddings for all canonical entity names and their aliases.
        """
        names_to_embed = []
        mapping = []
        for eid, ent in self.engine.entities.items():
            # Add canonical name
            names_to_embed.append(ent.canonical_name)
            mapping.append((eid, ent.canonical_name))
            # Add aliases
            for alias in ent.aliases:
                names_to_embed.append(alias)
                mapping.append((eid, alias))

        if names_to_embed:
            embeddings = self.model.encode(names_to_embed, normalize_embeddings=True)
            self.entity_cache = [(mapping[i][0], mapping[i][1], embeddings[i]) for i in range(len(mapping))]

    def match_entity(self, surface_form: str) -> Tuple[Optional[HeritageEntity], float]:
        """
        Matches a surface mention to the most probable existing KG entity.
        Returns (HeritageEntity, similarity_score).
        """
        # 1. Exact or Alias Match First (Fast path)
        exact_ent = self.engine.find_entity(surface_form)
        if exact_ent:
            return exact_ent, 1.0

        if not self.entity_cache:
            return None, 0.0

        # 2. Embedding Semantic Search
        query_vec = self.model.encode([surface_form], normalize_embeddings=True)[0]
        best_score = -1.0
        best_eid = None

        for eid, label, emb in self.entity_cache:
            score = float(np.dot(query_vec, emb))
            if score > best_score:
                best_score = score
                best_eid = eid

        if best_score >= self.threshold and best_eid:
            return self.engine.entities[best_eid], best_score

        return None, best_score
