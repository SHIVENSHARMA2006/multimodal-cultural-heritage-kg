"""
Production-Ready FastAPI Server for Multimodal Cultural Heritage Knowledge Graph.
Exposes RESTful endpoints for Cross-Lingual GraphRAG queries, Subgraph Retrieval,
Multimodal Ingestion (HTR, VLM, ASR), Community Review, and Benchmark Evaluation.
"""
import os
import sys
# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

from kg.graph_engine import HeritageGraphEngine
from kg.schema import CommunityAnnotation, AccessLevel
from graphrag.query_translation import QueryTranslator
from graphrag.subgraph_retriever import SubgraphRetriever
from graphrag.answer_generator import AnswerGenerator
from ingestion.htr_module import ManuscriptHTRModule
from ingestion.vlm_caption_module import VLMCaptionModule
from ingestion.asr_module import SpeechASRModule
from eval.evaluate import HeritageEvaluator

app = FastAPI(
    title="Multimodal Cultural Heritage Knowledge Graph API",
    description="Production-grade API for Low-Resource Cultural Heritage (Pilot: Manipuri/Meitei) featuring Dual-Provenance GraphRAG and Community Sovereignty.",
    version="1.0.0"
)

# Enable CORS for cross-origin client apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Singleton service instances
engine = HeritageGraphEngine()
translator = QueryTranslator(engine)
retriever = SubgraphRetriever(engine)
generator = AnswerGenerator()
htr_module = ManuscriptHTRModule()
vlm_module = VLMCaptionModule()
asr_module = SpeechASRModule()

# Request/Response Models
class QueryRequest(BaseModel):
    query: str = Field(..., example="When was Kangla established?")
    language: Optional[str] = Field("en", example="en")

class CommunityReviewRequest(BaseModel):
    entity_id: str = Field(..., example="E001")
    divergence_group_id: str = Field(..., example="D01")
    reviewer_name: str = Field(..., example="Elder N. Ningthouja")
    reviewer_role: str = Field(..., example="Cultural Custodian")
    adjudication_text: str = Field(..., example="Traditional oral memory confirms the pre-Christian sacred origins of Kangla as spiritual center.")
    access_tier: Optional[str] = Field("public", example="public")
    consent_given: Optional[bool] = Field(True, example=True)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "Multimodal Cultural Heritage KG",
        "version": "1.0.0",
        "pilot_language": "Manipuri (Meitei / Meetei Mayek)"
    }

@app.get("/stats", tags=["System"])
def get_graph_statistics():
    return engine.get_statistics()

@app.post("/query", tags=["GraphRAG"])
def query_graphrag(request: QueryRequest):
    """
    Executes cross-lingual Multimodal GraphRAG query with dual-provenance divergence handling.
    """
    q_trans = translator.process_query(request.query)
    ent = q_trans.get("primary_entity")

    if not ent:
        ctx = {"entity": None, "assignments": []}
        ans = generator.generate_answer(request.query, ctx)
    else:
        ctx = retriever.retrieve_context(ent, relation_hint=q_trans.get("detected_relation"))
        ans = generator.generate_answer(request.query, ctx, detected_relation=q_trans.get("detected_relation"))

    return {
        "query": request.query,
        "script": q_trans.get("detected_script"),
        "primary_entity": ent.canonical_name if ent else None,
        "meitei_name": ent.name_meitei_script if ent else None,
        "detected_relation": q_trans.get("detected_relation"),
        "behavior": ans.get("behavior"),
        "answer_text": ans.get("answer_text"),
        "confidence": ans.get("confidence"),
        "perspectives": ans.get("perspectives", []),
        "citations": ans.get("citations", []),
        "attached_media": ans.get("attached_media", [])
    }

@app.get("/entities", tags=["Knowledge Graph"])
def search_entities(q: str = Query("", description="Search term in English or Meetei Mayek")):
    results = engine.search_entities(q, limit=20)
    return [
        {
            "entity_id": e.entity_id,
            "canonical_name": e.canonical_name,
            "meitei_script": e.name_meitei_script,
            "cidoc_class": e.cidoc_class.value,
            "type": e.entity_type,
            "aliases": e.aliases,
            "has_divergence": e.has_divergence()
        }
        for e in results
    ]

