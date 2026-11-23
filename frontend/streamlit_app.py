"""
Cultural Heritage Knowledge Graph Explorer & Client Application.
Streamlit production interface with soothing cultural heritage design,
cross-lingual GraphRAG, interactive graph visualization, multimodal vault,
dual-provenance lab, community review desk, and live research evaluation.
Includes interactive Virtual Heritage Tour, Meetei Mayek Studio, Oral Folklore Lounge,
Historical Chronicle Timeline, Gamified Heritage Quest, and Cultural Dossier Exporter.
"""
import os
import sys
# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image

from frontend.styles import HERITAGE_CSS
from frontend.components import render_visjs_subgraph
from frontend.heritage_data import (
    HERITAGE_WALKING_TOUR,
    MEETEI_MAYEK_ANATOMY,
    TRANSLITERATION_LEXICON,
    transliterate_text,
    ORAL_FOLKLORE_STORIES,
    HISTORICAL_TIMELINE,
    HERITAGE_QUIZ_QUESTIONS
)
from kg.graph_engine import HeritageGraphEngine
from kg.schema import DivergenceGrade, EvidenceModality
from graphrag.query_translation import QueryTranslator
from graphrag.subgraph_retriever import SubgraphRetriever
from graphrag.answer_generator import AnswerGenerator
from ingestion.htr_module import ManuscriptHTRModule, MEETEI_MAYEK_ALPHABET
from ingestion.vlm_caption_module import VLMCaptionModule
from ingestion.asr_module import SpeechASRModule
from review_app.streamlit_review import render_review_interface
from eval.evaluate import HeritageEvaluator

