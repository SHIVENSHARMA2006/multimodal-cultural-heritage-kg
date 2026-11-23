"""
Evaluation Harness: Baseline-A vs. Full Multimodal Cultural Heritage GraphRAG.
Implements the formal evaluation protocol specified in Section 14 of the Working Plan.
Evaluates Answer Coverage, Conflicting-Source Handling, Divergence Precision/Recall,
and Grounding/Abstention rates against gold_qa_set.csv and divergence_cases.csv.
"""
import os
import sys
import csv
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from typing import Dict, List, Any, Tuple

from kg.graph_engine import HeritageGraphEngine
from graphrag.query_translation import QueryTranslator
from graphrag.subgraph_retriever import SubgraphRetriever
from graphrag.answer_generator import AnswerGenerator
from validation.divergence_detector import DivergenceDetector

class BaselineASystem:
    """
    Baseline A (WJoconde-style):
    - Restricted to text + image only (ignores oral/audio modality).
    - Single-provenance: when conflicts occur, silently collapses to one triple.
    - Generic keyword/string matching rather than CIDOC-CRM GraphRAG.
    """
    def __init__(self, engine: HeritageGraphEngine):
        self.engine = engine

    def query(self, question: str) -> Dict[str, Any]:
        q_lower = question.lower()
        
        # Oral-only queries are invisible to Baseline A
        if any(w in q_lower for w in ["oral", "speech", "indicvoices", "elder", "audio"]):
            # Either hallucinate or fail
            return {
                "answer": "Unknown or speculative answer.",
                "behavior": "hallucination_or_fail",
                "surfaced_multiple": False,
                "modalities_used": ["text"]
            }

        # Collapses conflicting claims to a single random/first claim
        matched_ent = None
        for eid, ent in self.engine.entities.items():
            if ent.canonical_name.lower() in q_lower:
                matched_ent = ent
                break

        if not matched_ent:
            return {
                "answer": "Not found in index.",
                "behavior": "abstain",
                "surfaced_multiple": False,
                "modalities_used": []
            }

        # Single provenance: just return the first claim blindly
        for rel, assigns in matched_ent.attributes.items():
            for a in assigns:
                if a.evidence_modality.value in ["text", "image_vlm"]:
                    return {
                        "answer": a.claim_value_normalized,
                        "behavior": "answer_single",
                        "surfaced_multiple": False,
                        "modalities_used": [a.evidence_modality.value]
                    }

        return {
            "answer": "No visual or text record.",
            "behavior": "abstain",
            "surfaced_multiple": False,
            "modalities_used": []
        }

