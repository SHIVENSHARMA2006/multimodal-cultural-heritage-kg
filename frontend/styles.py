"""
Cultural Heritage UI Styling and Design System.
Defines soothing heritage color palettes, typography, responsive card layouts,
and high-contrast accessible styling for tabs, sidebars, buttons, and expanders.
"""

HERITAGE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,700;1,400&family=Noto+Sans+Meetei+Mayek:wght@400;700&display=swap');

:root {
    --primary-slate: #18222F;
    --terracotta: #C86D51;
    --temple-gold: #D4A373;
    --temple-gold-bright: #E2B653;
    --sacred-jade: #2D5A4C;
    --parchment-bg: #FAF7F2;
    --card-surface: #FFFFFF;
    --border-soft: #E5DFD5;
    --text-primary: #18222F;
    --text-muted: #64748B;
}

/* Base Canvas */
.stApp {
    background-color: var(--parchment-bg) !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-primary);
}

/* Ensure headings and body paragraphs use clean fonts without breaking icon glyphs */
h1, h2, h3, h4, h5, h6, p, li, label {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-primary);
}

/* =========================================================================
   1. TABS: FONT COLOR INITIALLY (BEFORE HOVER) & ACTIVE STATES
   ========================================================================= */
/* Tab Bar Container */
[data-baseweb="tab-list"], [data-testid="stTabs"] {
    background: #F0EAE1 !important;
    padding: 6px 8px !important;
    border-radius: 12px !important;
    gap: 8px !important;
    border: 1px solid #DFD5C6 !important;
    margin-bottom: 1.2rem !important;
}

/* Inactive Tab Buttons (INITIAL STATE BEFORE HOVER) - Crisp, dark, high-contrast */
button[data-baseweb="tab"], [data-testid="stTabs"] [role="tab"] {
    color: #2C3E50 !important;
    background-color: #E6DED2 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border-radius: 8px !important;
    padding: 9px 18px !important;
    border: 1px solid #D8CDBD !important;
    transition: all 0.2s ease-in-out !important;
}

button[data-baseweb="tab"] p, 
button[data-baseweb="tab"] div, 
button[data-baseweb="tab"] span {
    color: #2C3E50 !important;
    font-weight: 600 !important;
}

/* Tab Hover State */
button[data-baseweb="tab"]:hover, [data-testid="stTabs"] [role="tab"]:hover {
    color: #FFFFFF !important;
    background-color: var(--temple-gold) !important;
    border-color: var(--temple-gold) !important;
}

button[data-baseweb="tab"]:hover p,
button[data-baseweb="tab"]:hover span {
    color: #FFFFFF !important;
}

/* Tab Active / Selected State */
button[data-baseweb="tab"][aria-selected="true"], 
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
    background-color: var(--terracotta) !important;
    border-color: #B0553A !important;
    box-shadow: 0 3px 10px rgba(200, 109, 81, 0.3) !important;
}

