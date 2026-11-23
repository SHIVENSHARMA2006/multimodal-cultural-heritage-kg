"""
Interactive Visual Components for Cultural Heritage Knowledge Graph.
Generates interactive Vis.js graph network diagrams, audio players,
and dual-perspective side-by-side cards.
"""
import json
from typing import Dict, List, Any

# CIDOC-CRM Visual Color Palette
CIDOC_COLOR_MAP = {
    "E22_Human_Made_Object": {"background": "#FDE68A", "border": "#D97706", "label": "Monument / Object"},
    "E53_Place": {"background": "#BFDBFE", "border": "#2563EB", "label": "Place / Site"},
    "E39_Actor": {"background": "#FED7AA", "border": "#EA580C", "label": "Historical Actor / Deity"},
    "E5_Event": {"background": "#FECDD3", "border": "#E11D48", "label": "Historical Event"},
    "E73_Information_Object": {"background": "#E9D5FF", "border": "#9333EA", "label": "Text / Manuscript"},
    "Value": {"background": "#F1F5F9", "border": "#94A3B8", "label": "Attribute Value"}
}

def render_visjs_subgraph(subgraph_data: Dict[str, Any], height: int = 550) -> str:
    """
    Renders an interactive Vis.js physics-enabled network graph.
    """
    nodes = []
    for n in subgraph_data.get("nodes", []):
        cidoc = n.get("cidoc_class", "Value")
        colors = CIDOC_COLOR_MAP.get(cidoc, CIDOC_COLOR_MAP["Value"])
        is_div = n.get("has_divergence", False)

        label = n.get("label", "")
        if n.get("meitei_name"):
            label += f"\n({n['meitei_name']})"

        border_width = 3 if is_div else 1
        border_color = "#DC2626" if is_div else colors["border"]

        nodes.append({
            "id": n["id"],
            "label": label,
            "title": f"Type: {n.get('type')}<br>CIDOC: {cidoc}<br>Divergence: {'Flagged' if is_div else 'None'}",
            "color": {
                "background": colors["background"],
                "border": border_color,
                "highlight": {"background": "#FFFBEB", "border": "#D97706"}
            },
            "borderWidth": border_width,
            "shape": "box",
            "margin": 10,
            "font": {"size": 13, "face": "Plus Jakarta Sans, sans-serif"}
        })

    edges = []
    for e in subgraph_data.get("edges", []):
        div_grade = e.get("divergence_grade", "none")
        edge_color = "#EF4444" if div_grade == "hard" else ("#F59E0B" if div_grade == "soft" else "#94A3B8")
        dashes = True if div_grade == "hard" else False

        edges.append({
            "from": e["source"],
            "to": e["target"],
            "label": e.get("relation", ""),
            "title": f"Source: {e.get('source_title')}<br>Modality: {e.get('modality')}<br>Divergence: {div_grade.upper()}",
            "color": {"color": edge_color, "highlight": "#1E293B"},
            "arrows": "to",
            "dashes": dashes,
            "font": {"size": 10, "align": "middle", "color": "#475569"}
        })

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style>
            #network {{
                width: 100%;
                height: {height}px;
                border: 1px solid #E2E8F0;
                background-color: #FAF9F6;
                border-radius: 12px;
            }}
            .legend {{
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                padding: 10px;
                font-family: sans-serif;
                font-size: 12px;
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                margin-top: 8px;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .color-box {{
                width: 14px;
                height: 14px;
                border-radius: 3px;
            }}
        </style>
    </head>
    <body style="margin: 0; padding: 0;">
        <div id="network"></div>
        <div class="legend">
            <div class="legend-item"><div class="color-box" style="background:#FDE68A; border:1px solid #D97706;"></div> Monument/Object (E22)</div>
            <div class="legend-item"><div class="color-box" style="background:#FED7AA; border:1px solid #EA580C;"></div> Historical Actor (E39)</div>
            <div class="legend-item"><div class="color-box" style="background:#BFDBFE; border:1px solid #2563EB;"></div> Place/Site (E53)</div>
            <div class="legend-item"><div class="color-box" style="background:#FECDD3; border:1px solid #E11D48;"></div> Historical Event (E5)</div>
            <div class="legend-item"><div class="color-box" style="background:#E9D5FF; border:1px solid #9333EA;"></div> Text/Manuscript (E73)</div>
            <div class="legend-item"><div class="color-box" style="border: 2px dashed #EF4444; background: white;"></div> Hard Divergence Edge</div>
        </div>
        <script type="text/javascript">
            var nodes = new vis.DataSet({json.dumps(nodes)});
            var edges = new vis.DataSet({json.dumps(edges)});
            var container = document.getElementById('network');
            var data = {{ nodes: nodes, edges: edges }};
            var options = {{
                nodes: {{
                    shadow: true
                }},
                edges: {{
                    smooth: {{ type: 'cubicBezier', forceDirection: 'none', roundness: 0.2 }}
                }},
                physics: {{
                    barnesHut: {{
                        gravitationalConstant: -3000,
                        centralGravity: 0.3,
                        springLength: 120,
                        springConstant: 0.04
                    }},
                    stabilization: {{ iterations: 150 }}
                }},
                interaction: {{
                    hover: true,
                    navigationButtons: true,
                    keyboard: true
                }}
            }};
            var network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    """
    return html_content