class HeritageEvaluator:
    def __init__(self, data_dir: str = "data/raw", eval_dir: str = "eval"):
        self.data_dir = data_dir
        self.eval_dir = eval_dir
        self.engine = HeritageGraphEngine(data_dir=data_dir)
        self.translator = QueryTranslator(self.engine)
        self.retriever = SubgraphRetriever(self.engine)
        self.generator = AnswerGenerator()
        self.baseline = BaselineASystem(self.engine)
        self.divergence_detector = DivergenceDetector()

    def run_gold_qa_evaluation(self) -> Dict[str, Any]:
        qa_file = os.path.join(self.eval_dir, "gold_qa_set.csv")
        if not os.path.exists(qa_file):
            qa_file = os.path.join(self.data_dir, "gold_qa_set.csv")

        questions = []
        with open(qa_file, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                questions.append(row)

        full_system_results = []
        baseline_results = []

        # Counters
        stats = {
            "total_questions": len(questions),
            "full_system": {
                "correct_behavior": 0,
                "coverage": 0,
                "conflict_surfaced": 0,
                "abstain_correct": 0
            },
            "baseline_a": {
                "correct_behavior": 0,
                "coverage": 0,
                "conflict_surfaced": 0,
                "abstain_correct": 0
            }
        }

        conflict_questions_count = sum(1 for q in questions if q.get("expected_behavior") == "present_all_perspectives")
        abstain_questions_count = sum(1 for q in questions if q.get("expected_behavior") == "abstain_not_in_kg")

        for q in questions:
            qid = q.get("qa_id")
            q_text = q.get("question")
            expected_behavior = q.get("expected_behavior", "answer")

            # 1. Run Full System
            q_trans = self.translator.process_query(q_text)
            ent = q_trans.get("primary_entity")
            if ent:
                ctx = self.retriever.retrieve_context(ent, relation_hint=q_trans.get("detected_relation"))
                ans = self.generator.generate_answer(q_text, ctx, detected_relation=q_trans.get("detected_relation"))
            else:
                ctx = {"entity": None, "assignments": []}
                ans = self.generator.generate_answer(q_text, ctx)

            sys_behavior = ans.get("behavior")
            if sys_behavior == expected_behavior:
                stats["full_system"]["correct_behavior"] += 1
            if sys_behavior in ["answer", "present_all_perspectives"]:
                stats["full_system"]["coverage"] += 1
            if expected_behavior == "present_all_perspectives" and sys_behavior == "present_all_perspectives":
                stats["full_system"]["conflict_surfaced"] += 1
            if expected_behavior == "abstain_not_in_kg" and sys_behavior == "abstain_not_in_kg":
                stats["full_system"]["abstain_correct"] += 1

            full_system_results.append({
                "qa_id": qid,
                "question": q_text,
                "expected": expected_behavior,
                "actual": sys_behavior,
                "perspectives_count": len(ans.get("perspectives", []))
            })

            # 2. Run Baseline A
            b_ans = self.baseline.query(q_text)
            b_behavior = b_ans.get("behavior")

            # Baseline A collapses all conflicts to single answers
            if expected_behavior == "present_all_perspectives":
                # Baseline fails by asserting a single winner
                b_match = False
            elif expected_behavior == "abstain_not_in_kg":
                b_match = (b_behavior == "abstain")
            else:
                b_match = (b_behavior == "answer_single")

            if b_match:
                stats["baseline_a"]["correct_behavior"] += 1
            if b_behavior == "answer_single":
                stats["baseline_a"]["coverage"] += 1
            if expected_behavior == "abstain_not_in_kg" and b_behavior == "abstain":
                stats["baseline_a"]["abstain_correct"] += 1

            baseline_results.append({
                "qa_id": qid,
                "actual": b_behavior,
                "surfaced_multiple": b_ans.get("surfaced_multiple", False)
            })

        total = stats["total_questions"]
        return {
            "total_questions": total,
            "conflict_count": conflict_questions_count,
            "abstain_count": abstain_questions_count,
            "full_system": {
                "behavior_accuracy": round((stats["full_system"]["correct_behavior"] / total) * 100, 1),
                "answer_coverage": round((stats["full_system"]["coverage"] / (total - abstain_questions_count)) * 100, 1),
                "conflict_handling_rate": round((stats["full_system"]["conflict_surfaced"] / conflict_questions_count) * 100, 1) if conflict_questions_count else 100.0,
                "hallucination_abstention_rate": round((stats["full_system"]["abstain_correct"] / abstain_questions_count) * 100, 1) if abstain_questions_count else 100.0
            },
            "baseline_a": {
                "behavior_accuracy": round((stats["baseline_a"]["correct_behavior"] / total) * 100, 1),
                "answer_coverage": round((stats["baseline_a"]["coverage"] / (total - abstain_questions_count)) * 100, 1),
                "conflict_handling_rate": 0.0,  # Baseline A silently collapses all conflicts
                "hallucination_abstention_rate": round((stats["baseline_a"]["abstain_correct"] / abstain_questions_count) * 100, 1) if abstain_questions_count else 50.0
            },
            "sample_comparisons": full_system_results[:10]
        }

    def run_divergence_benchmark(self) -> Dict[str, Any]:
        """
        Evaluates the Divergence Detector against all 23 divergence cases in divergence_cases.csv.
        """
        cases_file = os.path.join(self.data_dir, "divergence_cases.csv")
        cases = []
        with open(cases_file, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cases.append(row)

        tp, fp, tn, fn = 0, 0, 0, 0
        details = []

        for c in cases:
            gid = c.get("group_id")
            expected_grade = c.get("grade", "none").strip().lower()
            is_conflict_gold = (expected_grade in ["hard", "soft"])

            # Find registered group in engine
            reg = self.engine.provenance.get_divergence_info(gid)
            pred_grade = reg.get("grade").value if reg else "none"
            is_conflict_pred = (pred_grade in ["hard", "soft"])

            if is_conflict_gold and is_conflict_pred:
                tp += 1
            elif not is_conflict_gold and is_conflict_pred:
                fp += 1
            elif not is_conflict_gold and not is_conflict_pred:
                tn += 1
            else:
                fn += 1

            details.append({
                "group_id": gid,
                "entity": c.get("entity_name"),
                "relation": c.get("relation"),
                "gold_grade": expected_grade,
                "predicted_grade": pred_grade,
                "correct": (expected_grade == pred_grade)
            })

        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 1.0

        return {
            "total_cases": len(cases),
            "precision": round(precision * 100, 1),
            "recall": round(recall * 100, 1),
            "f1_score": round(f1 * 100, 1),
            "true_positives": tp,
            "false_positives": fp,
            "true_negatives": tn,
            "false_negatives": fn,
            "case_details": details
        }

if __name__ == "__main__":
    evaluator = HeritageEvaluator()
    print("Running Gold QA Benchmark...")
    qa_results = evaluator.run_gold_qa_evaluation()
    print("QA Benchmark Results:", json.dumps(qa_results, indent=2))
    print("\nRunning Divergence Detection Benchmark...")
    div_results = evaluator.run_divergence_benchmark()
    print("Divergence Benchmark Results:", json.dumps(div_results, indent=2))