@app.get("/subgraph/{entity_id}", tags=["Knowledge Graph"])
def get_entity_subgraph(entity_id: str, depth: int = Query(1, ge=1, le=2)):
    subgraph = engine.get_subgraph(entity_id, depth=depth)
    return subgraph

@app.get("/divergences", tags=["Dual-Provenance"])
def list_divergence_cases():
    return engine.provenance.divergence_registry

@app.post("/review", tags=["Community-in-the-Loop"])
def submit_community_review(review: CommunityReviewRequest):
    """
    Submits an additive community review annotation without overwriting archival records.
    """
    import datetime
    annotation = CommunityAnnotation(
        annotation_id=f"ANN_{review.divergence_group_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M')}",
        entity_id=review.entity_id,
        divergence_group_id=review.divergence_group_id,
        reviewer_name=review.reviewer_name,
        reviewer_role=review.reviewer_role,
        adjudication_text=review.adjudication_text,
        recommended_weight=1.0,
        data_sovereignty_consent=review.consent_given or True,
        access_level_recommendation=AccessLevel(review.access_tier or "public")
    )
    engine.provenance.add_community_annotation(annotation)
    return {
        "status": "success",
        "message": f"Additive community annotation registered for {review.entity_id}.",
        "annotation_id": annotation.annotation_id
    }

@app.get("/ingest/manuscripts", tags=["Multimodal Ingestion"])
def list_manuscript_scans():
    return htr_module.catalog

@app.post("/ingest/htr", tags=["Multimodal Ingestion"])
def transcribe_manuscript(image_path: str = Query(..., description="Path to manuscript image file")):
    return htr_module.transcribe_manuscript(image_path)

@app.get("/ingest/images", tags=["Multimodal Ingestion"])
def list_monument_images():
    return vlm_module.catalog

@app.post("/ingest/vlm", tags=["Multimodal Ingestion"])
def analyze_monument_image(image_path: str = Query(..., description="Path to monument image file")):
    return vlm_module.analyze_image(image_path)

@app.get("/ingest/audio", tags=["Multimodal Ingestion"])
def list_oral_recordings():
    return asr_module.manifest

@app.post("/ingest/asr", tags=["Multimodal Ingestion"])
def transcribe_oral_audio(audio_path: str = Query(..., description="Path to audio recording")):
    return asr_module.transcribe_audio(audio_path)

@app.get("/eval/benchmark", tags=["Research Benchmark"])
def run_benchmark():
    evaluator = HeritageEvaluator(data_dir="data/raw", eval_dir="eval")
    qa_results = evaluator.run_gold_qa_evaluation()
    div_results = evaluator.run_divergence_benchmark()
    return {
        "qa_benchmark": qa_results,
        "divergence_benchmark": div_results
    }

@app.get("/download/report.docx", tags=["Project Report"])
def download_word_report():
    docx_path = os.path.abspath("Multimodal_Cultural_Heritage_NLP_Project_Report.docx")
    if not os.path.exists(docx_path):
        raise HTTPException(status_code=404, detail="Word report document not found.")
    return FileResponse(
        docx_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="Multimodal_Cultural_Heritage_NLP_Project_Report.docx"
    )

@app.get("/download/report.pdf", tags=["Project Report"])
def download_pdf_report():
    pdf_path = os.path.abspath("Multimodal_Cultural_Heritage_NLP_Project_Report.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF report document not found.")
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="Multimodal_Cultural_Heritage_NLP_Project_Report.pdf"
    )

@app.get("/download/report.html", tags=["Project Report"])
def download_html_report():
    html_path = os.path.abspath("report_view.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="HTML report document not found.")
    return FileResponse(
        html_path,
        media_type="text/html",
        filename="Multimodal_Cultural_Heritage_NLP_Project_Report.html"
    )

@app.get("/report", tags=["Project Report"], response_class=HTMLResponse)
def view_html_report():
    html_path = os.path.abspath("report_view.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="HTML report not found.")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)
