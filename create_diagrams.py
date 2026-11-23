"""
Generates high-resolution academic data diagrams and flowcharts for the NLP Project Report.
Uses matplotlib to produce clean, professional, publication-quality figures.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("report_assets", exist_ok=True)

def save_diagram(fig, filename):
    filepath = os.path.join("report_assets", filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {filepath}")

# =============================================================================
# DIAGRAM 1: NLP CORE LIFECYCLE & HIERARCHICAL ARCHITECTURE FLOWCHART
# =============================================================================
def generate_diagram1():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 96, "Natural Language Processing (NLP) Hierarchical Processing Architecture",
            ha='center', va='center', fontsize=13, fontweight='bold', fontfamily='serif', color='#18222F')

    stages = [
        {"y": 82, "name": "Level 1: Raw Linguistic Input", "desc": "Raw Speech Audio Signals, Written Text Strings, Scanned Manuscript Folios", "color": "#E2E8F0", "border": "#94A3B8"},
        {"y": 68, "name": "Level 2: Phonetics, Morphology & Orthography", "desc": "Acoustic Featurization, Tokenization, Lemmatization, Subword Encoding (BPE/WordPiece), Unicode Normalization", "color": "#EDE9FE", "border": "#8B5CF6"},
        {"y": 54, "name": "Level 3: Syntactic Analysis & Grammar", "desc": "Part-of-Speech (POS) Tagging, Constituency & Dependency Parsing, Morphosyntactic Agreement", "color": "#E0E7FF", "border": "#6366F1"},
        {"y": 40, "name": "Level 4: Lexical & Compositional Semantics", "desc": "Named Entity Recognition (NER), Relation Extraction, Word Sense Disambiguation, Dense Vector Embeddings", "color": "#FEF3C7", "border": "#D97706"},
        {"y": 26, "name": "Level 5: Discourse & Pragmatic Understanding", "desc": "Coreference Resolution, Dialogue Context, Intent Detection, Cultural Nuance & Speech Act Theory", "color": "#D1FAE5", "border": "#10B981"},
        {"y": 12, "name": "Level 6: Applied Knowledge & Cognitive Systems", "desc": "Knowledge Graphs (CIDOC-CRM), Multimodal GraphRAG, Cross-Lingual Translation, Generative QA", "color": "#FEE2E2", "border": "#EF4444"}
    ]

    for i, st in enumerate(stages):
        box = patches.FancyBboxPatch((8, st["y"] - 4.5), 84, 9,
                                      boxstyle="round,pad=0.5,rounding_size=1.5",
                                      facecolor=st["color"], edgecolor=st["border"], linewidth=1.5)
        ax.add_patch(box)
        ax.text(12, st["y"] + 1.2, st["name"], fontsize=10.5, fontweight='bold', fontfamily='serif', color='#1E293B')
        ax.text(12, st["y"] - 2.2, st["desc"], fontsize=8.5, fontfamily='serif', color='#334155')

        # Arrow down to next level
        if i < len(stages) - 1:
            ax.annotate('', xy=(50, stages[i+1]["y"] + 4.8), xytext=(50, st["y"] - 4.8),
                        arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.5, mutation_scale=12))

    save_diagram(fig, "diagram1_nlp_lifecycle.png")

# =============================================================================
# DIAGRAM 2: END-TO-END MULTIMODAL KNOWLEDGE GRAPH ARCHITECTURE
# =============================================================================
def generate_diagram2():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(55, 96, "End-to-End Multimodal Knowledge Graph Architecture for Low-Resource Heritage",
            ha='center', va='center', fontsize=12.5, fontweight='bold', fontfamily='serif', color='#18222F')

    # Modality Ingestion Boxes (Top row)
    modalities = [
        {"x": 4, "title": "1. Manuscripts", "sub": "Meetei Mayek HTR\n(Iyek 27 Standard)", "bg": "#FCE7F3", "bdr": "#BE185D"},
        {"x": 31, "title": "2. Monuments", "sub": "VLM Captioning &\nIconography Tagging", "bg": "#FEF3C7", "bdr": "#D97706"},
        {"x": 58, "title": "3. Oral Speech", "sub": "Cross-Lingual ASR\n(+ Informed Consent)", "bg": "#D1FAE5", "bdr": "#047857"},
        {"x": 85, "title": "4. Archival Text", "sub": "Normalization &\nAlias Clustering", "bg": "#E0E7FF", "bdr": "#4338CA"}
    ]

    for m in modalities:
        box = patches.FancyBboxPatch((m["x"], 74), 21, 14, boxstyle="round,pad=0.4,rounding_size=1.2",
                                      facecolor=m["bg"], edgecolor=m["bdr"], linewidth=1.4)
        ax.add_patch(box)
        ax.text(m["x"] + 10.5, 83.5, m["title"], ha='center', va='center', fontsize=9.5, fontweight='bold', fontfamily='serif', color='#18222F')
        ax.text(m["x"] + 10.5, 78, m["sub"], ha='center', va='center', fontsize=7.5, fontfamily='serif', color='#334155')
        # Arrow down
        ax.annotate('', xy=(m["x"] + 10.5, 62), xytext=(m["x"] + 10.5, 73.5),
                    arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.3, mutation_scale=10))

    # Central Processing & Validation Layer
    mid_box = patches.FancyBboxPatch((4, 46), 102, 16, boxstyle="round,pad=0.5,rounding_size=1.5",
                                      facecolor="#F8FAFC", edgecolor="#64748B", linewidth=1.5)
    ax.add_patch(mid_box)
    ax.text(55, 58, "Stage 2 & 3: Extraction, Semantic Matching & Joint Validation Layer",
            ha='center', va='center', fontsize=10.5, fontweight='bold', fontfamily='serif', color='#1E293B')
    ax.text(28, 51, "• LLM + VLM Triple Extraction (WJoconde Pattern)\n• SentenceTransformer Semantic Matching (all-MiniLM-L6-v2)",
            ha='left', va='center', fontsize=8, fontfamily='serif', color='#334155')
    ax.text(78, 51, "• Cross-Modal Evidence Corroboration\n• Divergence-Flag Detection (Hard vs Soft Distance)",
            ha='left', va='center', fontsize=8, fontfamily='serif', color='#334155')

    # Arrows from mid layer down to KG & Review
    ax.annotate('', xy=(30, 34), xytext=(30, 45.5), arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.3, mutation_scale=10))
    ax.annotate('', xy=(80, 34), xytext=(80, 45.5), arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.3, mutation_scale=10))

    # Dual-Provenance KG Box
    kg_box = patches.FancyBboxPatch((4, 18), 52, 16, boxstyle="round,pad=0.5,rounding_size=1.5",
                                     facecolor="#FAF7F2", edgecolor="#C86D51", linewidth=1.8)
    ax.add_patch(kg_box)
    ax.text(30, 30.5, "Dual-Provenance KG (CIDOC-CRM E13)", ha='center', va='center', fontsize=10, fontweight='bold', fontfamily='serif', color='#C86D51')
    ax.text(30, 24, "• Retains Archival & Oral Accounts Side-by-Side\n• Reliability Tiers (A/B/C) & Modality Metadata\n• Embedded NetworkX & Neo4j Schema",
            ha='center', va='center', fontsize=7.8, fontfamily='serif', color='#334155')

    # Community Review Box
    rev_box = patches.FancyBboxPatch((60, 18), 46, 16, boxstyle="round,pad=0.5,rounding_size=1.5",
                                      facecolor="#F0FDF4", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(rev_box)
    ax.text(83, 30.5, "Community Review Desk & Sovereignty", ha='center', va='center', fontsize=10, fontweight='bold', fontfamily='serif', color='#166534')
    ax.text(83, 24, "• Additive (Non-Destructive) Elder Adjudication\n• Indigenous Data Sovereignty Access Matrix\n• Access: Public / Restricted / Sacred-Private",
            ha='center', va='center', fontsize=7.8, fontfamily='serif', color='#334155')

    # Bottom Arrow to GraphRAG & UI
    ax.annotate('', xy=(55, 10), xytext=(30, 17.5), arrowprops=dict(arrowstyle="-|>", color="#2D5A4C", lw=1.4, mutation_scale=10))
    ax.annotate('', xy=(55, 10), xytext=(83, 17.5), arrowprops=dict(arrowstyle="-|>", color="#2D5A4C", lw=1.4, mutation_scale=10))

    # Bottom Delivery Layer
    ui_box = patches.FancyBboxPatch((12, 1), 86, 9, boxstyle="round,pad=0.4,rounding_size=1.2",
                                     facecolor="#18222F", edgecolor="#D4A373", linewidth=1.5)
    ax.add_patch(ui_box)
    ax.text(55, 5.5, "Cross-Lingual Multimodal GraphRAG & Client UI (FastAPI + Streamlit)",
            ha='center', va='center', fontsize=10, fontweight='bold', fontfamily='serif', color='#FAF7F2')

    save_diagram(fig, "diagram2_multimodal_architecture.png")

# =============================================================================
# DIAGRAM 3: DIVERGENCE-FLAG PROTOCOL & CIDOC-CRM E13 DECISION TREE
# =============================================================================
def generate_diagram3():
    fig, ax = plt.subplots(figsize=(10, 6.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "The Divergence-Flag Protocol: CIDOC-CRM E13 Decision Tree",
            ha='center', va='center', fontsize=12.5, fontweight='bold', fontfamily='serif', color='#18222F')

    # Step 1: Input
    b1 = patches.FancyBboxPatch((25, 82), 50, 9, boxstyle="round,pad=0.4,rounding_size=1.2",
                                 facecolor="#F1F5F9", edgecolor="#64748B", linewidth=1.4)
    ax.add_patch(b1)
    ax.text(50, 86.5, "Candidate Claim Extraction: (Entity, Relation, Claim Value, Source)",
            ha='center', va='center', fontsize=9, fontweight='bold', fontfamily='serif', color='#1E293B')

    # Arrow down
    ax.annotate('', xy=(50, 72), xytext=(50, 81.5), arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.4, mutation_scale=10))

    # Step 2: Existing Attribute Check
    b2 = patches.FancyBboxPatch((22, 62), 56, 10, boxstyle="round,pad=0.4,rounding_size=1.2",
                                 facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.4)
    ax.add_patch(b2)
    ax.text(50, 68, "Semantic Distance Scoring vs Existing Claims", ha='center', va='center', fontsize=9.5, fontweight='bold', fontfamily='serif', color='#92400E')
    ax.text(50, 64, "Compute embedding distance d(c_new, c_exist) & temporal interval overlap", ha='center', va='center', fontsize=7.8, fontfamily='serif', color='#78350F')

    # 3 Decision Branches
    # Left Branch: Agreement (None)
    ax.annotate('', xy=(18, 48), xytext=(35, 61.5), arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=1.3, mutation_scale=10))
    ax.text(20, 56, "d < 0.25 (Match)", fontsize=7.5, fontweight='bold', color='#16A34A', rotation=30)
    b_none = patches.FancyBboxPatch((4, 34), 28, 14, boxstyle="round,pad=0.4,rounding_size=1.2",
                                     facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=1.4)
    ax.add_patch(b_none)
    ax.text(18, 44, "Grade: NONE\n(Agreement)", ha='center', va='center', fontsize=9, fontweight='bold', fontfamily='serif', color='#166534')
    ax.text(18, 38, "Corroborates existing claim.\nAdds source citation tier.", ha='center', va='center', fontsize=7.2, fontfamily='serif', color='#14532D')

    # Middle Branch: Soft Divergence
    ax.annotate('', xy=(50, 48), xytext=(50, 61.5), arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=1.3, mutation_scale=10))
    ax.text(52, 55, "0.25 <= d < 0.55", fontsize=7.5, fontweight='bold', color='#D97706')
    b_soft = patches.FancyBboxPatch((36, 34), 28, 14, boxstyle="round,pad=0.4,rounding_size=1.2",
                                     facecolor="#FEF9C3", edgecolor="#CA8A04", linewidth=1.4)
    ax.add_patch(b_soft)
    ax.text(50, 44, "Grade: SOFT\n(Granularity Difference)", ha='center', va='center', fontsize=9, fontweight='bold', fontfamily='serif', color='#854D0E')
    ax.text(50, 38, "e.g. Month vs exact day.\nPreserves both with notes.", ha='center', va='center', fontsize=7.2, fontfamily='serif', color='#713F12')

    # Right Branch: Hard Divergence
    ax.annotate('', xy=(82, 48), xytext=(65, 61.5), arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=1.3, mutation_scale=10))
    ax.text(76, 56, "d >= 0.55 (Conflict)", fontsize=7.5, fontweight='bold', color='#DC2626', rotation=-30)
    b_hard = patches.FancyBboxPatch((68, 34), 28, 14, boxstyle="round,pad=0.4,rounding_size=1.2",
                                     facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=1.4)
    ax.add_patch(b_hard)
    ax.text(82, 44, "Grade: HARD\n(Contradictory)", ha='center', va='center', fontsize=9, fontweight='bold', fontfamily='serif', color='#991B1B')
    ax.text(82, 38, "e.g. 33 CE vs 16th c.\nTriggers Dual Perspective.", ha='center', va='center', fontsize=7.2, fontfamily='serif', color='#7F1D1D')

    # Final Convergence: Storage & Presentation
    ax.annotate('', xy=(50, 20), xytext=(18, 33.5), arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.2, mutation_scale=10))
    ax.annotate('', xy=(50, 20), xytext=(50, 33.5), arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.2, mutation_scale=10))
    ax.annotate('', xy=(50, 20), xytext=(82, 33.5), arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.2, mutation_scale=10))

    b_final = patches.FancyBboxPatch((15, 4), 70, 16, boxstyle="round,pad=0.5,rounding_size=1.5",
                                      facecolor="#18222F", edgecolor="#D4A373", linewidth=1.5)
    ax.add_patch(b_final)
    ax.text(50, 15, "CIDOC-CRM E13 Attribute Assignment & Grounded RAG Delivery",
            ha='center', va='center', fontsize=9.5, fontweight='bold', fontfamily='serif', color='#FAF7F2')
    ax.text(50, 9, "• Stores claims in E13 nodes linked to original sources (Tier A/B/C) without overwriting.\n• GraphRAG generates side-by-side Dual-Perspective Cards rather than picking a single winner.",
            ha='center', va='center', fontsize=7.8, fontfamily='serif', color='#CBD5E1')

    save_diagram(fig, "diagram3_divergence_protocol.png")

# =============================================================================
# DIAGRAM 4: MULTIMODAL CROSS-VALIDATION & CORROBORATION CYCLE
# =============================================================================
def generate_diagram4():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "Multimodal Cross-Validation, Corroboration & Community Review Cycle",
            ha='center', va='center', fontsize=12.5, fontweight='bold', fontfamily='serif', color='#18222F')

    # Central Cross-Validation Hub
    hub_circle = patches.Circle((50, 52), 16, facecolor="#F1ECE1", edgecolor="#C86D51", linewidth=2.0)
    ax.add_patch(hub_circle)
    ax.text(50, 55, "Cross-Modal\nCorroboration\nHub", ha='center', va='center', fontsize=10, fontweight='bold', fontfamily='serif', color='#C86D51')
    ax.text(50, 44, "Joint Consistency\nMetric S_joint", ha='center', va='center', fontsize=7.5, fontfamily='serif', color='#334155')

    # Modality Nodes orbiting around
    nodes = [
        {"x": 18, "y": 78, "title": "Manuscript HTR", "desc": "Textual Claim in Puya", "bg": "#FCE7F3", "bdr": "#BE185D"},
        {"x": 82, "y": 78, "title": "Monument VLM", "desc": "Visual Iconography Tag", "bg": "#FEF3C7", "bdr": "#D97706"},
        {"x": 18, "y": 26, "title": "Oral ASR Recording", "desc": "Priestly Chants / Elder Lore", "bg": "#D1FAE5", "bdr": "#047857"},
        {"x": 82, "y": 26, "title": "Archival Surveys", "desc": "Colonial Gazetteers / Records", "bg": "#E0E7FF", "bdr": "#4338CA"}
    ]

    for n in nodes:
        box = patches.FancyBboxPatch((n["x"] - 14, n["y"] - 7), 28, 14, boxstyle="round,pad=0.4,rounding_size=1.2",
                                      facecolor=n["bg"], edgecolor=n["bdr"], linewidth=1.4)
        ax.add_patch(box)
        ax.text(n["x"], n["y"] + 2, n["title"], ha='center', va='center', fontsize=8.8, fontweight='bold', fontfamily='serif', color='#18222F')
        ax.text(n["x"], n["y"] - 3, n["desc"], ha='center', va='center', fontsize=7.2, fontfamily='serif', color='#475569')

        # Two-way arrows to hub
        ax.annotate('', xy=(50 + (n["x"]-50)*0.45, 52 + (n["y"]-52)*0.45), xytext=(n["x"] - (n["x"]-50)*0.25, n["y"] - (n["y"]-52)*0.25),
                    arrowprops=dict(arrowstyle="<|-|>", color="#64748B", lw=1.3, mutation_scale=10))

    # Bottom Review & Sovereignty Action
    act_box = patches.FancyBboxPatch((20, 2), 60, 9, boxstyle="round,pad=0.4,rounding_size=1.2",
                                      facecolor="#18222F", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(act_box)
    ax.text(50, 6.5, "Community Review Queue: Additive Annotation & Access Level Control",
            ha='center', va='center', fontsize=8.5, fontweight='bold', fontfamily='serif', color='#FAF7F2')

    save_diagram(fig, "diagram4_cross_modal_validation.png")

if __name__ == "__main__":
    generate_diagram1()
    generate_diagram2()
    generate_diagram3()
    generate_diagram4()
    print("All 4 academic data diagrams generated successfully!")