button[data-baseweb="tab"][aria-selected="true"] p,
button[data-baseweb="tab"][aria-selected="true"] span {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* =========================================================================
   2. LEFT SIDEBAR (NAVIGATION & METRICS) HIGH-CONTRAST PALETTE
   ========================================================================= */
[data-testid="stSidebar"] {
    background-color: #18222F !important;
    border-right: 1.5px solid rgba(212, 163, 115, 0.25) !important;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC;
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h4 {
    color: #FAF7F2 !important;
    font-family: 'Cinzel', serif !important;
}

/* Sidebar Navigation Radio Buttons */
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stRadio p,
[data-testid="stSidebar"] .stRadio span {
    color: #E2E8F0 !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    padding: 8px 12px !important;
    border-radius: 8px !important;
    margin-bottom: 4px !important;
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: rgba(212, 163, 115, 0.18) !important;
    border-color: rgba(212, 163, 115, 0.3) !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover p,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover span {
    color: var(--temple-gold-bright) !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] {
    background: rgba(200, 109, 81, 0.3) !important;
    border-left: 4px solid var(--terracotta) !important;
    border-color: rgba(200, 109, 81, 0.5) !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] p,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] span {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Sidebar Metrics & Numbers */
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: var(--temple-gold-bright) !important;
    font-family: 'Cinzel', serif !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
    font-size: 0.85rem !important;
}

[data-testid="stSidebar"] code {
    background: rgba(255, 255, 255, 0.12) !important;
    color: var(--temple-gold-bright) !important;
    border: 1px solid rgba(226, 182, 83, 0.4) !important;
    font-weight: 700 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}

/* =========================================================================
   3. SAMPLE QUERY BUTTONS & INQUIRY CARDS (HIGH-CONTRAST & READABLE)
   ========================================================================= */
.stButton > button, [data-testid="stButton"] button {
    background: #FFFFFF !important;
    color: #18222F !important;
    border: 1.5px solid #C86D51 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04) !important;
    transition: all 0.2s ease-in-out !important;
}

.stButton > button p, 
.stButton > button span,
[data-testid="stButton"] button p,
[data-testid="stButton"] button span {
    color: #18222F !important;
    font-weight: 600 !important;
}

.stButton > button:hover, [data-testid="stButton"] button:hover {
    background: #C86D51 !important;
    border-color: #B0553A !important;
    box-shadow: 0 4px 12px rgba(200, 109, 81, 0.25) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:hover p,
.stButton > button:hover span,
[data-testid="stButton"] button:hover p,
[data-testid="stButton"] button:hover span {
    color: #FFFFFF !important;
}

/* =========================================================================
   4. FORM CONTROLS: TEXT INPUTS, SELECTBOXES & DROPDOWNS
   ========================================================================= */
.stTextInput input, .stTextArea textarea {
    background: #FFFFFF !important;
    color: #18222F !important;
    border: 1.5px solid #C86D51 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-size: 1rem !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03) !important;
}

.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #94A3B8 !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--sacred-jade) !important;
    box-shadow: 0 0 0 3px rgba(45, 90, 76, 0.2) !important;
}

.stTextInput label, .stTextArea label, .stSelectbox label {
    color: #18222F !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* Selectbox dropdowns */
[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #18222F !important;
    border: 1.5px solid #D4A373 !important;
    border-radius: 10px !important;
}

[data-baseweb="select"] span, [data-baseweb="select"] div {
    color: #18222F !important;
}

/* Inline code tags & script chips */
code {
    background: #F1ECE1 !important;
    color: #C86D51 !important;
    border: 1px solid #E2D7C8 !important;
    border-radius: 6px !important;
    padding: 2px 8px !important;
    font-weight: 700 !important;
}

/* =========================================================================
   5. EXPANDER FIX (PREVENTS '_arrow_right' LIGATURE CORRUPTION)
   ========================================================================= */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1.5px solid #E5DFD5 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
    overflow: hidden !important;
    margin-top: 1rem !important;
}

[data-testid="stExpander"] summary {
    background: #FAF7F2 !important;
    color: #18222F !important;
    font-weight: 600 !important;
    padding: 12px 18px !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary:hover {
    color: #C86D51 !important;
    background: #F4EFEA !important;
}

[data-testid="stExpander"] summary p {
    color: #18222F !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin: 0 !important;
}

/* Ensure expander arrow icon font is preserved and never broken */
[data-testid="stExpanderToggleIcon"] {
    color: #C86D51 !important;
}

[data-testid="stExpanderToggleIcon"] svg {
    fill: #C86D51 !important;
}

/* Top Banner with Cultural Heritage Aesthetics */
.heritage-header {
    background: linear-gradient(135deg, #18222F 0%, #2A3B4C 50%, #1A2826 100%);
    border-bottom: 4px solid var(--temple-gold);
    border-radius: 14px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(24, 34, 47, 0.15);
    color: #FAF7F2;
    position: relative;
    overflow: hidden;
}

.heritage-header::after {
    content: "ꯀꯪꯂꯩꯄꯥꯛ";
    position: absolute;
    right: 20px;
    bottom: -15px;
    font-size: 5rem;
    font-family: 'Noto Sans Meetei Mayek', serif;
    color: rgba(212, 163, 115, 0.08);
    pointer-events: none;
    font-weight: 700;
}

.heritage-title {
    font-family: 'Cinzel', serif;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #F8F5EE;
    margin: 0;
}

.heritage-subtitle {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    color: var(--temple-gold);
    font-size: 1.15rem;
    margin-top: 0.4rem;
}

.heritage-desc {
    color: #CBD5E1;
    font-size: 0.95rem;
    margin-top: 0.8rem;
    max-width: 900px;
    line-height: 1.5;
}

/* Modality Badges */
.modality-badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.modality-text { background: #E0E7FF; color: #3730A3; }
.modality-image { background: #FEF3C7; color: #92400E; }
.modality-audio { background: #D1FAE5; color: #065F46; }
.modality-manuscript { background: #FCE7F3; color: #9D174D; }

/* Dual-Perspective Conflict Cards */
.divergence-card-container {
    display: flex;
    gap: 1.2rem;
    margin: 1.5rem 0;
}

.perspective-card {
    flex: 1;
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1.4rem;
    border: 1px solid var(--border-soft);
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    position: relative;
}

.perspective-a {
    border-top: 4px solid var(--terracotta);
}

.perspective-b {
    border-top: 4px solid var(--sacred-jade);
}

.perspective-badge {
    position: absolute;
    top: -12px;
    right: 16px;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: bold;
    color: white;
}

.badge-a { background: var(--terracotta); }
.badge-b { background: var(--sacred-jade); }

/* Meetei Mayek script highlights */
.meitei-glyph {
    font-family: 'Noto Sans Meetei Mayek', sans-serif;
    color: var(--terracotta);
    font-weight: 700;
}

/* Metric Display Cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    border: 1px solid var(--border-soft) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
}

[data-testid="stMetricValue"] {
    color: var(--terracotta) !important;
    font-family: 'Cinzel', serif !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: #475569 !important;
    font-weight: 600 !important;
}

/* =========================================================================
   6. BESPOKE CULTURAL HERITAGE ANSWER CARD
   ========================================================================= */
.heritage-answer-card {
    background: #FFFFFF;
    border: 1px solid #E2D7C8;
    border-top: 5px solid var(--sacred-jade);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    margin-bottom: 1.8rem;
}

.answer-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #F1ECE1;
    padding-bottom: 0.8rem;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
    gap: 10px;
}

.entity-title-group {
    display: flex;
    align-items: center;
    gap: 12px;
}

.entity-name-text {
    font-family: 'Cinzel', serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--primary-slate);
    margin: 0;
}

.meitei-script-pill {
    background: #FDF4EB;
    color: var(--terracotta);
    border: 1px solid rgba(200, 109, 81, 0.3);
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 1rem;
    font-family: 'Noto Sans Meetei Mayek', sans-serif;
    font-weight: 700;
}

.entity-type-badge {
    background: #EDF3F1;
    color: var(--sacred-jade);
    border: 1px solid rgba(45, 90, 76, 0.2);
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.verified-pill {
    background: #D1FAE5;
    color: #065F46;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}

.answer-lead-box {
    background: #FAF7F2;
    border: 1px solid #EFE8DD;
    border-left: 4px solid var(--terracotta);
    border-radius: 8px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1.2rem;
    font-size: 1.15rem;
    color: var(--primary-slate);
    line-height: 1.6;
    font-weight: 500;
}

.answer-lead-box strong {
    color: var(--terracotta);
    font-weight: 700;
}

.evidence-quote-box {
    background: #FFFFFF;
    border: 1px solid #EAE4D9;
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 1.2rem;
    display: flex;
    gap: 12px;
}

.quote-glyph {
    font-size: 2.2rem;
    line-height: 1;
    color: var(--temple-gold);
    font-family: 'Cinzel', serif;
}

.quote-body-text {
    font-style: italic;
    color: #475569;
    font-size: 0.95rem;
    line-height: 1.5;
    margin: 0;
}

.quote-source-caption {
    font-size: 0.82rem;
    color: #94A3B8;
    margin-top: 0.4rem;
    display: block;
    font-style: normal;
}

.citation-tray {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    padding-top: 0.6rem;
    border-top: 1px dashed #E2D7C8;
}

.citation-tray-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-right: 4px;
}

.citation-link-badge {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.82rem;
    color: var(--primary-slate);
    text-decoration: none;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.citation-link-badge:hover {
    background: var(--terracotta);
    border-color: var(--terracotta);
    color: #FFFFFF !important;
}

.citation-link-badge:hover span {
    color: #FFFFFF !important;
}

.citation-link-badge:hover .tier-badge {
    background: rgba(255, 255, 255, 0.25) !important;
    color: #FFFFFF !important;
}

.tier-badge {
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 700;
    background: #E2E8F0;
    color: #334155;
}

/* =========================================================================
   7. NOVELTY & INTERACTIVE EXPERIENCE ENHANCEMENTS
   ========================================================================= */

/* Virtual Walking Tour Cards */
.tour-waypoint-card {
    background: #FFFFFF;
    border: 1px solid #E2D7C8;
    border-top: 5px solid var(--terracotta);
    border-radius: 14px;
    padding: 1.8rem;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.05);
    margin-bottom: 2rem;
}

.tour-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #F1ECE1;
    padding-bottom: 0.8rem;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
    gap: 12px;
}

.tour-step-pill {
    background: #FEF3C7;
    color: #92400E;
    border: 1px solid #FDE68A;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.tour-gps-pill {
    background: #F1F5F9;
    color: #475569;
    border: 1px solid #E2E8F0;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-family: monospace;
}

.tour-oral-tradition-box {
    background: #F8FAFC;
    border-left: 4px solid var(--sacred-jade);
    padding: 0.9rem 1.2rem;
    border-radius: 6px;
    margin: 1rem 0;
    font-size: 0.92rem;
    color: #334155;
}

/* Meetei Mayek Anatomical Studio */
.mayek-anatomy-card {
    background: #FFFFFF;
    border: 1px solid #E2D7C8;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    margin-bottom: 1rem;
    position: relative;
}

.mayek-anatomy-card:hover {
    transform: translateY(-3px);
    border-color: var(--terracotta);
    box-shadow: 0 8px 20px rgba(200, 109, 81, 0.15);
}

.mayek-char-display {
    font-size: 2.8rem;
    color: var(--terracotta);
    font-family: 'Noto Sans Meetei Mayek', sans-serif;
    font-weight: 700;
    line-height: 1.1;
}

.mayek-anatomy-badge {
    background: #EDF3F1;
    color: var(--sacred-jade);
    padding: 2px 8px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
    margin: 4px 0;
}

.mayek-translit-box {
    background: #FAF7F2;
    border: 1.5px solid #D4A373;
    border-radius: 12px;
    padding: 1.4rem;
    margin: 1.2rem 0;
}

/* Folklore Storytelling Lounge */
.folklore-card {
    background: #FFFFFF;
    border: 1px solid #E2D7C8;
    border-left: 6px solid var(--sacred-jade);
    border-radius: 14px;
    padding: 1.8rem;
    box-shadow: 0 4px 18px rgba(0,0,0,0.04);
    margin-bottom: 2rem;
}

.folklore-bilingual-panel {
    background: #FAF7F2;
    border: 1px solid #EFE8DD;
    border-radius: 8px;
    padding: 1.1rem 1.3rem;
    margin: 1rem 0;
}

.folklore-moral-callout {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #166534;
    font-size: 0.95rem;
    margin-top: 1rem;
}

/* Historical Timeline Cards */
.timeline-card {
    background: #FFFFFF;
    border: 1px solid #E2D7C8;
    border-top: 4px solid var(--temple-gold);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 3px 12px rgba(0,0,0,0.03);
    transition: all 0.2s ease;
}

.timeline-card:hover {
    border-top-color: var(--terracotta);
    box-shadow: 0 6px 20px rgba(0,0,0,0.07);
}

.timeline-year-pill {
    background: #18222F;
    color: var(--temple-gold-bright);
    font-family: 'Cinzel', serif;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.9rem;
    display: inline-block;
}

.timeline-divergence-pill {
    background: #FEF2F2;
    color: #B91C1C;
    border: 1px solid #FECACA;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
}

/* Gamified Heritage Quest */
.quiz-container {
    background: #FFFFFF;
    border: 1.5px solid #E2D7C8;
    border-radius: 14px;
    padding: 1.8rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
}

.quiz-score-banner {
    background: linear-gradient(135deg, #18222F 0%, #2D5A4C 100%);
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    color: #FAF7F2;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.quiz-badge-rank {
    background: var(--temple-gold-bright);
    color: #18222F;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
</style>
"""
