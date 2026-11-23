import os
import subprocess
import base64
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH

def convert_docx_to_html_and_pdf():
    print("Reading Multimodal_Cultural_Heritage_NLP_Project_Report.docx...")
    doc = docx.Document('Multimodal_Cultural_Heritage_NLP_Project_Report.docx')
    
    # Pre-encode diagrams as base64 so HTML is completely standalone
    diagram_b64 = {}
    assets_dir = 'report_assets'
    if os.path.exists(assets_dir):
        for f in os.listdir(assets_dir):
            if f.endswith('.png'):
                with open(os.path.join(assets_dir, f), 'rb') as img_f:
                    diagram_b64[f] = base64.b64encode(img_f.read()).decode('utf-8')

    html_parts = []
    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Multimodal Cultural Heritage Knowledge Graph - Project Report</title>
<style>
@page {
    size: A4 portrait;
    margin-top: 25mm;
    margin-bottom: 25mm;
    margin-left: 38mm;
    margin-right: 22mm;
    @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", Times, serif;
        font-size: 10pt;
        color: #64748B;
    }
}
@media print {
    body {
        margin: 0;
        padding: 0;
        background: #ffffff;
    }
    .page-break {
        page-break-before: always;
        break-before: page;
    }
    .no-print {
        display: none !important;
    }
    .report-container {
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
}
body {
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #18222F;
    background: #F1F5F9;
    margin: 0;
    padding: 20px 0;
}
.report-container {
    max-width: 210mm;
    margin: 0 auto;
    background: #ffffff;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    padding: 25mm 22mm 25mm 38mm;
    box-sizing: border-box;
}
.download-bar {
    position: sticky;
    top: 0;
    background: #18222F;
    color: #FAFAF9;
    padding: 12px 24px;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.download-bar a, .download-bar button {
    background: #C86D51;
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    font-size: 14px;
    margin-left: 8px;
    display: inline-block;
}
.download-bar a:hover, .download-bar button:hover {
    background: #A0523D;
}
h1 {
    font-size: 16pt;
    font-weight: bold;
    color: #18222F;
    margin-top: 28px;
    margin-bottom: 14px;
    page-break-after: avoid;
}
h2 {
    font-size: 14pt;
    font-weight: bold;
    color: #2D5A4C;
    margin-top: 20px;
    margin-bottom: 8px;
    page-break-after: avoid;
}
h3 {
    font-size: 12pt;
    font-weight: bold;
    color: #C86D51;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
}
p {
    font-size: 12pt;
    line-height: 1.5;
    text-align: justify;
    margin-top: 0;
    margin-bottom: 8px;
}
.title-cover {
    text-align: center;
    padding-top: 50px;
    padding-bottom: 60px;
}
.title-cover h1 {
    font-size: 24pt;
    line-height: 1.3;
    font-weight: bold;
    color: #18222F;
    margin-bottom: 18px;
}
.title-cover .subtitle {
    font-size: 14pt;
    font-style: italic;
    color: #C86D51;
    margin-bottom: 40px;
}
.title-cover .meta-block {
    font-size: 12pt;
    color: #334155;
    line-height: 1.6;
    margin-top: 40px;
}
.preliminary-header {
    text-align: center;
    font-size: 16pt;
    font-weight: bold;
    color: #18222F;
    margin-top: 30px;
    margin-bottom: 24px;
}
.signature-block {
    text-align: right;
    margin-top: 60px;
    line-height: 1.5;
    font-size: 11pt;
}
table.report-table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 10pt;
    page-break-inside: avoid;
}
table.report-table th {
    background-color: #18222F;
    color: #FAF7F2;
    padding: 8px 10px;
    text-align: center;
    font-weight: bold;
    border-top: 1px solid #18222F;
    border-bottom: 1px solid #18222F;
}
table.report-table td {
    padding: 7px 10px;
    border-top: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
    color: #1E293B;
    line-height: 1.3;
}
table.report-table tr:nth-child(even) td {
    background-color: #FAF7F2;
}
.placeholder-box {
    border: 2px double #C86D51;
    background-color: #FAF7F2;
    padding: 20px;
    margin: 18px 0;
    text-align: center;
    border-radius: 4px;
    page-break-inside: avoid;
}
.placeholder-tag {
    font-size: 12pt;
    font-weight: bold;
    color: #C86D51;
    margin-bottom: 6px;
}
.placeholder-title {
    font-size: 11pt;
    font-weight: bold;
    color: #18222F;
    margin-bottom: 10px;
}
.placeholder-desc {
    font-size: 10pt;
    font-style: italic;
    color: #334155;
    margin-bottom: 10px;
}
.placeholder-inst {
    font-size: 9.5pt;
    color: #64748B;
    border-top: 1px dashed #CBD5E1;
    padding-top: 8px;
    line-height: 1.4;
}
.figure-container {
    text-align: center;
    margin: 20px 0;
    page-break-inside: avoid;
}
.figure-container img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    border: 1px solid #E2E8F0;
}
.figure-caption {
    font-size: 10.5pt;
    font-style: italic;
    color: #334155;
    margin-top: 6px;
    margin-bottom: 16px;
    text-align: center;
}
.figure-caption strong {
    font-style: normal;
    color: #18222F;
}
.page-break {
    page-break-before: always;
    break-before: page;
}
</style>
</head>
<body>