# Streamlit Page Configuration
st.set_page_config(
    page_title="Manipuri Cultural Heritage Knowledge Graph",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Cultural Heritage Styling
st.markdown(HERITAGE_CSS, unsafe_allow_html=True)

# Cache graph engine & models to ensure lightning-fast UI responsiveness
@st.cache_resource
def load_heritage_services():
    engine = HeritageGraphEngine()
    translator = QueryTranslator(engine)
    retriever = SubgraphRetriever(engine)
    generator = AnswerGenerator()
    htr = ManuscriptHTRModule()
    vlm = VLMCaptionModule()
    asr = SpeechASRModule()
    return engine, translator, retriever, generator, htr, vlm, asr

engine, translator, retriever, generator, htr_module, vlm_module, asr_module = load_heritage_services()

# Sidebar Navigation with Cultural Aesthetics
with st.sidebar:
    st.html(
        '<div style="text-align: center; padding: 0.5rem 0 1.2rem 0;">'
        '<span style="font-size: 2.4rem;">🏛️</span>'
        '<h3 style="font-family: \'Cinzel\', serif; margin: 0.3rem 0 0 0; color: #FAF7F2;">Kangleipak Heritage</h3>'
        '<span style="font-size: 0.85rem; color: #E2B653; font-weight: 600;">ꯃꯅꯤꯄꯨꯔ ꯂꯥꯏꯔꯤꯛ ꯈꯣꯝꯖꯤꯟꯕꯥ</span>'
        '</div>'
    )

    nav_choice = st.radio(
        "Navigate Application:",
        [
            "🏛️ Heritage GraphRAG Explorer",
            "🗺️ Virtual Heritage Tour (Kangla Walk)",
            "🔤 Meetei Mayek Studio (Anatomy & Translit)",
            "📜 Oral Folklore & Stories (Funga Wari)",
            "⏳ Chronicle Historical Timeline",
            "🎮 Heritage Quest & Trivia Challenge",
            "🕸️ Interactive Knowledge Graph",
            "🏺 Multimodal Heritage Vault",
            "⚖️ Dual-Provenance & Divergence Lab",
            "📑 Cultural Dossier Export Studio",
            "🛡️ Community Review Desk",
            "📊 Benchmark & Research Evaluation",
            "📄 Academic Project Report & Downloads"
        ]
    )

    st.markdown("---")
    stats = engine.get_statistics()
    st.markdown("### 📈 Graph Metrics")
    st.markdown(f"**Entities**: `{stats['total_entities']}`")
    st.markdown(f"**Attributed Claims**: `{stats['total_claims']}`")
    st.markdown(f"**Divergence Groups**: `{stats['divergence_groups']}`")
    st.markdown(f"**Verified Sources**: `{stats['total_sources']}`")
    
    st.markdown("---")
    st.markdown("### 📥 Download Documents")
    docx_file = "Multimodal_Cultural_Heritage_NLP_Project_Report.docx"
    pdf_file = "Multimodal_Cultural_Heritage_NLP_Project_Report.pdf"
    bp_docx = "Comprehensive_System_Architecture_and_Engineering_Blueprint.docx"
    bp_pdf = "Comprehensive_System_Architecture_and_Engineering_Blueprint.pdf"
    
    if os.path.exists(docx_file):
        with open(docx_file, "rb") as f:
            st.download_button(
                label="📥 Academic Report (.docx)",
                data=f.read(),
                file_name=docx_file,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
    if os.path.exists(bp_docx):
        with open(bp_docx, "rb") as f:
            st.download_button(
                label="📐 Engineering Blueprint (.docx)",
                data=f.read(),
                file_name=bp_docx,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
    if os.path.exists(bp_pdf):
        with open(bp_pdf, "rb") as f:
            st.download_button(
                label="📄 Engineering Blueprint (.pdf)",
                data=f.read(),
                file_name=bp_pdf,
                mime="application/pdf",
                use_container_width=True
            )
    
    st.markdown("---")
    st.html("<small style='color: #CBD5E1;'>Pilot Language: <b style='color:#FAF7F2;'>Manipuri (Meitei)</b><br>Schema: <b style='color:#FAF7F2;'>CIDOC-CRM (ISO 21127)</b><br><span style='color:#D4A373;'>Indigenous Data Sovereignty enabled.</span></small>")

# Top Banner
st.html(
    '<div class="heritage-header">'
    '<div class="heritage-title">Multimodal Cultural Heritage Knowledge Graph</div>'
    '<div class="heritage-subtitle">Preserving Indigenous Knowledge & Historical Memory with Dual-Provenance GraphRAG</div>'
    '<div class="heritage-desc">'
    'A pilot system unifying manuscripts, monument photography, oral recordings, and colonial archival surveys. '
    'Featuring <b>E13 Attribute Assignment</b> dual-provenance conflict handling, preventing silent arbitration between external archival records and community oral traditions.'
    '</div>'
    '</div>'
)

# -------------------------------------------------------------
# TAB 1: HERITAGE GRAPHRAG EXPLORER & CHAT
# -------------------------------------------------------------
if nav_choice == "🏛️ Heritage GraphRAG Explorer":
    st.markdown("### 🏛️ Multimodal GraphRAG Discovery")
    st.markdown("Query the verified cultural heritage knowledge graph across languages (English, Meetei Mayek script `ꯀꯪꯂꯥ`, or transliteration).")

    # Perspective Lens Selector
    lens_col1, lens_col2 = st.columns([2, 1])
    with lens_col1:
        perspective_lens = st.radio(
            "Dual-Provenance Perspective Lens:",
            ["🌐 Unified / Reconciled View", "🏛️ Colonial Archival Survey Focus", "🪶 Community Oral Memory Focus"],
            horizontal=True,
            help="Switch lenses to experience how history is viewed through external colonial gazetteers vs. indigenous oral memory."
        )

    # Sample query prompts
    sample_queries = [
        "When was Kangla established?",
        "What does the name 'Kangla' mean in old Meetei?",
        "When were the Puyas burned?",
        "In which year was Sankirtana inscribed on UNESCO ICH?",
        "How many letters does Meitei Mayek have?",
        "Who manages Kangla Fort today?",
        "Which is the world's oldest polo ground?",
        "Who designed the 2006 Kangla Sha statues?"
    ]
    
    st.markdown("**Sample Research Inquiries:**")
    prompt_cols = st.columns(4)
    selected_prompt = None
    for i, sq in enumerate(sample_queries):
        col_idx = i % 4
        with prompt_cols[col_idx]:
            if st.button(sq, key=f"sq_{i}", use_container_width=True):
                selected_prompt = sq

    # Query Input
    query_text = st.text_input(
        "Enter heritage question or Meetei Mayek entity:",
        value=selected_prompt or "When was Kangla established?",
        placeholder="e.g., When was Kangla established? or ꯀꯪꯂꯥ"
    )

    if query_text:
        with st.spinner("Executing Cross-Lingual Multimodal GraphRAG..."):
            # 1. Translate Query
            q_trans = translator.process_query(query_text)
            ent = q_trans.get("primary_entity")
            
            # 2. Retrieve Subgraph Context & Multimodal chunks
            if ent:
                ctx = retriever.retrieve_context(ent, relation_hint=q_trans.get("detected_relation"))
                ans = generator.generate_answer(query_text, ctx, detected_relation=q_trans.get("detected_relation"))
            else:
                ctx = {"entity": None, "assignments": []}
                ans = generator.generate_answer(query_text, ctx)

        # Query metadata chips
        chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)
        with chip_col1:
            st.metric("Detected Script", q_trans.get("detected_script", "en").title())
        with chip_col2:
            st.metric("Primary Entity", ent.canonical_name if ent else "None Found")
        with chip_col3:
            st.metric("Query Behavior", ans.get("behavior", "answer").replace("_", " ").title())
        with chip_col4:
            st.metric("Confidence", f"{int(ans.get('confidence', 0.95)*100)}%")

        st.markdown("---")

        # Answer Rendering
        if ans.get("behavior") == "present_all_perspectives":
            alert_html = (
                '<div style="background: #FFFBEB; border-left: 5px solid #F59E0B; padding: 1.2rem; border-radius: 8px; margin-bottom: 1.5rem;">'
                '<h4 style="margin: 0; color: #92400E; font-family: \'Cinzel\', serif;">⚖️ Dual-Provenance Historical Divergence Alert</h4>'
                '<p style="margin: 0.4rem 0 0 0; color: #78350F; font-size: 0.95rem;">'
                'Archival colonial surveys and traditional community oral chronicles present differing accounts for this property. '
                'In accordance with the <b>Divergence-Flag Protocol</b>, the system presents all accounts side-by-side with full provenance attribution rather than silently asserting a single winner.'
                '</p>'
                '</div>'
            )
            st.html(alert_html)

            perspectives = ans.get("perspectives", [])
            if len(perspectives) >= 2:
                # Filter by lens if specific lens selected
                p_col1, p_col2 = st.columns(2)
                p1 = perspectives[0]
                p2 = perspectives[1]
                
                show_p1 = "Community" not in perspective_lens
                show_p2 = "Colonial" not in perspective_lens

                with p_col1:
                    p1_html = (
                        f'<div class="perspective-card perspective-a" style="opacity: {1.0 if show_p1 else 0.4};">'
                        f'<span class="perspective-badge badge-a">Perspective A ({p1["modality"].upper()})</span>'
                        f'<h4 style="margin: 0 0 0.5rem 0; color: #C86D51;">{p1["value"]}</h4>'
                        f'<p style="font-style: italic; color: #334155; font-size: 0.95rem;">"{p1["text"]}"</p>'
                        f'<div style="margin-top: 1rem; font-size: 0.85rem; color: #64748B;">'
                        f'<b>Source:</b> <a href="{p1["source_url"]}" target="_blank">{p1["source_title"]}</a><br/>'
                        f'<b>Reliability:</b> Tier {p1["tier"]} | <b>Modality:</b> <code>{p1["modality"]}</code>'
                        f'</div>'
                        f'</div>'
                    )
                    st.html(p1_html)
                with p_col2:
                    p2_html = (
                        f'<div class="perspective-card perspective-b" style="opacity: {1.0 if show_p2 else 0.4};">'
                        f'<span class="perspective-badge badge-b">Perspective B ({p2["modality"].upper()})</span>'
                        f'<h4 style="margin: 0 0 0.5rem 0; color: #2D5A4C;">{p2["value"]}</h4>'
                        f'<p style="font-style: italic; color: #334155; font-size: 0.95rem;">"{p2["text"]}"</p>'
                        f'<div style="margin-top: 1rem; font-size: 0.85rem; color: #64748B;">'
                        f'<b>Source:</b> <a href="{p2["source_url"]}" target="_blank">{p2["source_title"]}</a><br/>'
                        f'<b>Reliability:</b> Tier {p2["tier"]} | <b>Modality:</b> <code>{p2["modality"]}</code>'
                        f'</div>'
                        f'</div>'
                    )
                    st.html(p2_html)
            else:
                st.markdown(ans.get("answer_text", ""))

        elif ans.get("behavior") == "abstain_not_in_kg":
            abstain_html = (
                f'<div style="background: #FEF2F2; border-left: 5px solid #EF4444; padding: 1.2rem; border-radius: 8px; margin-bottom: 1.5rem;">'
                f'<h4 style="margin: 0; color: #991B1B;">🛡️ Hallucination Safeguard / Verified Abstention</h4>'
                f'<p style="margin: 0.5rem 0 0 0; color: #7F1D1D;">{ans.get("answer_text")}</p>'
                f'</div>'
            )
            st.html(abstain_html)
        else:
            citations_html = ""
            for c in ans.get("citations", []):
                c_url = c.get("url") or "#"
                c_title = c.get("title") or "Historical Record"
                c_tier = c.get("tier") or "B"
                citations_html += (
                    f'<a href="{c_url}" target="_blank" class="citation-link-badge">'
                    f'<span>{c_title}</span>'
                    f'<span class="tier-badge">Tier {c_tier}</span>'
                    f'</a>'
                )

            meitei_pill = f'<span class="meitei-script-pill">{ans.get("meitei_script")}</span>' if ans.get('meitei_script') else ""
            entity_type = ans.get('entity_type', 'Heritage Entity')
            lead_answer = ans.get('synthesized_answer') or ans.get('answer_text') or ""
            
            lead_answer_html = lead_answer
            while "**" in lead_answer_html:
                lead_answer_html = lead_answer_html.replace("**", "<strong>", 1).replace("**", "</strong>", 1)

            quote_html = ""
            if ans.get("claim_quote"):
                q_text = ans.get("claim_quote")
                q_src_title = ans.get("source_title", "Archival Record")
                q_src_url = ans.get("source_url", "#")
                q_src_tier = ans.get("source_tier", "B")
                quote_html = (
                    f'<div class="evidence-quote-box">'
                    f'<div class="quote-glyph">“</div>'
                    f'<div style="flex: 1;">'
                    f'<p class="quote-body-text">{q_text}</p>'
                    f'<span class="quote-source-caption">— Source: <a href="{q_src_url}" target="_blank" style="color:#64748B;">{q_src_title}</a> (Reliability Tier {q_src_tier})</span>'
                    f'</div>'
                    f'</div>'
                )

            ent_display = ans.get('entity_name') or (ent.canonical_name if ent else 'Heritage Finding')
            
            citations_tray = ""
            if citations_html:
                citations_tray = (
                    f'<div class="citation-tray">'
                    f'<span class="citation-tray-label">Verified Sources:</span>'
                    f'{citations_html}'
                    f'</div>'
                )

            card_html = (
                f'<div class="heritage-answer-card">'
                f'<div class="answer-card-header">'
                f'<div class="entity-title-group">'
                f'<span class="entity-name-text">{ent_display}</span>'
                f'{meitei_pill}'
                f'<span class="entity-type-badge">{entity_type}</span>'
                f'</div>'
                f'<span class="verified-pill">✓ Verified Heritage Record</span>'
                f'</div>'
                f'<div class="answer-lead-box">'
                f'{lead_answer_html}'
                f'</div>'
                f'{quote_html}'
                f'{citations_tray}'
                f'</div>'
            )
            st.html(card_html)

        # Attached Multimodal Evidence Chunks
        attached_media = ans.get("attached_media", [])
        if attached_media:
            st.markdown("#### 🖼️ Attached Multimodal Evidence")
            media_cols = st.columns(min(len(attached_media), 3))
            for idx, m in enumerate(attached_media[:3]):
                with media_cols[idx]:
                    m_path = m["path"]
                    if m["modality"] == "image_vlm" and os.path.exists(m_path):
                        try:
                            img = Image.open(m_path)
                            st.image(img, caption=f"🏛️ {m['title']}", use_container_width=True)
                        except Exception:
                            st.write(m["title"])
                    elif m["modality"] == "manuscript_htr" and os.path.exists(m_path):
                        try:
                            img = Image.open(m_path)
                            st.image(img, caption=f"📜 {m['title']}", use_container_width=True)
                        except Exception:
                            st.write(m["title"])
                    elif m["modality"] == "audio_asr" and os.path.exists(m_path):
                        st.markdown(f"**🎙️ {m['title']}**")
                        st.audio(m_path)

        # Interactive Subgraph Inspector
        if ent:
            st.markdown("---")
            with st.expander(f"Inspect 1-Hop Subgraph for {ent.canonical_name}", expanded=False):
                sg = retriever.engine.get_subgraph(ent.entity_id, depth=1)
                html_vis = render_visjs_subgraph(sg, height=450)
                components.html(html_vis, height=480, scrolling=False)

# -------------------------------------------------------------
# TAB 2: VIRTUAL HERITAGE TOUR (KANGLA SACRED WALK)
# -------------------------------------------------------------
elif nav_choice == "🗺️ Virtual Heritage Tour (Kangla Walk)":
    st.markdown("### 🗺️ Kangla Sacred Walk: Virtual Heritage Trail")
    st.markdown("An interactive, step-by-step cultural pilgrimage through the sacred monuments, citadels, and holy lakes of ancient Kangleipak.")

    if "tour_idx" not in st.session_state:
        st.session_state["tour_idx"] = 0

    tour_len = len(HERITAGE_WALKING_TOUR)
    
    # Quick Waypoint Selector
    tour_titles = [f"{i+1}. {w['title']}" for i, w in enumerate(HERITAGE_WALKING_TOUR)]
    selected_stop = st.selectbox(
        "Jump to Pilgrimage Waypoint:",
        tour_titles,
        index=st.session_state["tour_idx"]
    )
    st.session_state["tour_idx"] = tour_titles.index(selected_stop)
    curr_stop = HERITAGE_WALKING_TOUR[st.session_state["tour_idx"]]

    # Progress bar
    prog = (st.session_state["tour_idx"] + 1) / tour_len
    st.progress(prog, text=f"Waypoint {st.session_state['tour_idx']+1} of {tour_len}: {curr_stop['title']}")

    # Waypoint Card Container
    tour_card_html = (
        f'<div class="tour-waypoint-card">'
        f'<div class="tour-header-row">'
        f'<div>'
        f'<span class="tour-step-pill">Stop {st.session_state["tour_idx"]+1} of {tour_len}</span>'
        f'<span class="entity-name-text" style="margin-left: 10px;">{curr_stop["title"]}</span>'
        f'<span class="meitei-script-pill" style="margin-left: 10px;">{curr_stop["title_mayek"]}</span>'
        f'</div>'
        f'<div>'
        f'<span class="tour-gps-pill">📍 {curr_stop["coordinates"]}</span>'
        f'<span class="entity-type-badge" style="margin-left: 8px;">{curr_stop["era"]}</span>'
        f'</div>'
        f'</div>'
        f'<div class="answer-lead-box" style="margin-bottom: 1rem;">'
        f'<b>Site Significance:</b> {curr_stop["summary"]}'
        f'</div>'
        f'</div>'
    )
    st.html(tour_card_html)

    # Two-Column Media & Chronicle Layout
    col_vis, col_chr = st.columns([1, 1])
    with col_vis:
        st.markdown("#### 📷 Site Photography & Architectural Iconography")
        if os.path.exists(curr_stop["image_path"]):
            img = Image.open(curr_stop["image_path"])
            st.image(img, caption=f"🏛️ {curr_stop['title']}", use_container_width=True)
        
        st.markdown("**Architectural Tags**:")
        tag_html = " ".join([f"<span class='entity-type-badge'>{t}</span>" for t in curr_stop["iconography_tags"]])
        st.html(f"<div style='margin-bottom: 1rem;'>{tag_html}</div>")

        st.markdown(f"**🎙️ Oral Audio Guide ({curr_stop['audio_caption']}):**")
        if os.path.exists(curr_stop["audio_path"]):
            st.audio(curr_stop["audio_path"])

    with col_chr:
        st.markdown("#### 📜 Historical Chronicle & Oral Memory")
        st.write(curr_stop["details"])

        oral_html = (
            f'<div class="tour-oral-tradition-box">'
            f'<b>🪶 Living Oral Tradition:</b><br/>'
            f'{curr_stop["oral_tradition"]}'
            f'</div>'
        )
        st.html(oral_html)

        div_html = (
            f'<div style="background: #FFFBEB; border-left: 4px solid #D97706; padding: 0.9rem 1.2rem; border-radius: 6px; font-size: 0.92rem; color: #78350F;">'
            f'<b>⚖️ Dual-Provenance Context:</b><br/>'
            f'{curr_stop["dual_provenance_note"]}'
            f'</div>'
        )
        st.html(div_html)

    # Stepper Buttons
    st.markdown("---")
    step_col1, step_col2, step_col3 = st.columns([1, 2, 1])
    with step_col1:
        if st.button("◀ Previous Waypoint", disabled=(st.session_state["tour_idx"] == 0), use_container_width=True):
            st.session_state["tour_idx"] -= 1
            st.rerun()
    with step_col3:
        if st.button("Next Waypoint ▶", disabled=(st.session_state["tour_idx"] == tour_len - 1), use_container_width=True):
            st.session_state["tour_idx"] += 1
            st.rerun()

# -------------------------------------------------------------
# TAB 3: MEETEI MAYEK STUDIO (ANATOMY & TRANSLIT)
# -------------------------------------------------------------
elif nav_choice == "🔤 Meetei Mayek Studio (Anatomy & Translit)":
    st.markdown("### 🔤 Meetei Mayek Script Studio & Anatomical Cosmology")
    st.markdown(
        "Meetei Mayek is an extraordinary indigenous writing system where every letter corresponds to an anatomical part of the human body (Iyek 27), "
        "reflecting ancient Meitei cosmological philosophy and deep reverence for human anatomy."
    )

    studio_tab1, studio_tab2 = st.tabs([
        "👤 Anatomical Body Map (Iyek 27)",
        "✍️ Live Bi-Directional Transliteration Lab"
    ])

    with studio_tab1:
        st.markdown("#### 👤 Cosmological Anatomy of the 18 Core Letters")
        st.markdown("Click or explore each letter to uncover its anatomical naming, phonetic sound, and traditional cosmological significance.")

        regions = ["All", "Head & Face", "Throat & Chest", "Torso & Spine", "Limbs & Surface", "Internal & Spiritual"]
        sel_region = st.selectbox("Filter by Anatomical Region:", regions)

        filtered_letters = MEETEI_MAYEK_ANATOMY
        if sel_region != "All":
            filtered_letters = [l for l in MEETEI_MAYEK_ANATOMY if l["region"] == sel_region]

        grid_cols = st.columns(3)
        for i, glyph in enumerate(filtered_letters):
            c_idx = i % 3
            with grid_cols[c_idx]:
                card_html = (
                    f'<div class="mayek-anatomy-card">'
                    f'<div class="mayek-char-display">{glyph["char"]}</div>'
                    f'<div style="font-weight: 700; font-size: 1.1rem; color: #18222F;">{glyph["name"]}</div>'
                    f'<span class="mayek-anatomy-badge">{glyph["body_part"]}</span> '
                    f'<span style="font-family: monospace; font-size: 0.85rem; color: #64748B;">{glyph["ipa"]}</span>'
                    f'<p style="font-size: 0.82rem; color: #475569; margin: 8px 0;">{glyph["meaning"]}</p>'
                    f'<div style="font-size: 0.78rem; color: #C86D51; font-weight: 600;">Ex: {glyph["example"]}</div>'
                    f'</div>'
                )
                st.html(card_html)

    with studio_tab2:
        st.markdown("#### ✍️ Live Meetei Mayek Transliteration Engine")
        st.markdown("Convert Romanized Manipuri or English terminology into standardized Meetei Mayek Unicode, 19th-century Bengali script comparison, and IPA phonetics.")

        # Quick prompt buttons
        st.markdown("**Quick Heritage Terms:**")
        quick_words = ["Kangleipak", "Kangla", "Ima Keithel", "Sankirtana", "Khamba Thoibi", "Lai Haraoba"]
        q_cols = st.columns(6)
        chosen_term = None
        for i, qw in enumerate(quick_words):
            with q_cols[i]:
                if st.button(qw, key=f"qw_{i}", use_container_width=True):
                    chosen_term = qw

        translit_input = st.text_input(
            "Enter Romanized Manipuri or English term:",
            value=chosen_term or "Kangleipak",
            placeholder="Type e.g., Kangleipak, Kangla, Sankirtana..."
        )

        if translit_input:
            tr_res = transliterate_text(translit_input)
            
            box_html = (
                f'<div class="mayek-translit-box">'
                f'<div style="font-size: 0.85rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Meetei Mayek Standard Unicode</div>'
                f'<div style="font-size: 3.5rem; font-family: \'Noto Sans Meetei Mayek\', sans-serif; font-weight: 700; color: #C86D51; margin: 0.5rem 0;">'
                f'{tr_res["mayek"]}'
                f'</div>'
                f'<div style="display: flex; gap: 20px; flex-wrap: wrap; margin-top: 1rem;">'
                f'<div><b>IPA Phonetics:</b> <code style="font-size: 1rem;">{tr_res["ipa"]}</code></div>'
                f'<div><b>Bengali Script Comparison:</b> <span style="font-size: 1.1rem; color: #2D5A4C;">{tr_res["bengali"]}</span></div>'
                f'</div>'
                f'<p style="margin-top: 0.8rem; color: #334155; font-size: 0.95rem;"><b>Cultural Meaning:</b> {tr_res["meaning"]}</p>'
                f'</div>'
            )
            st.html(box_html)

            st.caption("Copy script directly: ")
            st.code(tr_res["mayek"], language=None)

# -------------------------------------------------------------
# TAB 4: ORAL FOLKLORE & STORIES (FUNGA WARI)
# -------------------------------------------------------------
elif nav_choice == "📜 Oral Folklore & Stories (Funga Wari)":
    st.markdown("### 📜 Funga Wari & Khunung Eshei: Oral Folklore & Epics")
    st.markdown("Passed down across firesides (Phunga) through generations of elders. Experience traditional stories with spoken oral audio, synchronized Meetei Mayek text, and ancestral morals.")

    story_titles = [f"{s['title']} ({s['title_mayek']})" for s in ORAL_FOLKLORE_STORIES]
    selected_story_title = st.selectbox("Select Ancestral Tale:", story_titles)
    curr_story = next((s for s in ORAL_FOLKLORE_STORIES if f"{s['title']} ({s['title_mayek']})" == selected_story_title), ORAL_FOLKLORE_STORIES[0])

    story_html = (
        f'<div class="folklore-card">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">'
        f'<div>'
        f'<h3 style="margin: 0; font-family: \'Cinzel\', serif; color: #18222F;">{curr_story["title"]}</h3>'
        f'<span class="meitei-script-pill">{curr_story["title_mayek"]}</span>'
        f'</div>'
        f'<div>'
        f'<span class="entity-type-badge">{curr_story["genre"]}</span>'
        f'</div>'
        f'</div>'
        f'<p style="color: #64748B; font-size: 0.85rem; margin-top: 0.5rem;">Recorded with consent from: <b>{curr_story["teller"]}</b></p>'
        f'</div>'
    )
    st.html(story_html)

    col_s_aud, col_s_text = st.columns([1, 1])
    with col_s_aud:
        st.markdown("#### 🔊 Spoken Story Audio")
        if os.path.exists(curr_story["audio_path"]):
            st.audio(curr_story["audio_path"])
        st.info("Traditional oral performance recorded by elders preserving vocal inflection, rhythmic pacing, and ritual prosody.")
        
        st.markdown("#### 🏷️ Cultural Motifs")
        for tag in curr_story["tags"]:
            st.markdown(f"- 🌿 `{tag}`")

    with col_s_text:
        st.markdown("#### 📖 Bilingual Story Narrative")
        st.html(
            f'<div class="folklore-bilingual-panel">'
            f'<div style="font-size: 1.3rem; line-height: 1.6; color: #C86D51; font-family: \'Noto Sans Meetei Mayek\', sans-serif; font-weight: 700; margin-bottom: 0.5rem;">'
            f'{curr_story["mayek_snippet"]}'
            f'</div>'
            f'<div style="font-style: italic; color: #475569; font-size: 0.92rem; margin-bottom: 0.8rem;">'
            f'{curr_story["translit_snippet"]}'
            f'</div>'
            f'<p style="color: #18222F; font-size: 0.95rem; line-height: 1.6;">{curr_story["synopsis"]}</p>'
            f'</div>'
        )

        moral_html = (
            f'<div class="folklore-moral-callout">'
            f'<b>🌱 Indigenous Wisdom & Ecological Moral:</b><br/>'
            f'{curr_story["cultural_moral"]}'
            f'</div>'
        )
        st.html(moral_html)

# -------------------------------------------------------------
# TAB 5: CHRONICLE HISTORICAL TIMELINE
# -------------------------------------------------------------
elif nav_choice == "⏳ Chronicle Historical Timeline":
    st.markdown("### ⏳ Chronicle of Kangleipak: Interactive Historical Timeline")
    st.markdown("A chronological journey through the Royal Court Chronicle (*Cheitharol Kumbaba*) and landmark historical events from 33 CE to 2013 CE.")

    cat_options = ["All Categories", "Monarchy & Statehood", "Monuments & Architecture", "Religious Transition", "Manuscripts & Cultural Memory", "Anti-Colonial Resistance", "Global Heritage"]
    sel_cat = st.selectbox("Filter Events by Category:", cat_options)

    filtered_timeline = HISTORICAL_TIMELINE
    if sel_cat != "All Categories":
        filtered_timeline = [e for e in HISTORICAL_TIMELINE if e["category"] == sel_cat]

    for event in filtered_timeline:
        div_badge = ""
        if event.get("divergence") and event.get("divergence_grade") != "none":
            div_badge = f'<div style="margin-top: 8px;"><span class="timeline-divergence-pill">⚠️ Historical Divergence Alert</span> <small style="color: #991B1B;">{event["divergence"]}</small></div>'

        event_html = (
            f'<div class="timeline-card">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
            f'<span class="timeline-year-pill">{event["year_display"]}</span>'
            f'<span class="entity-type-badge">{event["category"]}</span>'
            f'</div>'
            f'<h4 style="margin: 4px 0; color: #18222F; font-family: \'Cinzel\', serif;">{event["title"]}</h4>'
            f'<div class="meitei-script-pill" style="display: inline-block; margin-bottom: 8px;">{event["title_mayek"]}</div>'
            f'<p style="color: #334155; font-size: 0.95rem; line-height: 1.5; margin: 4px 0;">{event["description"]}</p>'
            f'<div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;"><b>Key Figures:</b> {", ".join(event["key_figures"])}</div>'
            f'{div_badge}'
            f'</div>'
        )
        st.html(event_html)

# -------------------------------------------------------------
# TAB 6: GAMIFIED HERITAGE QUEST (QUIZ & TRIVIA)
# -------------------------------------------------------------
elif nav_choice == "🎮 Heritage Quest & Trivia Challenge":
    st.markdown("### 🎮 Kanglei Heritage Quest: Cultural Knowledge Challenge")
    st.markdown("Test your understanding of Manipuri cultural heritage, Meetei Mayek script anatomy, and historical divergence cases!")

    if "quiz_score" not in st.session_state:
        st.session_state["quiz_score"] = 0
    if "quiz_answered" not in st.session_state:
        st.session_state["quiz_answered"] = {}

    total_q = len(HERITAGE_QUIZ_QUESTIONS)
    answered_count = len(st.session_state["quiz_answered"])
    current_score = st.session_state["quiz_score"]

    # Determine Rank Badge
    if current_score <= 2:
        rank_badge = "🌱 Novice Explorer"
    elif current_score <= 5:
        rank_badge = "📜 Folklore Custodian"
    elif current_score <= 7:
        rank_badge = "🏛️ Maiba / Maibi Scholar"
    else:
        rank_badge = "👑 Supreme Guardian of Kangleipak"

    # Score Banner
    st.html(
        f'<div class="quiz-score-banner">'
        f'<div>'
        f'<h3 style="margin:0; font-family: \'Cinzel\', serif; color: #FAF7F2;">Your Cultural Standing</h3>'
        f'<p style="margin: 4px 0 0 0; color: #D4A373;">Answered: {answered_count} / {total_q} Questions | Score: {current_score} Points</p>'
        f'</div>'
        f'<div>'
        f'<span class="quiz-badge-rank">{rank_badge}</span>'
        f'</div>'
        f'</div>'
    )

    tier_sel = st.radio("Difficulty Tier:", ["All Tiers", "Beginner", "Intermediate", "Divergence Master"], horizontal=True)
    filtered_q = HERITAGE_QUIZ_QUESTIONS
    if tier_sel != "All Tiers":
        filtered_q = [q for q in HERITAGE_QUIZ_QUESTIONS if q["tier"] == tier_sel]

    for q in filtered_q:
        qid = q["id"]
        st.markdown(f"#### ❓ {q['question']}")
        st.markdown(f"**Tier:** `{q['tier']}`")

        user_choice = st.radio(
            "Select your answer:",
            q["options"],
            key=f"opt_{qid}",
            disabled=(qid in st.session_state["quiz_answered"])
        )

        if qid not in st.session_state["quiz_answered"]:
            if st.button(f"Submit Answer for Question", key=f"btn_{qid}"):
                chosen_idx = q["options"].index(user_choice)
                is_correct = (chosen_idx == q["answer_index"])
                st.session_state["quiz_answered"][qid] = {
                    "chosen": chosen_idx,
                    "correct": is_correct
                }
                if is_correct:
                    st.session_state["quiz_score"] += 1
                st.rerun()
        else:
            ans_info = st.session_state["quiz_answered"][qid]
            if ans_info["correct"]:
                st.success(f"✅ **Correct!** {q['explanation']}")
            else:
                st.error(f"❌ **Incorrect.** The correct answer is: **{q['options'][q['answer_index']]}**")
                st.info(f"💡 **Context:** {q['explanation']}")
        st.markdown("---")

    if st.button("🔄 Reset Quiz & Start Over"):
        st.session_state["quiz_score"] = 0
        st.session_state["quiz_answered"] = {}
        st.rerun()

# -------------------------------------------------------------
# TAB 7: INTERACTIVE KNOWLEDGE GRAPH VIEWER
# -------------------------------------------------------------
elif nav_choice == "🕸️ Interactive Knowledge Graph":
    st.markdown("### 🕸️ CIDOC-CRM Interactive Knowledge Graph")
    st.markdown("Explore entity topology, CIDOC-CRM concept classes, multi-provenance edges, and Meetei Mayek script associations.")

    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        entity_names = [e.canonical_name for e in engine.entities.values()]
        selected_entity_name = st.selectbox("Focus Subgraph on Entity:", ["All Core Entities"] + entity_names)
    with filter_col2:
        depth = st.slider("Graph Exploration Depth:", min_value=1, max_value=2, value=1)

    if selected_entity_name == "All Core Entities":
        core_eids = ["E001", "E002", "E005", "E007", "E009", "E010", "E012", "E018", "E019", "E021"]
        combined_nodes = {}
        combined_edges = []
        for eid in core_eids:
            sg = engine.get_subgraph(eid, depth=1)
            for n in sg["nodes"]:
                combined_nodes[n["id"]] = n
            for e in sg["edges"]:
                combined_edges.append(e)
        full_sg = {"nodes": list(combined_nodes.values()), "edges": combined_edges}
        st.markdown(f"Displaying **{len(full_sg['nodes'])}** nodes and **{len(full_sg['edges'])}** CIDOC-CRM edges across pilot entities.")
        html_vis = render_visjs_subgraph(full_sg, height=600)
        components.html(html_vis, height=640, scrolling=False)
    else:
        ent = engine.find_entity(selected_entity_name)
        if ent:
            sg = engine.get_subgraph(ent.entity_id, depth=depth)
            st.markdown(f"Displaying neighborhood for **{ent.canonical_name}** (`{ent.entity_id}`):")
            html_vis = render_visjs_subgraph(sg, height=580)
            components.html(html_vis, height=620, scrolling=False)

            st.markdown("#### 📋 Entity Attributes & Provenance Events")
            rows = []
            for rel, assigns in ent.attributes.items():
                for a in assigns:
                    rows.append({
                        "Claim ID": a.assignment_id,
                        "Relation": a.relation,
                        "Claim Value": a.claim_value_normalized,
                        "Modality": a.evidence_modality.value,
                        "Divergence": a.divergence_grade.value.upper(),
                        "Source": a.source_title,
                        "Tier": a.source_reliability_tier.value
                    })
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

# -------------------------------------------------------------
# TAB 8: MULTIMODAL HERITAGE VAULT
# -------------------------------------------------------------
elif nav_choice == "🏺 Multimodal Heritage Vault":
    st.markdown("### 🏺 Multimodal Cultural Heritage Vault")
    st.markdown("First-class support for Manuscripts (HTR), Monuments & Artifacts (VLM), and Oral Traditions (ASR).")

    v_tab1, v_tab2, v_tab3 = st.tabs([
        "📜 Manuscripts (HTR)",
        "🏛️ Monuments & Iconography (VLM)",
        "🎙️ Oral Traditions (ASR)"
    ])

    with v_tab1:
        st.subheader("📜 Historical Manuscript Transcription (HTR Module)")
        st.markdown("Transcribing 16th century **Subika** and **Puya** folios into standardized Meetei Mayek Unicode and Latin transliteration.")
        
        manuscripts = htr_module.catalog
        if manuscripts:
            selected_ms = st.selectbox("Select Manuscript Folio:", [m["title"] for m in manuscripts])
            ms_entry = next((m for m in manuscripts if m["title"] == selected_ms), manuscripts[0])

            col_img, col_htr = st.columns([1, 1])
            with col_img:
                if os.path.exists(ms_entry["filepath"]):
                    img = Image.open(ms_entry["filepath"])
                    st.image(img, caption=ms_entry["title"], use_container_width=True)
            with col_htr:
                htr_res = htr_module.transcribe_manuscript(ms_entry["filepath"])
                st.markdown(f"#### ꯏꯌꯦꯛ Transcribed Meetei Mayek Script")
                st.html(
                    f'<div style="font-size: 1.5rem; line-height: 1.8; color: #C86D51; background: #FFF; padding: 1rem; border-radius: 8px; border: 1px solid #E2E8F0;">'
                    f'{htr_res["transcription_mayek"]}'
                    f'</div>'
                )
                st.markdown(f"**Latin Transliteration**: *{htr_res['transliteration']}*")
                st.markdown(f"**English Translation**: {htr_res['translation_en']}")
                st.markdown(f"**Confidence**: `{htr_res['confidence']*100:.1f}%` | **Standard**: `{htr_res['script_standard']}`")
                st.markdown(f"**Recognized Concepts**: {', '.join(htr_res['extracted_concepts'])}")

    with v_tab2:
        st.subheader("🏛️ Monument & Iconography Understanding (VLM Module)")
        st.markdown("Automated architectural analysis and CIDOC-CRM triple extraction for monuments and palace ruins.")
        
        images = vlm_module.catalog
        if images:
            selected_img_title = st.selectbox("Select Monument Photo:", [im["title"] for im in images])
            img_entry = next((im for im in images if im["title"] == selected_img_title), images[0])

            col_vlm_img, col_vlm_res = st.columns([1, 1])
            with col_vlm_img:
                if os.path.exists(img_entry["filepath"]):
                    img = Image.open(img_entry["filepath"])
                    st.image(img, caption=img_entry["title"], use_container_width=True)
            with col_vlm_res:
                vlm_res = vlm_module.analyze_image(img_entry["filepath"])
                st.markdown(f"#### {vlm_res['title']}")
                st.markdown(f"**Caption**: *{vlm_res['caption']}*")
                st.markdown(f"**Architectural & Iconography Tags**:")
                for tag in vlm_res["iconography_tags"]:
                    st.markdown(f"- 🏷️ `{tag}`")
                st.markdown("**Proposed CIDOC-CRM Candidate Triples**:")
                for t in vlm_res["candidate_triples"]:
                    st.markdown(f"- `{t['subject']}` ➔ **{t['relation']}** (`{t['cidoc']}`) ➔ `{t['object']}`")

    with v_tab3:
        st.subheader("🎙️ Oral Traditions & Speech Ingestion (ASR Module)")
        st.markdown("Oral testimony, folk narratives, and sacred chants as a first-class knowledge graph modality.")

        audios = list(asr_module.manifest.values())
        if audios:
            selected_audio_title = st.selectbox("Select Oral Recording:", [a["title"] for a in audios])
            audio_entry = next((a for a in audios if a["title"] == selected_audio_title), audios[0])

            col_aud_p, col_aud_trans = st.columns([1, 1])
            with col_aud_p:
                st.markdown(f"#### 🔊 Audio Playback: {audio_entry['title']}")
                if os.path.exists(audio_entry["filepath"]):
                    st.audio(audio_entry["filepath"])
                st.markdown(f"- **Speaker/Performer**: `{audio_entry['speaker_or_performer']}`")
                st.markdown(f"- **Language**: `{audio_entry['language']}`")
                st.markdown(f"- **Consent Status**: `🛡️ {audio_entry['consent_status']}`")
                st.markdown(f"- **Provenance Terms**: *{audio_entry['provenance_notes']}*")

            with col_aud_trans:
                asr_res = asr_module.transcribe_audio(audio_entry["filepath"])
                st.markdown("#### 📝 Speech-to-Text Transcription")
                st.markdown(f"**Original (Meetei Mayek)**: `{asr_res['transcript_original']}`")
                st.markdown(f"**Phonetic Transliteration**: *{asr_res['transliteration']}*")
                st.markdown(f"**Aligned English Translation**: {asr_res['english_translation']}")
                st.markdown(f"**Confidence**: `{asr_res['asr_confidence']*100:.1f}%`")
                st.markdown("**Extracted Oral Triples**:")
                for t in asr_res["candidate_triples"]:
                    st.markdown(f"- `{t['subject']}` ➔ **{t['relation']}** ➔ `{t['object']}`")

# -------------------------------------------------------------
# TAB 9: DUAL-PROVENANCE & DIVERGENCE LAB
# -------------------------------------------------------------
elif nav_choice == "⚖️ Dual-Provenance & Divergence Lab":
    st.markdown("### ⚖️ Dual-Provenance & Divergence Laboratory")
    st.markdown("Detailed audit of all 23 divergence cases in the Manipuri Cultural Heritage Knowledge Graph.")

    cases = engine.provenance.divergence_registry
    grade_filter = st.radio("Filter Divergence Grade:", ["All (23)", "Hard (12)", "Soft (7)", "None / Agreement (4)"], horizontal=True)

    filtered_cases = []
    for gid, c in cases.items():
        g_val = c["grade"].value
        if grade_filter == "All (23)":
            filtered_cases.append((gid, c))
        elif grade_filter == "Hard (12)" and g_val == "hard":
            filtered_cases.append((gid, c))
        elif grade_filter == "Soft (7)" and g_val == "soft":
            filtered_cases.append((gid, c))
        elif grade_filter == "None / Agreement (4)" and g_val == "none":
            filtered_cases.append((gid, c))

    for gid, c in filtered_cases:
        ent = engine.entities.get(c["entity_id"])
        ent_name = ent.canonical_name if ent else c["entity_id"]
        meitei_name = f" ({ent.name_meitei_script})" if ent and ent.name_meitei_script else ""
        grade_color = "#DC2626" if c["grade"] == DivergenceGrade.HARD else ("#D97706" if c["grade"] == DivergenceGrade.SOFT else "#16A34A")

        with st.expander(f"{gid}: {ent_name} ➔ {c['relation']} [{c['grade'].value.upper()}]", expanded=False):
            col_l, col_r = st.columns([1, 1])
            with col_l:
                st.markdown(f"**Entity**: {ent_name}{meitei_name} (`{c['entity_id']}`)")
                st.markdown(f"**Relation Target**: `{c['relation']}`")
                st.markdown(f"**Divergence Category**: `{c['divergence_type']}`")
                st.markdown(f"**Classification**: <span style='color:{grade_color}; font-weight:bold;'>{c['grade'].value.upper()}</span>", unsafe_allow_html=True)
                st.markdown(f"**Why Divergent**: *{c['why_divergent']}*")
                st.markdown(f"**Expected System Action**: `{c['expected_behavior']}`")
            with col_r:
                st.markdown("**Underlying Attributed Claims:**")
                claim_ids = c.get("claim_ids", [])
                if ent:
                    for rel, assigns in ent.attributes.items():
                        for a in assigns:
                            if a.assignment_id in claim_ids:
                                st.markdown(f"- <b>{a.claim_value_normalized}</b> (Modality: `{a.evidence_modality.value}`) — *{a.source_title} (Tier {a.source_reliability_tier.value})*", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 10: CULTURAL DOSSIER EXPORT STUDIO
# -------------------------------------------------------------
elif nav_choice == "📑 Cultural Dossier Export Studio":
    st.markdown("### 📑 Cultural Heritage Dossier & Factsheet Export Studio")
    st.markdown("Generate publication-ready, citation-backed cultural heritage factsheets for any entity in the Knowledge Graph.")

    all_ent_names = sorted([e.canonical_name for e in engine.entities.values()])
    selected_ent_name = st.selectbox("Select Heritage Entity for Dossier Generation:", all_ent_names)
    target_ent = engine.find_entity(selected_ent_name)

    if target_ent:
        # Build Dossier Markdown
        lines = [
            f"# Cultural Heritage Dossier: {target_ent.canonical_name}",
            f"**Meetei Mayek Script**: {target_ent.name_meitei_script or 'N/A'}",
            f"**CIDOC-CRM Class**: `{target_ent.cidoc_class}`",
            f"**Known Aliases**: {', '.join(target_ent.aliases)}",
            "",
            "## Attributed Claims & Historical Provenance (CIDOC-CRM E13)",
            ""
        ]

        dossier_claims = []
        for rel, assigns in target_ent.attributes.items():
            for a in assigns:
                dossier_claims.append({
                    "Relation": a.relation,
                    "Attributed Value": a.claim_value_normalized,
                    "Modality": a.evidence_modality.value,
                    "Divergence": a.divergence_grade.value.upper(),
                    "Source Record": a.source_title,
                    "Reliability Tier": a.source_reliability_tier.value
                })
                lines.append(f"- **{a.relation}**: {a.claim_value_normalized} | *Source:* {a.source_title} (Tier {a.source_reliability_tier.value}, Modality: {a.evidence_modality.value})")

        dossier_md = "\n".join(lines)

        # Render Visual Dossier Card
        st.html(
            f'<div class="heritage-answer-card">'
            f'<div class="answer-card-header">'
            f'<div class="entity-title-group">'
            f'<span class="entity-name-text">{target_ent.canonical_name}</span>'
            f'<span class="meitei-script-pill">{target_ent.name_meitei_script or ""}</span>'
            f'<span class="entity-type-badge">{target_ent.cidoc_class}</span>'
            f'</div>'
            f'<span class="verified-pill">✓ Publication Ready</span>'
            f'</div>'
            f'<p><b>Aliases:</b> {", ".join(target_ent.aliases)}</p>'
            f'</div>'
        )

        st.markdown("#### 📋 Attributed Heritage Claims")
        if dossier_claims:
            st.dataframe(pd.DataFrame(dossier_claims), use_container_width=True)

        st.markdown("#### 📥 Export Dossier File")
        d_col1, d_col2 = st.columns([1, 1])
        with d_col1:
            st.download_button(
                label="📄 Download Dossier (.md Markdown)",
                data=dossier_md,
                file_name=f"Heritage_Dossier_{target_ent.canonical_name.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with d_col2:
            st.download_button(
                label="📊 Download Claims Table (.csv)",
                data=pd.DataFrame(dossier_claims).to_csv(index=False).encode('utf-8'),
                file_name=f"Claims_{target_ent.canonical_name.replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# -------------------------------------------------------------
# TAB 11: COMMUNITY REVIEW DESK
# -------------------------------------------------------------
elif nav_choice == "🛡️ Community Review Desk":
    render_review_interface(engine)

# -------------------------------------------------------------
# TAB 12: BENCHMARK & RESEARCH EVALUATION
# -------------------------------------------------------------
elif nav_choice == "📊 Benchmark & Research Evaluation":
    st.markdown("### 📊 Benchmark & Empirical Research Evaluation")
    st.markdown("Comparing **Baseline A** (WJoconde-style text+image single-provenance baseline) vs. **Full Multimodal Heritage GraphRAG**.")

    if st.button("🚀 Run Evaluation Suite Now (41 Gold QA + 23 Divergence Cases)"):
        with st.spinner("Executing rigorous evaluation harness..."):
            evaluator = HeritageEvaluator(data_dir="data/raw", eval_dir="eval")
            qa_res = evaluator.run_gold_qa_evaluation()
            div_res = evaluator.run_divergence_benchmark()

            st.session_state["qa_res"] = qa_res
            st.session_state["div_res"] = div_res
            st.success("Evaluation complete!")

    if "qa_res" in st.session_state:
        qa_res = st.session_state["qa_res"]
        div_res = st.session_state["div_res"]

        # High-Level Metrics Comparison
        st.markdown("#### 🏆 Quantitative Benchmark Results")
        m_c1, m_c2, m_c3, m_c4 = st.columns(4)
        with m_c1:
            st.metric("Full System Accuracy", f"{qa_res['full_system']['behavior_accuracy']}%", delta=f"+{qa_res['full_system']['behavior_accuracy'] - qa_res['baseline_a']['behavior_accuracy']:.1f}% vs Baseline A")
        with m_c2:
            st.metric("Answer Coverage", f"{qa_res['full_system']['answer_coverage']}%", delta=f"+{qa_res['full_system']['answer_coverage'] - qa_res['baseline_a']['answer_coverage']:.1f}%")
        with m_c3:
            st.metric("Conflict Handling Rate", f"{qa_res['full_system']['conflict_handling_rate']}%", delta=f"+{qa_res['full_system']['conflict_handling_rate'] - qa_res['baseline_a']['conflict_handling_rate']:.1f}%")
        with m_c4:
            st.metric("Hallucination Abstention", f"{qa_res['full_system']['hallucination_abstention_rate']}%", delta=f"+{qa_res['full_system']['hallucination_abstention_rate'] - qa_res['baseline_a']['hallucination_abstention_rate']:.1f}%")

        st.markdown("#### 📋 Formal Evaluation Metric Matrix")
        comparison_df = pd.DataFrame({
            "Metric": [
                "Overall Behavior Accuracy (%)",
                "Answer Coverage (%)",
                "Conflict Handling Rate (%)",
                "Hallucination Abstention Rate (%)",
                "Oral Modality Support",
                "Dual-Provenance Preservation"
            ],
            "Baseline A (WJoconde-style)": [
                f"{qa_res['baseline_a']['behavior_accuracy']}%",
                f"{qa_res['baseline_a']['answer_coverage']}%",
                f"{qa_res['baseline_a']['conflict_handling_rate']}% (Collapses all)",
                f"{qa_res['baseline_a']['hallucination_abstention_rate']}%",
                "❌ Ignored / Invisible",
                "❌ Single-winner overwrite"
            ],
            "Full System (Our Model)": [
                f"{qa_res['full_system']['behavior_accuracy']}%",
                f"{qa_res['full_system']['answer_coverage']}%",
                f"{qa_res['full_system']['conflict_handling_rate']}% (Dual-perspective)",
                f"{qa_res['full_system']['hallucination_abstention_rate']}%",
                "✅ First-Class Modality (ASR)",
                "✅ E13 Attribute Assignment"
            ]
        })
        st.table(comparison_df)

        st.markdown("#### 🎯 Divergence Detector Precision / Recall")
        d_c1, d_c2, d_c3, d_c4 = st.columns(4)
        d_c1.metric("Precision", f"{div_res['precision']}%")
        d_c2.metric("Recall", f"{div_res['recall']}%")
        d_c3.metric("F1 Score", f"{div_res['f1_score']}%")
        d_c4.metric("Gold Cases Tested", f"{div_res['total_cases']}")

# -------------------------------------------------------------
# TAB 13: ACADEMIC PROJECT REPORT & DOWNLOADS
# -------------------------------------------------------------
elif nav_choice == "📄 Academic Project Report & Downloads":
    st.markdown("## 📄 Academic Project Report Download & Review Center")
    st.markdown(
        "Download the official capstone project report formatted strictly to academic publication standards: "
        "**Times New Roman (12pt body, 24pt title)**, **1.5 Line Spacing**, **Justified Alignment**, and "
        "**Margins: Top 25mm, Bottom 25mm, Left 38mm (binding), Right 22mm**."
    )

    st.html('''
    <div style="background: linear-gradient(135deg, #18222F 0%, #2D5A4C 100%); color: #FAF7F2; padding: 24px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
        <h3 style="margin: 0 0 8px 0; color: #E2B653; font-family: 'Cinzel', serif;">Capstone Project Report Document Ready</h3>
        <p style="margin: 0 0 16px 0; font-size: 1.05rem; opacity: 0.95;">
            Title: <strong>Multimodal Cultural Heritage Knowledge Graph for Low-Resource Languages</strong><br>
            Subtitle: <em>A CIDOC-CRM Aligned GraphRAG System with Dual-Provenance Conflict Resolution (Pilot: Manipuri / Meitei)</em>
        </p>
        <div style="display: flex; gap: 16px; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.12); padding: 8px 16px; border-radius: 6px; font-size: 0.9rem;">📏 <strong>Pages:</strong> ~38 Standard Pages (60 PDF print pages)</div>
            <div style="background: rgba(255,255,255,0.12); padding: 8px 16px; border-radius: 6px; font-size: 0.9rem;">📝 <strong>Word Count:</strong> ~10,000 Technical Words</div>
            <div style="background: rgba(255,255,255,0.12); padding: 8px 16px; border-radius: 6px; font-size: 0.9rem;">📊 <strong>Diagrams:</strong> 4 High-Res Flowcharts (300 DPI)</div>
            <div style="background: rgba(255,255,255,0.12); padding: 8px 16px; border-radius: 6px; font-size: 0.9rem;">🖼️ <strong>Placeholders:</strong> Exactly 6 Framed Screenshot Boxes</div>
            <div style="background: rgba(255,255,255,0.12); padding: 8px 16px; border-radius: 6px; font-size: 0.9rem;">📑 <strong>Tables:</strong> 11 Detailed Research Tables</div>
        </div>
    </div>
    ''')

    col1, col2, col3 = st.columns(3)
    docx_path = "Multimodal_Cultural_Heritage_NLP_Project_Report.docx"
    pdf_path = "Multimodal_Cultural_Heritage_NLP_Project_Report.pdf"
    html_path = "report_view.html"

    with col1:
        if os.path.exists(docx_path):
            with open(docx_path, "rb") as f:
                st.download_button(
                    label="📥 Download Word (.docx)",
                    data=f.read(),
                    file_name="Multimodal_Cultural_Heritage_NLP_Project_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        st.caption("Fully editable Microsoft Word document with formatted styles and dynamic page numbering.")

    with col2:
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download PDF (.pdf)",
                    data=f.read(),
                    file_name="Multimodal_Cultural_Heritage_NLP_Project_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        st.caption("Publication-ready PDF document viewable and printable on any computer, phone, or browser.")

    with col3:
        if os.path.exists(html_path):
            with open(html_path, "rb") as f:
                st.download_button(
                    label="🌐 Download HTML Report",
                    data=f.read(),
                    file_name="Multimodal_Cultural_Heritage_NLP_Project_Report.html",
                    mime="text/html",
                    use_container_width=True
                )
        st.caption("Standalone HTML web page with interactive buttons and print styling.")

    st.markdown("---")
    st.markdown("### 📐 Complete Technical Architecture & Engineering Specification Blueprint")
    st.markdown(
        "Exhaustive low-level engineering specification manual covering **backend and frontend internals, 4-modality ingestion pipelines, "
        "CIDOC-CRM E13 ontology schemas, NetworkX BFS algorithms, FastAPI contracts, Streamlit state machines, mathematical formulations, "
        "and complete replication instructions** to rebuild this exact project without visual screenshots."
    )

    bp_c1, bp_c2, bp_c3 = st.columns(3)
    bp_docx_p = "Comprehensive_System_Architecture_and_Engineering_Blueprint.docx"
    bp_pdf_p = "Comprehensive_System_Architecture_and_Engineering_Blueprint.pdf"
    bp_html_p = "system_blueprint_view.html"

    with bp_c1:
        if os.path.exists(bp_docx_p):
            with open(bp_docx_p, "rb") as f:
                st.download_button(
                    label="📥 Download Blueprint (.docx)",
                    data=f.read(),
                    file_name="Comprehensive_System_Architecture_and_Engineering_Blueprint.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        st.caption("Complete Microsoft Word engineering manual with low-level specs and tables.")

    with bp_c2:
        if os.path.exists(bp_pdf_p):
            with open(bp_pdf_p, "rb") as f:
                st.download_button(
                    label="📄 Download Blueprint (.pdf)",
                    data=f.read(),
                    file_name="Comprehensive_System_Architecture_and_Engineering_Blueprint.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        st.caption("29-page publication-ready PDF printable engineering blueprint.")

    with bp_c3:
        if os.path.exists(bp_html_p):
            with open(bp_html_p, "rb") as f:
                st.download_button(
                    label="🌐 Download Blueprint HTML",
                    data=f.read(),
                    file_name="Comprehensive_System_Architecture_and_Engineering_Blueprint.html",
                    mime="text/html",
                    use_container_width=True
                )
        st.caption("Standalone HTML document readable in any web browser.")

    st.markdown("---")
    st.markdown("### 📚 Report Chapter Structure & Visual Assets")
    
    st.markdown("""
    1. **Front Matter**: Front Cover (24pt Times Bold), Certificate of Endorsement, Student Declaration, Acknowledgements, Structured Abstract, Table of Contents, List of Tables, List of Figures.
    2. **Chapter 1: Introduction to Natural Language Processing & Cultural Heritage AI**: Comprehensive survey of NLP, linguistic levels (phonology to discourse), NLP processing lifecycle (**Figure 1 Diagram**), computational advantages, systematic limitations, low-resource language crisis, and why Manipuri/Meitei was chosen.
    3. **Chapter 2: Literature Review & Theoretical Foundations**: Evolution of Knowledge Graphs (WordNet, ConceptNet, Wikidata), CIDOC-CRM ISO 21127 ontology standard, dense vector retrieval (Bi-encoders/Cross-encoders), multimodal representation learning, and script transliteration models. Includes **Table 1: Comparative Analysis Matrix**.
    4. **Chapter 3: System Requirements & Domain Modeling**: Functional (**Table 2**) and Non-Functional (**Table 3**) requirements, domain ontology schema, CIDOC-CRM mapping (**Table 4**), epistemic pluralism, and multimodal taxonomy.
    5. **Chapter 4: Knowledge Graph Construction & Data Engineering**: Corpus acquisition (**Table 5**), Meetei Mayek script normalization, triplet mining, graph ingestion, vector embeddings, and cross-modal indexing.
    6. **Chapter 5: System Architecture & Implementation**: End-to-end architecture (**Figure 2 Diagram**), Hybrid GraphRAG, Divergence-Flag Protocol (**Figure 4 Diagram**), Cross-Modal validation (**Figure 6 Diagram**), FastAPI backend (**Table 6**), and Streamlit interface. Holds **Figure 3, 5, 7, 8, 9, 10 screenshot placeholders**.
    7. **Chapter 6: Results, Evaluation & Experimental Analysis**: Quantitative benchmark vs. Baseline A (**Table 7**), latency benchmarks (**Table 8**), human usability study (**Table 9**), and qualitative case studies.
    8. **Chapter 7: Production Deployment & Operational Guidelines**: Environment matrix (**Table 10**), local setup guide, production health checks (**Table 11**), containerization, and recovery.
    9. **Chapter 8: Conclusion, Ethical Considerations & Future Horizons**: Summary of achievements, Indigenous Data Sovereignty (CARE principles), limitations, and roadmap.
    10. **References & Appendices**: 30 IEEE/APA citations, 41-question Gold QA Benchmark (Appendix A), Curated Divergence Catalog (Appendix B), Meetei Mayek 27-letter sound map (Appendix C), and OpenAPI REST spec (Appendix D).
    """)

    st.markdown("---")
    st.markdown("### 🖼️ Guide for Attaching Your 6 Live Screenshots")
    st.info(
        "The report has 6 designated framed placeholder boxes ready for you to paste screenshots from this live app into Word:\n\n"
        "- **Figure 3**: Knowledge Graph Explorer (open 'Interactive Knowledge Graph', search Kangla Sha, expand 1 hop).\n"
        "- **Figure 5**: Dual-Provenance Divergence Alert Card (open 'Heritage GraphRAG Explorer', query 1891 statues conflict).\n"
        "- **Figure 7**: Meetei Mayek Script Learning Studio (open 'Meetei Mayek Studio', select Kok letter).\n"
        "- **Figure 8**: Virtual Heritage Tour (open 'Virtual Heritage Tour', select Stop 2 Kangla Sha).\n"
        "- **Figure 9**: Oral Folklore Storytelling Lounge (open 'Oral Folklore & Stories', select Khamba Thoibi story).\n"
        "- **Figure 10**: Historical Chronicle Timeline (open 'Chronicle Historical Timeline', expand 1891 War)."
    )
