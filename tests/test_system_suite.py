"""
Comprehensive Automated Test Suite for Multimodal Cultural Heritage Knowledge Graph.
Tests API endpoints, GraphRAG retrieval, Ingestion modules (HTR, VLM, ASR),
Divergence Detection, Entity Matching, and edge/failure cases.
"""
import os
import sys
import json
import urllib.request
import urllib.error
import traceback
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from kg.graph_engine import HeritageGraphEngine
from kg.schema import DivergenceGrade, AccessLevel, EvidenceModality, CommunityAnnotation
from graphrag.query_translation import QueryTranslator
from graphrag.subgraph_retriever import SubgraphRetriever
from graphrag.answer_generator import AnswerGenerator
from ingestion.htr_module import ManuscriptHTRModule
from ingestion.vlm_caption_module import VLMCaptionModule
from ingestion.asr_module import SpeechASRModule
from ingestion.text_normalize import TextNormalizer
from validation.entity_matching import EntityMatcher
from validation.cross_modal_validator import CrossModalValidator
from validation.divergence_detector import DivergenceDetector
from extraction.llm_extractor import LLMExtractor
from extraction.vlm_extractor import VLMExtractor

class TestHeritageSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "="*70)
        print("  STARTING HERITAGE KNOWLEDGE GRAPH COMPREHENSIVE TEST SUITE")
        print("="*70)
        cls.engine = HeritageGraphEngine()
        cls.translator = QueryTranslator(cls.engine)
        cls.retriever = SubgraphRetriever(cls.engine)
        cls.generator = AnswerGenerator()
        cls.htr = ManuscriptHTRModule()
        cls.vlm = VLMCaptionModule()
        cls.asr = SpeechASRModule()
        cls.matcher = EntityMatcher(cls.engine)
        cls.cross_validator = CrossModalValidator()
        cls.div_detector = DivergenceDetector()
        cls.llm_extractor = LLMExtractor()
        cls.vlm_extractor = VLMExtractor(cls.vlm)

    # -------------------------------------------------------------
    # 1. KNOWLEDGE GRAPH ENGINE TESTS
    # -------------------------------------------------------------
    def test_01_graph_loading(self):
        stats = self.engine.get_statistics()
        self.assertGreater(stats["total_entities"], 30, "Entities should exceed 30")
        self.assertGreater(stats["total_claims"], 150, "Claims should exceed 150")
        self.assertGreater(stats["total_sources"], 50, "Sources should exceed 50")
        self.assertGreater(stats["divergence_groups"], 20, "Divergence groups should exceed 20")
        print("  [PASS] Test 01: Graph engine dataset loading verified.")

    def test_02_entity_search_and_alias_resolution(self):
        # Canonical search
        ent = self.engine.find_entity("Kangla Fort")
        self.assertIsNotNone(ent)
        self.assertEqual(ent.entity_id, "E001")

        # Alias search: Pamheiba vs Garib Niwaz vs Gharib Nawaz
        ent_pam = self.engine.find_entity("Gharib Nawaz")
        self.assertIsNotNone(ent_pam)
        self.assertEqual(ent_pam.entity_id, "E011")

        # Meetei Mayek script search
        ent_mayek = self.engine.find_entity("ꯀꯪꯂꯥ")
        self.assertIsNotNone(ent_mayek)
        self.assertEqual(ent_mayek.entity_id, "E001")
        print("  [PASS] Test 02: Entity search & alias resolution verified.")

    def test_03_subgraph_generation(self):
        sg = self.engine.get_subgraph("E001", depth=1)
        self.assertIn("nodes", sg)
        self.assertIn("edges", sg)
        self.assertGreater(len(sg["nodes"]), 1)
        self.assertGreater(len(sg["edges"]), 1)
        
        # Test non-existent entity subgraph (should not crash)
        sg_empty = self.engine.get_subgraph("E99999", depth=1)
        self.assertEqual(len(sg_empty["nodes"]), 0)
        self.assertEqual(len(sg_empty["edges"]), 0)
        print("  [PASS] Test 03: Subgraph extraction and boundary checks verified.")

    # -------------------------------------------------------------
    # 2. INGESTION MODULES TESTS
    # -------------------------------------------------------------
    def test_04_htr_manuscript_ingestion(self):
        manuscripts = self.htr.catalog
        self.assertGreater(len(manuscripts), 0, "Manuscript catalog should not be empty")
        for ms in manuscripts:
            res = self.htr.transcribe_manuscript(ms["filepath"])
            self.assertTrue(res["success"])
            self.assertIn("transcription_mayek", res)
            self.assertIn("translation_en", res)
            self.assertGreater(res["confidence"], 0.7)

        # Test non-existent image handling
        res_fail = self.htr.transcribe_manuscript("data/manuscripts/non_existent.jpg")
        self.assertFalse(res_fail["success"])
        print("  [PASS] Test 04: HTR module & Meetei Mayek transcription verified.")

    def test_05_vlm_monument_understanding(self):
        images = self.vlm.catalog
        self.assertGreater(len(images), 0, "Image catalog should not be empty")
        for im in images:
            res = self.vlm.analyze_image(im["filepath"])
            self.assertTrue(res["success"])
            self.assertIn("caption", res)
            self.assertGreater(len(res["iconography_tags"]), 0)
            self.assertGreater(len(res["candidate_triples"]), 0)

        # Non-existent image check
        res_fail = self.vlm.analyze_image("data/images/non_existent.jpg")
        self.assertFalse(res_fail["success"])
        print("  [PASS] Test 05: VLM module & monument iconography verified.")

    def test_06_asr_speech_ingestion(self):
        manifest = self.asr.manifest
        self.assertGreater(len(manifest), 0, "Audio manifest should not be empty")
        for fname, meta in manifest.items():
            path = meta.get("filepath", f"data/audio/{fname}")
            if os.path.exists(path):
                res = self.asr.transcribe_audio(path)
                self.assertTrue(res["success"])
                self.assertIn("transcript_original", res)
                self.assertIn("english_translation", res)
                self.assertIn("speaker", res)
                self.assertIn("consent_provenance", res)

        # Non-existent audio check
        res_fail = self.asr.transcribe_audio("data/audio/ghost.wav")
        self.assertFalse(res_fail["success"])
        print("  [PASS] Test 06: ASR speech ingestion & consent provenance verified.")

    # -------------------------------------------------------------
    # 3. EXTRACTION & VALIDATION TESTS
    # -------------------------------------------------------------
    def test_07_llm_and_vlm_extraction(self):
        sample_doc = "The ancient fortress of Kangla Fort was founded in 33 CE by King Pakhangba beside the Imphal river."
        res = self.llm_extractor.extract_triples(sample_doc, title="Kangla Fort History", source_tier="B")
        self.assertIn("triples", res)
        self.assertGreater(len(res["triples"]), 0)
        found_founding = any(t["relation"] == "founding_date" for t in res["triples"])
        self.assertTrue(found_founding, "Should extract founding_date")
        print("  [PASS] Test 07: LLM & rule-based triple extraction verified.")

    def test_08_semantic_entity_matching(self):
        # Match slightly misspelled or variant name
        ent, score = self.matcher.match_entity("King Garib Nawaz")
        self.assertIsNotNone(ent)
        self.assertEqual(ent.entity_id, "E011")
        self.assertGreater(score, 0.6)

        ent2, score2 = self.matcher.match_entity("Imphal Kangla Palace")
        self.assertIsNotNone(ent2)
        self.assertEqual(ent2.entity_id, "E001")
        print("  [PASS] Test 08: SentenceTransformer semantic entity matching verified.")

    def test_09_cross_modal_corroboration(self):
        # Corroborating case
        val_res = self.cross_validator.validate_claim(
            subject="Sanggai Yumpham",
            relation="made_from_material",
            claim_value="Red Brick Masonry",
            evidence_description="Historical brick doorway of Sanggai Yumpham showing classical Meitei masonry."
        )
        self.assertEqual(val_res["status"], "CORROBORATED")

        # Neutral case
        val_res_neu = self.cross_validator.validate_claim(
            subject="Kangla Fort",
            relation="vendor_count",
            claim_value="3600 licensed vendors",
            evidence_description="A traditional Meitei sacred garden inside the royal palace precinct."
        )
        self.assertIn(val_res_neu["status"], ["SILENT_NEUTRAL", "PARTIALLY_ALIGNED"])
        print("  [PASS] Test 09: Cross-modal validation & corroboration verified.")

    # -------------------------------------------------------------
    # 4. DIVERGENCE DETECTION & DUAL-PROVENANCE TESTS
    # -------------------------------------------------------------
    def test_10_divergence_detector(self):
        divs = self.engine.provenance.divergence_registry
        # Test D01 (Hard divergence: Kangla founding date 33 CE vs unverified archaeological status)
        self.assertIn("D01", divs)
        self.assertEqual(divs["D01"]["grade"], DivergenceGrade.HARD)

        # Test D04 (Hard divergence: Puya Meithaba 1726 vs 1729 vs apocryphal 1732)
        self.assertIn("D04", divs)
        self.assertEqual(divs["D04"]["grade"], DivergenceGrade.HARD)

        # Test D11a (Soft divergence: vendor count 3615 vs 5000+ vs 6000)
        self.assertIn("D11a", divs)
        self.assertEqual(divs["D11a"]["grade"], DivergenceGrade.SOFT)

        # Test A01 (Agreement control: Kangla capture 27 April 1891)
        self.assertIn("A01", divs)
        self.assertEqual(divs["A01"]["grade"], DivergenceGrade.NONE)
        print("  [PASS] Test 10: Divergence-Flag Protocol & gold cases verified.")

    # -------------------------------------------------------------
    # 5. GRAPHRAG QUERY PIPELINE & EDGE CASES
    # -------------------------------------------------------------
    def test_11_graphrag_divergence_behavior(self):
        # Query known hard divergence
        q = "When was Kangla established?"
        q_trans = self.translator.process_query(q)
        ent = q_trans.get("primary_entity")
        self.assertIsNotNone(ent)
        ctx = self.retriever.retrieve_context(ent, relation_hint=q_trans.get("detected_relation"))
        ans = self.generator.generate_answer(q, ctx, detected_relation=q_trans.get("detected_relation"))
        
        self.assertEqual(ans["behavior"], "present_all_perspectives")
        self.assertGreaterEqual(len(ans["perspectives"]), 2)
        print("  [PASS] Test 11: GraphRAG hard-divergence dual perspective verified.")

    def test_12_graphrag_hallucination_abstention(self):
        # Query deliberate unanswerable probes
        probes = [
            "Who designed the 2006 Kangla Sha statues?",
            "How many Puya manuscripts are currently held in the Kangla Museum?",
            "In what year was the very first Lai Haraoba held?",
            "What does a village elder's recorded oral account say about Kangla's origin?"
        ]
        for p in probes:
            q_trans = self.translator.process_query(p)
            ent = q_trans.get("primary_entity")
            if ent:
                ctx = self.retriever.retrieve_context(ent, relation_hint=q_trans.get("detected_relation"))
                ans = self.generator.generate_answer(p, ctx, detected_relation=q_trans.get("detected_relation"))
            else:
                ctx = {"entity": None, "assignments": []}
                ans = self.generator.generate_answer(p, ctx)
            self.assertEqual(ans["behavior"], "abstain_not_in_kg", f"Probe '{p}' should abstain")
        print("  [PASS] Test 12: Hallucination probes & unrecorded fact abstention verified.")

    def test_13_edge_cases_and_weird_inputs(self):
        # Empty string
        q_empty = self.translator.process_query("")
        self.assertIsNone(q_empty.get("primary_entity"))
        ans_empty = self.generator.generate_answer("", {"entity": None, "assignments": []})
        self.assertEqual(ans_empty["behavior"], "abstain_not_in_kg")

        # Special characters & symbols
        q_sym = self.translator.process_query("@@#$$%^^&&**(())_+!~`{}|[]")
        self.assertIsNotNone(q_sym)

        # Extremely long query
        long_query = "What is the historical significance of Kangla " * 50
        q_long = self.translator.process_query(long_query)
        self.assertIsNotNone(q_long)
        print("  [PASS] Test 13: Edge cases, empty inputs, and boundary checks verified.")

    # -------------------------------------------------------------
    # 6. FASTAPI REST SERVER ENDPOINTS VERIFICATION
    # -------------------------------------------------------------
    def test_14_fastapi_endpoints(self):
        from fastapi.testclient import TestClient
        from api.main import app

        client = TestClient(app)
        
        # 1. Health check
        res = client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")

        # 2. Stats
        res_stats = client.get("/stats")
        self.assertEqual(res_stats.status_code, 200)

        # 3. Query
        res_q = client.post("/query", json={"query": "When was Kangla established?"})
        self.assertEqual(res_q.status_code, 200)
        q_resp = res_q.json()
        self.assertEqual(q_resp["behavior"], "present_all_perspectives")

        # 4. Entities Search
        res_ent = client.get("/entities?q=Kangla")
        self.assertEqual(res_ent.status_code, 200)

        # 5. Subgraph
        res_sg = client.get("/subgraph/E001?depth=1")
        self.assertEqual(res_sg.status_code, 200)

        # 6. Divergences
        res_div = client.get("/divergences")
        self.assertEqual(res_div.status_code, 200)

        # 7. Community Review Submission (Additive)
        review_payload = {
            "entity_id": "E001",
            "divergence_group_id": "D01",
            "reviewer_name": "Test Suite Elder",
            "reviewer_role": "Heritage Custodian",
            "adjudication_text": "Automated verification of additive community adjudication.",
            "access_tier": "public",
            "consent_given": True
        }
        res_rev = client.post("/review", json=review_payload)
        self.assertEqual(res_rev.status_code, 200)
        rev_data = res_rev.json()
        self.assertEqual(rev_data["status"], "success")

        # 8. Ingest listings
        res_ms = client.get("/ingest/manuscripts")
        self.assertEqual(res_ms.status_code, 200)
        res_im = client.get("/ingest/images")
        self.assertEqual(res_im.status_code, 200)
        res_au = client.get("/ingest/audio")
        self.assertEqual(res_au.status_code, 200)
        print("  [PASS] Test 14: All FastAPI REST endpoints verified.")

if __name__ == "__main__":
    unittest.main()
