"""
Community-in-the-Loop Review Desk (Section 6.4 & Section 16).
Enables designated heritage custodians, historians, and village elders to annotate
and adjudicate flagged divergence cases through an additive, non-destructive protocol.
"""
import streamlit as st
import datetime
from kg.graph_engine import HeritageGraphEngine
from kg.schema import CommunityAnnotation, AccessLevel, DivergenceGrade

def render_review_interface(engine: HeritageGraphEngine):
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2D5A4C 0%, #1E3D34 100%); padding: 1.5rem; border-radius: 12px; color: #FAF7F2; margin-bottom: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="margin: 0; font-family: 'Cinzel', 'Merriweather', serif; font-size: 1.6rem; color: #E2B653;">
            🛡️ Community-in-the-Loop Review Desk
        </h2>
        <p style="margin: 0.4rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">
            Empowering indigenous heritage custodians and traditional scholars with <b>additive adjudication</b>.
            Community findings enrich the Knowledge Graph without destroying or overwriting historical archival records.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sovereign Data Governance Notice
    st.info("📜 **Indigenous Data Sovereignty (CARE Principles)**: In accordance with Section 16, community annotations represent living cultural memory. Archival gazetteers and oral traditions are maintained side-by-side with full provenance attribution.")

    divergences = engine.provenance.divergence_registry
    if not divergences:
        st.warning("No divergence cases registered in the system.")
        return

    # Filter tabs
    tab_pending, tab_adjudicated, tab_sovereignty = st.tabs(["⏳ Flagged Divergence Queue", "✅ Community Adjudications", "🔒 Access & Data Sovereignty"])

    with tab_pending:
        st.subheader("Flagged Discrepancies Awaiting Community Testimony")
        
        # Select group to review
        group_keys = list(divergences.keys())
        selected_gid = st.selectbox(
            "Select Divergence Case to Adjudicate:",
            group_keys,
            format_func=lambda gid: f"{gid}: {divergences[gid]['entity_id']} - {divergences[gid]['relation']} ({divergences[gid]['grade'].value.upper()})"
        )

        case = divergences[selected_gid]
        ent = engine.entities.get(case["entity_id"])
        ent_name = ent.canonical_name if ent else case["entity_id"]
        meitei_name = f" ({ent.name_meitei_script})" if ent and ent.name_meitei_script else ""

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"### Entity: **{ent_name}**{meitei_name}")
            st.markdown(f"- **Property In Conflict**: `{case['relation']}`")
            st.markdown(f"- **Divergence Category**: `{case['divergence_type']}`")
            st.markdown(f"- **Divergence Grade**: `:{'red' if case['grade'] == DivergenceGrade.HARD else 'orange'}[{case['grade'].value.upper()}]`")
            st.markdown(f"- **Underlying Conflict**: *{case['why_divergent']}*")

        with col2:
            st.markdown("### Existing Attributed Claims")
            claim_ids = case.get("claim_ids", [])
            claims = []
            if ent:
                for rel, assigns in ent.attributes.items():
                    for a in assigns:
                        if a.assignment_id in claim_ids:
                            claims.append(a)

            for i, c in enumerate(claims, start=1):
                st.markdown(f"""
                <div style="background: #FDFBF7; border-left: 4px solid #C86D51; padding: 0.6rem 0.8rem; margin-bottom: 0.5rem; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <span style="font-weight: 600; color: #1E293B;">Perspective {chr(64+i)} ({c.evidence_modality.value}):</span> <b>{c.claim_value_normalized}</b><br/>
                    <small style="color: #64748B;">Source: {c.source_title} (Tier {c.source_reliability_tier.value})</small><br/>
                    <span style="font-style: italic; font-size: 0.85rem; color: #334155;">"{c.claim_text}"</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("✍️ Submit Community Adjudication")

        with st.form(f"review_form_{selected_gid}"):
            reviewer_col1, reviewer_col2 = st.columns(2)
            with reviewer_col1:
                reviewer_name = st.text_input("Reviewer Name:", value="Elder N. Ningthouja")
            with reviewer_col2:
                reviewer_role = st.selectbox(
                    "Reviewer Custodial Role:",
                    ["Cultural Custodian / Traditional Scholar", "Village Elder / Oral Storyteller", "Puya Manuscript Specialist", "Academic Heritage Historian"]
                )

            adjudication_text = st.text_area(
                "Community Finding / Traditional Context:",
                value=f"Traditional community memory confirms that {ent_name}'s {case['relation']} preserves profound cultural symbolism handed down through sacred oral lineage, providing essential context to external archival records.",
                height=100
            )

            consent_col1, consent_col2 = st.columns(2)
            with consent_col1:
                consent_given = st.checkbox("Informed consent granted under community data sovereignty", value=True)
            with consent_col2:
                access_tier = st.selectbox(
                    "Recommended Public Access Tier:",
                    [AccessLevel.PUBLIC.value, AccessLevel.RESTRICTED.value, AccessLevel.SACRED_NOT_MACHINE_QUERYABLE.value]
                )

            submitted = st.form_submit_button("🛡️ Record Additive Community Adjudication")
            if submitted:
                annotation = CommunityAnnotation(
                    annotation_id=f"ANN_{selected_gid}_{datetime.datetime.now().strftime('%Y%m%d%H%M')}",
                    entity_id=case["entity_id"],
                    divergence_group_id=selected_gid,
                    reviewer_name=reviewer_name,
                    reviewer_role=reviewer_role,
                    adjudication_text=adjudication_text,
                    recommended_weight=1.0,
                    data_sovereignty_consent=consent_given,
                    access_level_recommendation=AccessLevel(access_tier)
                )
                engine.provenance.add_community_annotation(annotation)
                st.success(f"✅ Additive annotation successfully registered for {ent_name} ({selected_gid})! Archival provenance preserved.")

    with tab_adjudicated:
        st.subheader("Verified Community Adjudications")
        all_anns = engine.provenance.community_annotations
        if not all_anns:
            st.info("No community annotations registered yet. Use the review form to add an adjudication.")
        else:
            for ann in all_anns:
                st.markdown(f"""
                <div style="background: #F4EFEA; border-left: 5px solid #2D5A4C; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong style="color: #2D5A4C; font-size: 1.05rem;">{ann.reviewer_name} ({ann.reviewer_role})</strong>
                        <span style="color: #64748B; font-size: 0.85rem;">Group: <code>{ann.divergence_group_id}</code> | Date: {ann.timestamp[:10]}</span>
                    </div>
                    <p style="margin: 0.5rem 0; color: #1E293B;">"{ann.adjudication_text}"</p>
                    <div style="font-size: 0.8rem; color: #475569;">
                        Access Level: <span style="background: #E2E8F0; padding: 2px 6px; border-radius: 4px;">{ann.access_level_recommendation.value}</span> | 
                        Consent Verified: <b>{'Yes' if ann.data_sovereignty_consent else 'No'}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab_sovereignty:
        st.subheader("🔒 Indigenous Data Sovereignty Matrix")
        st.markdown("""
        Every entity and relation in this Knowledge Graph is assigned an explicit **Access Tier**:
        - **Public (`public`)**: Open for scholarly research, educational access, and cross-lingual GraphRAG queries.
        - **Restricted (`restricted`)**: Accessible only to authenticated academic researchers and verified community partners.
        - **Sacred-Not-Machine-Queryable (`sacred-not-machine-queryable`)**: Traditional ritual formulae or sensitive ceremonial knowledge preserved in the repository with indexing withheld from automated generative synthesis.
        """)

        tier_counts = {"public": len(engine.entities), "restricted": 0, "sacred-not-machine-queryable": 0}
        c1, c2, c3 = st.columns(3)
        c1.metric("Public Heritage Entities", tier_counts["public"], help="Freely queryable")
        c2.metric("Restricted Clan Records", tier_counts["restricted"], help="Requires permission")
        c3.metric("Sacred Ceremonial Rites", tier_counts["sacred-not-machine-queryable"], help="Not machine queryable")