<div class="download-bar no-print">
    <div>
        <strong>Multimodal Cultural Heritage Knowledge Graph Report</strong>
        <span style="opacity: 0.8; font-size: 12px; margin-left: 12px;">(Manipuri / Meitei Pilot • 38 Pages)</span>
    </div>
    <div>
        <a href="/download/report.docx" download="Multimodal_Cultural_Heritage_NLP_Project_Report.docx">📥 Download Word (.docx)</a>
        <a href="/download/report.pdf" download="Multimodal_Cultural_Heritage_NLP_Project_Report.pdf">📄 Download PDF (.pdf)</a>
        <button onclick="window.print()">🖨️ Print / Save as PDF</button>
    </div>
</div>

<div class="report-container">
""")

    # Walk through document body
    # We will map paragraphs and tables
    # In python-docx, doc.element.body iterates children in document order!
    from docx.oxml.text.paragraph import CT_P
    from docx.oxml.table import CT_Tbl
    from docx.text.paragraph import Paragraph
    from docx.table import Table

    diagram_map = {
        "Figure 1: ": "diagram1_nlp_lifecycle.png",
        "Figure 2: ": "diagram2_multimodal_architecture.png",
        "Figure 4: ": "diagram3_divergence_protocol.png",
        "Figure 6: ": "diagram4_cross_modal_validation.png",
    }

    body = doc._body._body
    in_cover = True

    for child in body:
        if isinstance(child, CT_P):
            p = Paragraph(child, doc)
            text = p.text.strip()
            if not text:
                continue
            
            # Check for page break run
            has_page_break = any('lastRenderedPageBreak' in r._r.xml or 'w:br' in r._r.xml for r in p.runs)

            # Headings detection
            if text.startswith("MULTIMODAL CULTURAL HERITAGE KNOWLEDGE GRAPH"):
                html_parts.append(f'<div class="title-cover"><h1>{text}</h1>')
                continue
            elif text.startswith("A CIDOC-CRM Aligned GraphRAG System"):
                html_parts.append(f'<div class="subtitle">{text.replace(chr(10), "<br>")}</div>')
                continue
            elif text.startswith("A CAPSTONE PROJECT REPORT"):
                html_parts.append(f'<div style="font-weight:bold; font-size:11.5pt; margin-top:20px;">{text.replace(chr(10), "<br>")}</div>')
                continue
            elif text.startswith("Submitted by:"):
                html_parts.append(f'<div class="meta-block">{text.replace(chr(10), "<br>")}</div></div><div class="page-break"></div>')
                in_cover = False
                continue
            
            # Preliminary headings
            if text in ["CERTIFICATE OF ENDORSEMENT", "STUDENT DECLARATION", "ACKNOWLEDGEMENTS", "ABSTRACT", "TABLE OF CONTENTS", "LIST OF TABLES", "LIST OF FIGURES"]:
                html_parts.append(f'<div class="page-break"></div><div class="preliminary-header">{text}</div>')
                continue

            # Chapters (H1)
            if text.startswith("CHAPTER ") or text in ["REFERENCES", "APPENDIX A: GOLD QUESTION-ANSWERING BENCHMARK", "APPENDIX B: CURATED CULTURAL DIVERGENCE CATALOG", "APPENDIX C: MEETEI MAYEK IYEK 27 ALPHABET & SOUND MAPPINGS", "APPENDIX D: REST API OPENAPI SPECIFICATION SUMMARY"]:
                html_parts.append(f'<div class="page-break"></div><h1>{text}</h1>')
                continue

            # Headings (H2)
            if len(text) > 3 and text[:3].replace('.', '').isdigit() and ' ' in text[:5]:
                html_parts.append(f'<h2>{text}</h2>')
                continue

            # Headings (H3)
            if len(text) > 5 and text[:5].count('.') == 2 and ' ' in text[:8]:
                html_parts.append(f'<h3>{text}</h3>')
                continue

            # Signatures
            if "_______________________________" in text:
                html_parts.append(f'<div class="signature-block">{text.replace(chr(10), "<br>")}</div>')
                continue

            # Captions for figures
            if text.startswith("Figure "):
                # Check if this is one of our 4 embedded diagrams
                fig_key = text[:10]
                matched_diagram = None
                for k, v in diagram_map.items():
                    if text.startswith(k):
                        matched_diagram = v
                        break
                
                if matched_diagram and matched_diagram in diagram_b64:
                    img_data = diagram_b64[matched_diagram]
                    html_parts.append(f'''
                    <div class="figure-container">
                        <img src="data:image/png;base64,{img_data}" alt="{text}">
                        <div class="figure-caption"><strong>{text.split(":")[0]}:</strong> {":".join(text.split(":")[1:]) if ":" in text else ""}</div>
                    </div>''')
                else:
                    html_parts.append(f'<div class="figure-caption"><strong>{text.split(":")[0]}:</strong> {":".join(text.split(":")[1:]) if ":" in text else ""}</div>')
                continue

            # Normal paragraphs
            # Preserve bold prefix if run 0 is bold
            p_html = ""
            for run in p.runs:
                r_text = run.text
                if not r_text:
                    continue
                # HTML escape
                r_text = r_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                if run.bold and run.italic:
                    p_html += f"<strong><em>{r_text}</em></strong>"
                elif run.bold:
                    p_html += f"<strong>{r_text}</strong>"
                elif run.italic:
                    p_html += f"<em>{r_text}</em>"
                else:
                    p_html += r_text
            
            html_parts.append(f'<p>{p_html}</p>')

        elif isinstance(child, CT_Tbl):
            tbl = Table(child, doc)
            # Check if this table is a screenshot placeholder (1 row, 1 col)
            if len(tbl.rows) == 1 and len(tbl.columns) == 1:
                cell_text = tbl.rows[0].cells[0].text
                if "[ SCREENSHOT PLACEHOLDER:" in cell_text:
                    lines = [l.strip() for l in cell_text.split('\n') if l.strip()]
                    tag = lines[0] if len(lines) > 0 else ""
                    title = lines[1] if len(lines) > 1 else ""
                    desc = ""
                    inst = ""
                    for line in lines[2:]:
                        if line.startswith("Description:"):
                            desc = line
                        elif line.startswith("Instructions for Submission:"):
                            inst = line
                        elif desc and not inst:
                            desc += " " + line
                        elif inst:
                            inst += " " + line
                    
                    html_parts.append(f'''
                    <div class="placeholder-box">
                        <div class="placeholder-tag">{tag}</div>
                        <div class="placeholder-title">{title}</div>
                        <div class="placeholder-desc">{desc}</div>
                        <div class="placeholder-inst">{inst}</div>
                    </div>''')
                    continue

            # Standard Data Table
            t_html = ['<table class="report-table">']
            # Header
            t_html.append('<thead><tr>')
            for cell in tbl.rows[0].cells:
                t_html.append(f'<th>{cell.text.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</th>')
            t_html.append('</tr></thead><tbody>')
            
            # Rows
            for row in tbl.rows[1:]:
                t_html.append('<tr>')
                for cell in row.cells:
                    t_html.append(f'<td>{cell.text.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</td>')
                t_html.append('</tr>')
            t_html.append('</tbody></table>')
            html_parts.append('\n'.join(t_html))

    html_parts.append("""
</div>
</body>
</html>
""")

    output_html = "report_view.html"
    with open(output_html, "w", encoding="utf-8") as f:
        f.write('\n'.join(html_parts))
    print(f"HTML report successfully generated: {output_html} ({os.path.getsize(output_html)} bytes)")

    # Now generate PDF using Microsoft Edge headless
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        output_pdf = os.path.abspath("Multimodal_Cultural_Heritage_NLP_Project_Report.pdf")
        html_abs = os.path.abspath(output_html)
        cmd = [
            edge_path,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_pdf}",
            f"file:///{html_abs.replace(os.sep, '/')}"
        ]
        print("Rendering PDF via Microsoft Edge...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(output_pdf):
            print(f"PDF successfully created: {output_pdf} ({os.path.getsize(output_pdf)} bytes)")
        else:
            print("Edge PDF export returned:", res.stderr)

if __name__ == '__main__':
    convert_docx_to_html_and_pdf()
