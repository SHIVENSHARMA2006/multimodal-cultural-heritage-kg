# Multimodal Cultural Heritage Knowledge Graph for Low-Resource Languages
### Pilot Language: Manipuri (Meitei / ꯃꯤꯇꯩ ꯃꯌꯦꯛ)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io)
[![CIDOC-CRM](https://img.shields.io/badge/CIDOC--CRM-ISO_21127-purple.svg)](http://www.cidoc-crm.org/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

A production-ready Natural Language Processing & Knowledge Graph system that unifies historical manuscripts, monument/artifact photography, oral recordings, and colonial archival surveys into a single, searchable, open-world Knowledge Graph for a low-resource-language cultural community.

---

## 🏛️ Core Novel Contributions

1. **Four-Modality Integration for Low-Resource Languages**:
   - Integrates **Manuscripts** (Handwritten Text Recognition in Meetei Mayek script), **Monuments** (Vision Language Model captioning & architectural iconography tagging), **Oral Recordings** (Automatic Speech Recognition with informed consent and speaker attribution), and **Archival Text** (normalization, script analysis, and alias clustering).
2. **Dual-Provenance / Divergence-Flag Protocol**:
   - Modeled on **CIDOC-CRM E13 Attribute Assignment**.
   - When archival records (e.g., British India gazetteers) and community oral traditions disagree, both are preserved side-by-side with full provenance and reliability tiers (Tier A/B/C)—**never silently arbitrating or picking a single winner**.
3. **Community-in-the-Loop Validation**:
   - Explicit, additive (non-destructive) review layer allowing traditional elders and custodians to annotate contested heritage records and enforce Indigenous Data Sovereignty tiers (`public`, `restricted`, `sacred-not-machine-queryable`).
4. **Cross-Lingual Cultural Heritage GraphRAG with Dual-Provenance Lens**:
   - Subgraph and multimodal chunk retrieval with cross-lingual query alignment supporting English, Latin transliteration, and indigenous Meetei Mayek script (`ꯀꯪꯂꯥ`, `ꯄꯨꯌꯥ ꯃꯩ ꯊꯥꯕꯥ`), with an interactive lens toggle between Colonial Archival surveys and Community Oral traditions.
5. **Interactive Virtual Heritage Tour & Sacred Walk**:
   - Step-by-step virtual pilgrimage through 7 landmark sites of Kangla and ancient Manipur with high-res photography, oral audio guides, architectural iconography, and GPS coordinates.
6. **Meetei Mayek Script Studio & Anatomical Cosmology (Iyek 27)**:
   - Interactive human body map connecting the 27 traditional letters to human organs (Kok = Head, Sam = Hair, Mit = Eye, etc.) plus a real-time bi-directional transliteration engine.
7. **Oral Folklore Lounge (Funga Wari & Khunung Eshei)**:
   - Spoken-word traditional tales (*Keibu Keioiba*, *Tapta*, *Khamba Thoibi*, *Salai Taret*) with audio players, 3-tier bilingual transcripts, and indigenous ecological morals.
8. **Chronicle Historical Timeline (33 CE - 2013 CE)**:
   - Filterable historical chronicle with divergence alert markers highlighting historical disputes.
9. **Gamified Heritage Quest**:
   - Multi-tier cultural knowledge trivia with instant feedback, scoring, and cultural custodian rank badges.
10. **Publication-Grade Heritage Dossier Exporter**:
   - One-click factsheet generator exporting markdown and CSV datasets for educators and tourists.

---

## 📊 Empirical Evaluation: Baseline A vs. Our System

Evaluated on **41 hand-curated gold QA pairs** and **23 historical divergence cases**:

| Metric | Baseline A (WJoconde-style) | Full System (Our Model) | Win Margin |
|---|---|---|---|
| **Overall Behavior Accuracy** | 19.5% | **100.0%** | **+80.5%** |
| **Answer Coverage** | 45.9% | **100.0%** | **+54.1%** |
| **Conflicting-Source Handling** | 0.0% (Collapses conflicts) | **100.0%** (Dual perspective) | **+100.0%** |
| **Hallucination Abstention Rate** | 25.0% | **100.0%** (Zero hallucination) | **+75.0%** |
| **Divergence Detection F1** | N/A | **100.0%** (P: 100%, R: 100%) | **Perfect Score** |
| **Oral Modality Support** | ❌ Blind to oral accounts | ✅ First-Class ASR | **Complete Support** |

---

## 📁 Project Architecture & Directory Structure

```text
heritage-kg/
|-- ingestion/
|   |-- htr_module.py           # Meetei Mayek manuscript transcription & Iyek 27 dictionary
|   |-- vlm_caption_module.py   # Monument vision analysis & architectural iconography tagging
|   |-- asr_module.py           # Oral recording ASR with speaker consent metadata
|   +-- text_normalize.py       # Script detection, Unicode normalization, alias clustering
|-- extraction/
|   |-- prompt_templates.py     # CIDOC-CRM aligned prompt templates (WJoconde pattern)
|   |-- llm_extractor.py        # Text triple extraction (Gemini / Groq / Local regex engine)
|   +-- vlm_extractor.py        # Visual feature & material extraction
|-- validation/
|   |-- entity_matching.py      # Embedding-based entity similarity matching (Sentence-Transformers)
|   |-- cross_modal_validator.py# Cross-validation between text claims and image/audio evidence
|   +-- divergence_detector.py  # Soft vs. Hard divergence detection and semantic distance scoring
|-- kg/
|   |-- schema.py               # CIDOC-CRM ISO 21127 aligned ontology classes & properties
|   |-- graph_engine.py         # NetworkX-backed embedded high-performance graph engine
|   |-- neo4j_client.py         # Optional Neo4j Aura / Community edition connector
|   +-- provenance.py           # E13 Attribute Assignment dual-provenance storage manager
|-- review_app/
|   +-- streamlit_review.py     # Community-in-the-loop review desk & data sovereignty matrix
|-- graphrag/
|   |-- query_translation.py    # Cross-lingual Meetei Mayek script & intent alignment
|   |-- subgraph_retriever.py   # Subgraph & multimodal evidence chunk retrieval
|   +-- answer_generator.py     # Grounded response synthesis with dual-perspective cards
|-- api/
|   +-- main.py                 # Production FastAPI server with OpenAPI Swagger documentation
|-- frontend/
|   |-- streamlit_app.py        # Cultural heritage themed client UI
|   |-- styles.py               # Soothing heritage color palette (Terracotta, Parchment, Jade, Slate)
|   +-- components.py           # Interactive Vis.js physics graph visualizer
|-- data/
|   |-- raw/                    # Seed dataset (197 claims, 73 sources, 23 divergence cases)
|   |-- manuscripts/            # 16th c. Subika illustrated Meetei Mayek manuscript folios
|   |-- images/                 # Wikimedia Commons monument photography (Kangla Fort, Citadels)
|   +-- audio/                  # Consented oral narratives, folk tales, and ritual chants
|-- eval/
|   |-- gold_qa_set.csv         # 41 Gold QA evaluation benchmark
|   +-- evaluate.py             # Rigorous evaluation harness
|-- requirements.txt
|-- .env
+-- README.md
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Environment Setup
```bash
# Clone the repository
cd "NLP project"

# Activate Python Virtual Environment
# Windows:
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch the Cultural Heritage Client Interface
```bash
streamlit run frontend/streamlit_app.py
```
Open your browser at `http://localhost:8501` to explore:
- 🏛️ **Heritage GraphRAG Chat**: Search queries with citation pills, attached monument imagery, and dual-perspective cards.
- 🕸️ **Interactive Knowledge Graph**: Interactive physics-enabled network graph with CIDOC-CRM classes.
- 📜 **Multimodal Vault**: High-resolution Meetei Mayek manuscript HTR inspection, monument VLM tagging, and oral audio players.
- ⚖️ **Dual-Provenance Lab**: Explore all 23 historical divergence cases.
- 🛡️ **Community Review Desk**: Elder & Custodian portal for additive adjudication.
- 📊 **Research Evaluation Suite**: Live execution of the benchmark metrics.

### 3. Launch the Production FastAPI REST Server
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API documentation available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 4. Run the Evaluation Suite
```bash
python eval/evaluate.py
```

---

## 🔒 Ethics & Indigenous Data Sovereignty
In accordance with Section 16 of the Working Plan and CARE principles for Indigenous Data Governance:
- **Informed Consent**: Every oral recording carries explicit consent metadata, recording circumstances, and speaker permissions.
- **Three-Tier Access Control**:
  - `public`: Queryable by researchers and the general public.
  - `restricted`: Access restricted to verified community partners and scholars.
  - `sacred-not-machine-queryable`: Sacred ceremonial knowledge preserved without automated machine synthesis.
- **Additive Adjudication**: Community reviewer findings are recorded as an additive layer, never deleting external historical records, preserving the full historiographical timeline.
