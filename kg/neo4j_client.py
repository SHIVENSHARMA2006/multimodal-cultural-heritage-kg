"""
Neo4j Client for Cultural Heritage Knowledge Graph.
Supports synchronization with Neo4j Aura / Community Edition using Cypher queries.
Gracefully falls back to the embedded HeritageGraphEngine if Neo4j is not configured.
"""
import os
from typing import Optional, Dict, Any, List
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

from kg.graph_engine import HeritageGraphEngine

class Neo4jHeritageClient:
    def __init__(self, fallback_engine: Optional[HeritageGraphEngine] = None):
        self.uri = os.getenv("NEO4J_URI", "")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "")
        self.driver = None
        self.is_connected = False
        self.engine = fallback_engine or HeritageGraphEngine()

        if NEO4J_AVAILABLE and self.uri and self.password:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                self.driver.verify_connectivity()
                self.is_connected = True
                print("Connected to Neo4j successfully.")
            except Exception as e:
                print(f"Neo4j connection failed ({e}). Using embedded HeritageGraphEngine.")
                self.is_connected = False
        else:
            self.is_connected = False

    def close(self):
        if self.driver:
            self.driver.close()

    def sync_from_engine(self) -> bool:
        """
        Pushes all entities and claims from the embedded graph engine to Neo4j.
        """
        if not self.is_connected:
            return False

        with self.driver.session() as session:
            # Create schema constraints
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (e:HeritageEntity) REQUIRE e.id IS UNIQUE")
            
            # Sync entities
            for eid, ent in self.engine.entities.items():
                session.run(
                    """
                    MERGE (e:HeritageEntity {id: $id})
                    SET e.name = $name,
                        e.cidoc_class = $cidoc_class,
                        e.type = $type,
                        e.meitei_name = $meitei_name,
                        e.aliases = $aliases
                    """,
                    id=eid,
                    name=ent.canonical_name,
                    cidoc_class=ent.cidoc_class.value,
                    type=ent.entity_type,
                    meitei_name=ent.name_meitei_script or "",
                    aliases=ent.aliases
                )
        return True

    def query(self, cypher: str, parameters: Optional[Dict] = None) -> List[Dict]:
        if not self.is_connected:
            return []
        with self.driver.session() as session:
            result = session.run(cypher, parameters or {})
            return [record.data() for record in result]
