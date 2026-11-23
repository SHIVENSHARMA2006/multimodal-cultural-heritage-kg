import os
import subprocess
import docx
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.text.paragraph import Paragraph
from docx.table import Table

def export_blueprint():
    docx_filename = "Comprehensive_System_Architecture_and_Engineering_Blueprint.docx"
    html_filename = "system_blueprint_view.html"
    pdf_filename = "Comprehensive_System_Architecture_and_Engineering_Blueprint.pdf"
    
    print(f"Reading {docx_filename}...")
    doc = docx.Document(docx_filename)

    html_parts = ["""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Technical Architecture & Engineering Specification Blueprint</title>
<style>
@page {
    size: A4 portrait;
    margin-top: 25mm;
    margin-bottom: 25mm;
    margin-left: 35mm;
    margin-right: 20mm;
}
@media print {
    body { margin: 0; padding: 0; background: #ffffff; }
    .page-break { page-break-before: always; break-before: page; }
    .no-print { display: none !important; }
    .report-container { box-shadow: none !important; padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
}
body {
    font-family: "Times New Roman", Times, serif;
    font-size: 11pt;
    line-height: 1.4;
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
    padding: 25mm 20mm 25mm 35mm;
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
.download-bar a:hover, .download-bar button:hover { background: #A0523D; }
h1 {
    font-size: 15pt;
    font-weight: bold;
    color: #18222F;
    margin-top: 26px;
    margin-bottom: 12px;
    page-break-after: avoid;
    border-bottom: 1.5px solid #E2E8F0;
    padding-bottom: 6px;
}
h2 {
    font-size: 13pt;
    font-weight: bold;
    color: #2D5A4C;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
}
h3 {
    font-size: 11.5pt;
    font-weight: bold;
    color: #C86D51;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
}
p {
    font-size: 11pt;
    line-height: 1.35;
    text-align: justify;
    margin-top: 0;
    margin-bottom: 7px;
}
.title-cover {
    text-align: center;
    padding-top: 40px;
    padding-bottom: 40px;
}
.title-cover h1 {
    font-size: 22pt;
    line-height: 1.25;
    font-weight: bold;
    color: #18222F;
    margin-bottom: 16px;
    border: none;
}
.title-cover .subtitle {
    font-size: 12.5pt;
    font-style: italic;
    color: #C86D51;
    margin-bottom: 30px;
}
.title-cover .meta-block {
    font-size: 10.5pt;
    color: #475569;
    line-height: 1.5;
    margin-top: 30px;
}
.callout-box {
    border-left: 5px solid #2D5A4C;
    background-color: #F1F5F9;
    padding: 14px 18px;
    margin: 14px 0;
    border-radius: 4px;
    page-break-inside: avoid;
}
.callout-box.architecture {
    border-left-color: #C86D51;
    background-color: #FAF7F2;
}
.callout-box .box-title {
    font-weight: bold;
    font-size: 11pt;
    color: #18222F;
    margin-bottom: 6px;
}
.callout-box .box-text {
    font-size: 10pt;
    color: #334155;
    line-height: 1.4;
}
.code-box {
    background-color: #18222F;
    border-left: 5px solid #C86D51;
    color: #FAFAF9;
    padding: 12px 16px;
    margin: 14px 0;
    border-radius: 4px;
    font-family: Consolas, monospace;
    font-size: 8.5pt;
    line-height: 1.4;
    white-space: pre-wrap;
    page-break-inside: avoid;
}
.code-box .code-title {
    color: #E2B653;
    font-weight: bold;
    font-size: 9.5pt;
    margin-bottom: 6px;
    border-bottom: 1px dashed rgba(255,255,255,0.2);
    padding-bottom: 4px;
}
table.report-table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}
table.report-table th {
    background-color: #18222F;
    color: #FAF7F2;
    padding: 7px 9px;
    text-align: center;
    font-weight: bold;
    border: 1px solid #18222F;
}
table.report-table td {
    padding: 6px 9px;
    border: 1px solid #E2E8F0;
    color: #1E293B;
    line-height: 1.25;
}
table.report-table tr:nth-child(even) td { background-color: #FAF7F2; }
.page-break { page-break-before: always; break-before: page; }
ul { margin-top: 4px; margin-bottom: 8px; padding-left: 24px; }
li { font-size: 11pt; line-height: 1.35; margin-bottom: 4px; text-align: justify; }
</style>
</head>
<body>

<div class="download-bar no-print">
    <div>
        <strong>System Architecture & Engineering Specification Blueprint</strong>
        <span style="opacity: 0.8; font-size: 12px; margin-left: 12px;">(Multimodal Cultural Heritage KG)</span>
    </div>
    <div>
        <a href="/download/blueprint.docx" download="Comprehensive_System_Architecture_and_Engineering_Blueprint.docx">📥 Download Word (.docx)</a>
        <a href="/download/blueprint.pdf" download="Comprehensive_System_Architecture_and_Engineering_Blueprint.pdf">📄 Download PDF (.pdf)</a>
        <button onclick="window.print()">🖨️ Print / Save as PDF</button>
    </div>
</div>

<div class="report-container">
"""]

    body = doc._body._body
    for child in body:
        if isinstance(child, CT_P):
            p = Paragraph(child, doc)
            text = p.text.strip()
            if not text:
                continue

            if text.startswith("COMPLETE TECHNICAL ARCHITECTURE"):
                html_parts.append(f'<div class="title-cover"><h1>{text.replace(chr(10), "<br>")}</h1>')
                continue
            elif text.startswith("Comprehensive End-to-End Construction Manual"):
                html_parts.append(f'<div class="subtitle">{text.replace(chr(10), "<br>")}</div>')
                continue
            elif text.startswith("Project Repository:"):
                html_parts.append(f'<div class="meta-block">{text.replace(chr(10), "<br>")}</div></div><div class="page-break"></div>')
                continue
            elif text.startswith("SECTION "):
                html_parts.append(f'<div class="page-break"></div><h1>{text}</h1>')
                continue
            elif len(text) > 3 and text[:3].replace('.', '').isdigit() and ' ' in text[:5]:
                html_parts.append(f'<h2>{text}</h2>')
                continue
            elif len(text) > 5 and text[:5].count('.') == 2 and ' ' in text[:8]:
                html_parts.append(f'<h3>{text}</h3>')
                continue
            
            # Check if paragraph is inside list
            if p.style.name == 'List Bullet':
                p_html = ""
                for run in p.runs:
                    r_text = run.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    if run.bold:
                        p_html += f"<strong>{r_text}</strong>"
                    elif run.italic:
                        p_html += f"<em>{r_text}</em>"
                    else:
                        p_html += r_text
                html_parts.append(f'<ul><li>{p_html}</li></ul>')
                continue

            p_html = ""
            for run in p.runs:
                r_text = run.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                if run.bold:
                    p_html += f"<strong>{r_text}</strong>"
                elif run.italic:
                    p_html += f"<em>{r_text}</em>"
                else:
                    p_html += r_text
            html_parts.append(f'<p>{p_html}</p>')

        elif isinstance(child, CT_Tbl):
            tbl = Table(child, doc)
            # Check if this table is a callout box or code block (1 row, 1 col)
            if len(tbl.rows) == 1 and len(tbl.columns) == 1:
                cell_text = tbl.rows[0].cells[0].text.strip()
                if cell_text.startswith("📌"):
                    lines = cell_text.split('\n')
                    title = lines[0].replace("📌", "").strip()
                    body_text = '\n'.join(lines[1:]).strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
                    box_cls = "callout-box architecture" if "BLUEPRINT PURPOSE" in title else "callout-box"
                    html_parts.append(f'''
                    <div class="{box_cls}">
                        <div class="box-title">📌 {title}</div>
                        <div class="box-text">{body_text}</div>
                    </div>''')
                    continue
                elif cell_text.startswith("💻"):
                    lines = cell_text.split('\n')
                    title = lines[0].replace("💻", "").strip()
                    code_body = '\n'.join(lines[1:]).strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    html_parts.append(f'''
                    <div class="code-box">
                        <div class="code-title">💻 {title}</div>
                        <div>{code_body}</div>
                    </div>''')
                    continue

            # Standard Data Table
            t_html = ['<table class="report-table">']
            t_html.append('<thead><tr>')
            for cell in tbl.rows[0].cells:
                t_html.append(f'<th>{cell.text.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</th>')
            t_html.append('</tr></thead><tbody>')
            
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

    with open(html_filename, "w", encoding="utf-8") as f:
        f.write('\n'.join(html_parts))
    print(f"HTML blueprint generated: {html_filename} ({os.path.getsize(html_filename)} bytes)")

    # Render PDF using Microsoft Edge headless
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        output_pdf = os.path.abspath(pdf_filename)
        html_abs = os.path.abspath(html_filename)
        cmd = [
            edge_path,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_pdf}",
            f"file:///{html_abs.replace(os.sep, '/')}"
        ]
        print("Rendering Blueprint PDF via Microsoft Edge...")
        subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(output_pdf):
            print(f"Blueprint PDF successfully created: {output_pdf} ({os.path.getsize(output_pdf)} bytes)")

if __name__ == '__main__':
    export_blueprint()
