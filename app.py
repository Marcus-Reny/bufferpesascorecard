"""
BufferPesa — Kenya Commercial Scorecard (v2)
Rebuilt from the actual vet-list PDF + invoice-level data.

Run with:  python app.py
Then open: http://127.0.0.1:8050
"""

from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.graph_objects as go
from collections import Counter

# =====================================================================
# RAW DATA — straight from BufferPesa_Vet_list___Main_Data PDF
# Columns: Name, Organization, Region, Sub-County, KAM, Download, KYC
# =====================================================================
VETS = [
    ("Morien Kinuthia", "Agrovet (PPP-private)", "Kajiado", "Ngong'", "Daniel", "Yes", "Pending"),
    ("Kisengo Vincent", "Private Vpp", "Kajiado", "Ngong'", "Daniel", "Yes", "Approved"),
    ("Maka Bore", "Private Vpp", "Kajiado", "Ngong'", "Daniel", "Yes", "Pending"),
    ("Chrispus Kimwaro", "Private Vpp", "Kajiado", "Ngong'", "Daniel", "No", "Pending"),
    ("Maureen Waithere Mbaabu", "Private Vpp", "Kajiado", "Kiserian", "Daniel", "Yes", "Pending"),
    ("Susan Mbogo", "Private Vpp", "Kajiado", "Ngong'", "Daniel", "Yes", "Approved"),
    ("Nazariah Nyaga", "Private BVM", "Kajiado", "Kajiado", "Daniel", "No", "Pending"),
    ("Sharon Nutrix", "Agrovet", "Kajiado", "Ngong'", "Daniel", "Yes", "Approved"),
    ("Kennedy Sane", "Private BVM", "Kajiado", "Ngong'", "Daniel", "Yes", "Pending"),
    ("Elvis Mutsotso", "Private Vpp", "Kajiado", "Ngong'", "Daniel", "Yes", "Pending"),
    ("George Ndungu Mwangi", "", "Kiambu", "Gatundu South", "Daniel", "Yes", "Approved"),
    ("Samuel chege ndungu", "", "Kiambu", "Gatundu South", "Daniel", "Yes", "Approved"),
    ("Dennis muchai", "", "Kiambu", "Gatundu South", "Daniel", "Yes", "Approved"),
    ("Ann Wambui", "Private Practice", "Kiambu", "Gatundu South", "Daniel", "Yes", "Approved"),
    ("Eunice Wanjiru", "County Government", "Kiambu", "Gatundu South", "Daniel", "Yes", "Approved"),
    ("Catherine wambui", "County Government", "Kiambu", "Gatundu South", "Daniel", "Yes", "Approved"),
    ("Bernard Ngugi Kiarie", "Private Practice", "Kiambu", "Gatundu South", "Daniel", "Yes", "Approved"),
    ("Nicholas G Mwangi", "Private Practice", "Kiambu", "Gatundu North", "Daniel", "Yes", "Approved"),
    ("Lydiah Nyaga", "County Government", "Kiambu", "Gatundu South", "Daniel", "Yes", "Approved"),
    ("Lucy Njogu", "Private Practice", "Kiambu", "Gatundu South", "Daniel", "Yes", "Approved"),
    ("Joseph Mwaura", "Private Practice", "Kiambu", "Gatundu South", "Daniel", "No", "Pending"),
    ("Anthony Kiarie", "Private Practice", "Kiambu", "Gatundu South", "Daniel", "Yes", "Pending"),
    ("Tabitha Gathecha", "County Government", "Kiambu", "Gatundu South", "Daniel", "No", "Pending"),
    ("Peter Ngugi", "Private Practice", "Kiambu", "Gatundu South", "Daniel", "Yes", "Pending"),
    ("Dr. Morgan Musonye", "Vet Trainer", "Lake Basin", "Shinyalu", "Daniel", "Pending", "Pending"),
    ("Dr. Paul Ng'ang'a", "Animal Health Provider", "Kiambu", "Kiambu", "Daniel", "Pending", "Pending"),
    ("Dr. Dancun Kibet", "Animal Health Provider", "Lake Basin", "Bomet", "Daniel", "Pending", "Pending"),
    ("Dr. Erick Kangu", "Vet VMD", "Kiambu", "Kiambu", "Daniel", "Yes", "Pending"),
    ("Nelson Mwakitau", "Private-BVM", "Voi", "Voi", "Harold", "Pending", "Pending"),
    ("Bravon Lukondo", "VPP", "Voi", "Wundanyi", "Harold", "Yes", "Approved"),
    ("Dorothy Mwalugho", "VPP", "Voi", "Mwatate", "Harold", "Yes", "Approved"),
    ("Jemima Kichengoa", "VPP", "Voi", "Wundanyi", "Harold", "Yes", "Approved"),
    ("Donald Kiwinga", "VPP-Private", "Voi", "Wundanyi", "Harold", "Yes", "Approved"),
    ("Stephen Mkala", "VPP", "Voi", "Mwatate", "Harold", "Yes", "Pending"),
    ("Derick Mwachola", "VPP", "Voi", "Taveta", "Harold", "Yes", "Approved"),
    ("Dan Boli", "VPP", "Voi", "Voi", "Harold", "Yes", "Approved"),
    ("Remmy Mwasaru", "VPP", "Voi", "Voi", "Harold", "Yes", "Approved"),
    ("Festus kiptoo koech", "", "Lake Basin", "Kericho", "Harold", "Yes", "Pending"),
    ("GUSTON", "", "Lake Basin", "Kisumu", "Harold", "Pending", "Pending"),
    ("JACK OMONDI", "", "Lake Basin", "Kisumu", "Harold", "Yes", "Pending"),
    ("MILLICENT A. OJWANG'", "", "Lake Basin", "Kisumu", "Harold", "Pending", "Pending"),
    ("AGUSTINE OCHIENG OTIENO", "", "Lake Basin", "Kisumu", "Harold", "Pending", "Pending"),
    ("Felix Oyier", "", "Lake Basin", "Bomet", "Harold", "Yes", "Approved"),
    ("Dr. Onyonge", "", "Lake Basin", "Kisumu", "Harold", "Pending", "Pending"),
    ("Gibson Mwandigha", "AI Technician", "Voi", "", "Harold", "Yes", "Approved"),
    ("BOAZ ARISI", "Private Practice", "Lake Basin", "Nyamira", "Harold", "Yes", "Approved"),
    ("Amos Bett", "Office Cleaning Service", "Nairobi", "Nairobi", "", "Yes", "Approved"),
]
VET_COLS = ["Name", "Organization", "Region", "Sub-County", "KAM", "Download", "KYC"]

# ---- Invoices CREATED (vets using BufferPesa purely as a tracking tool —
#      these were not necessarily sold/factored to BufferPesa) -----------
INVOICES_CREATED = [
    ("Kisengo Vincent", "Kajiado", 2800.00, 1, 1),
    ("Susan Mbogo", "Kajiado", 3020.00, 2, 1),
    ("Dan Boli", "Voi", 6345.00, 4, 4),
    ("Bravon Lukondo", "Voi", 1300.00, 2, 2),   # region corrected: Wundanyi is his sub-county within Voi
    ("Samuel Chege", "Kiambu", 5000.00, 3, 3),
    ("Bernard Ngugi", "Kiambu", 28200.00, 15, 14),
    ("Remmy Mwasaru", "Voi", 1800.00, 1, 1),
]
INV_COLS = ["Vet Name", "Region", "Amount (KSH)", "Invoice Count", "Farmers"]

INV_TOTAL_AMOUNT = sum(r[2] for r in INVOICES_CREATED)
INV_TOTAL_COUNT = sum(r[3] for r in INVOICES_CREATED)
INV_TOTAL_FARMERS = sum(r[4] for r in INVOICES_CREATED)

# ---- Invoices FUNDED (actually factored/disbursed by BufferPesa) -------
FUNDED_INVOICES = [700, 500]   # KSH
FUNDED_COUNT = len(FUNDED_INVOICES)
FUNDED_TOTAL = sum(FUNDED_INVOICES)  # 1,200 KSH

# =====================================================================
# DERIVED ROLL-UPS
# =====================================================================
REGIONS = ["Kajiado", "Kiambu", "Voi", "Lake Basin", "Nairobi"]
REGION_COLORS = {"Kajiado": "#185FA5", "Kiambu": "#1D9E75", "Voi": "#533AB7",
                  "Lake Basin": "#A32D2D", "Nairobi": "#C27A1A"}

# Approximate town-level coordinates representing each region (not exact centroids)
REGION_COORDS = {
    "Kajiado": (-1.8531, 36.7820),    # Kajiado town
    "Kiambu": (-1.1714, 36.8356),     # Kiambu town
    "Voi": (-3.3961, 38.5561),        # Voi town
    "Lake Basin": (-0.0917, 34.7680), # Kisumu (most Lake Basin vets are Kisumu/Kericho/Bomet/Nyamira)
    "Nairobi": (-1.2921, 36.8219),    # Nairobi CBD
}

region_counts = Counter(v[2] for v in VETS)
region_dl_yes = Counter(v[2] for v in VETS if v[5] == "Yes")
region_dl_no = Counter(v[2] for v in VETS if v[5] == "No")
region_dl_pending = Counter(v[2] for v in VETS if v[5] == "Pending")
region_kyc_approved = Counter(v[2] for v in VETS if v[6] == "Approved")
region_kyc_pending = Counter(v[2] for v in VETS if v[6] == "Pending")

TOTAL_VETS = len(VETS)
TOTAL_DL_YES = sum(1 for v in VETS if v[5] == "Yes")
TOTAL_DL_NO = sum(1 for v in VETS if v[5] == "No")
TOTAL_DL_PENDING = sum(1 for v in VETS if v[5] == "Pending")
TOTAL_KYC_APPROVED = sum(1 for v in VETS if v[6] == "Approved")
TOTAL_KYC_PENDING = sum(1 for v in VETS if v[6] == "Pending")
ACTIVE_INVOICING_VETS = len(INVOICES_CREATED)

kam_counts = Counter(v[4] if v[4] else "Unassigned" for v in VETS)

# Business-type grouping (organization field is messy/inconsistent in source data —
# grouped into broader buckets; revisit if finer detail is needed)
PRACTICE_KEYWORDS = ["vpp", "private", "bvm"]


def classify_org(org):
    o = org.lower()
    if not o:
        return "Unspecified"
    if "agrovet" in o:
        return "Agrovet"
    if "county government" in o:
        return "County Government"
    if "animal health" in o or "vet trainer" in o or "vmd" in o:
        return "Technical / Specialist"
    if "ai technician" in o:
        return "AI Technician"
    if any(k in o for k in PRACTICE_KEYWORDS):
        return "Private Practice / VPP"
    return "Other"


biz_counts = Counter(classify_org(v[1]) for v in VETS)

# =====================================================================
# APP
# =====================================================================
app = Dash(__name__)
app.title = "BufferPesa — Kenya Commercial Scorecard"

NAVY, BLUE, TEAL, GREEN, AMBER, PURPLE, RED, GRAY = (
    "#0D2B55", "#185FA5", "#1D9E75", "#3B6D11", "#C27A1A", "#533AB7", "#A32D2D", "#888780"
)
BG, CARD, BORDER, TEXT, MUTED = "#F2F0EB", "#FAFAF8", "#DDD9D0", "#1A1917", "#6B6860"
FONT = "DM Sans, Helvetica, Arial, sans-serif"
HEAD_FONT = "Syne, Helvetica, Arial, sans-serif"


def kpi_card(label, value, sub, color):
    return html.Div(
        style={"background": CARD, "border": f"1.5px solid {BORDER}", "borderRadius": "12px",
               "padding": "1rem .9rem", "borderTop": f"3px solid {color}", "flex": "1", "minWidth": "150px"},
        children=[
            html.Div(label, style={"fontSize": ".7rem", "fontWeight": "600", "color": MUTED,
                                    "textTransform": "uppercase", "letterSpacing": ".05em", "marginBottom": ".4rem"}),
            html.Div(str(value), style={"fontFamily": HEAD_FONT, "fontWeight": "800", "fontSize": "1.9rem", "color": color}),
            html.Div(sub, style={"fontSize": ".7rem", "color": MUTED, "marginTop": ".3rem"}),
        ],
    )


def section_head(title):
    return html.Div(
        style={"display": "flex", "alignItems": "center", "gap": ".75rem", "margin": "1.75rem 0 1rem"},
        children=[
            html.H2(title, style={"fontFamily": HEAD_FONT, "fontWeight": "700", "fontSize": ".95rem",
                                   "color": NAVY, "whiteSpace": "nowrap"}),
            html.Hr(style={"flex": "1", "border": "none", "borderTop": f"1px solid {BORDER}"}),
        ],
    )


def chart_card(children, flex="1"):
    return html.Div(
        style={"background": CARD, "border": f"1px solid {BORDER}", "borderRadius": "14px",
               "padding": "1.1rem 1.2rem", "flex": flex, "minWidth": "300px"},
        children=children,
    )


def note(text, color=MUTED, bg=BG):
    return html.Div(text, style={"fontSize": ".78rem", "color": color, "background": bg,
                                  "border": f"1px solid {BORDER}", "borderRadius": "8px",
                                  "padding": ".6rem .9rem", "marginBottom": "1rem"})


# ---------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------
app.layout = html.Div(
    style={"fontFamily": FONT, "background": BG, "minHeight": "100vh", "color": TEXT},
    children=[
        html.Div(
            style={"background": NAVY, "padding": "0 2rem", "height": "56px", "display": "flex",
                   "alignItems": "center", "justifyContent": "space-between"},
            children=[
                html.Div([html.Span("Buffer", style={"color": "#fff"}), html.Span("Pesa", style={"color": "#4DB896"})],
                         style={"fontFamily": HEAD_FONT, "fontWeight": "800", "fontSize": "1.15rem"}),
                html.Div("Kenya · Verified Vet List", style={"fontSize": ".78rem", "color": "rgba(255,255,255,.5)"}),
            ],
        ),
        html.Div(
            style={"padding": "1.75rem 2rem", "maxWidth": "1250px", "margin": "0 auto"},
            children=[
                html.Div([
                    html.H1("Kenya Commercial Scorecard", style={"fontFamily": HEAD_FONT, "fontWeight": "800",
                                                                  "fontSize": "1.6rem", "color": NAVY}),
                    html.P("Pipeline → App Download → KYC Approval → Active Invoicing  |  Invoices Created → Funded",
                           style={"fontSize": ".85rem", "color": MUTED, "marginTop": ".3rem"}),
                ], style={"marginBottom": "1rem"}),

                # ---- National KPIs ----
                section_head("Key Metrics (National)"),
                html.Div(
                    style={"display": "flex", "gap": "10px", "flexWrap": "wrap", "marginBottom": "1rem"},
                    children=[
                        kpi_card("Vets in Pipeline", TOTAL_VETS, "Verified from vet list", NAVY),
                        kpi_card("App Downloaded", TOTAL_DL_YES, f"{round(TOTAL_DL_YES/TOTAL_VETS*100)}% of pipeline", BLUE),
                        kpi_card("KYC Approved", TOTAL_KYC_APPROVED, f"{round(TOTAL_KYC_APPROVED/TOTAL_VETS*100)}% of pipeline", TEAL),
                        kpi_card("Actively Invoicing", ACTIVE_INVOICING_VETS, "Vets who've raised ≥1 invoice", PURPLE),
                        kpi_card("Invoices Created", INV_TOTAL_COUNT, f"{INV_TOTAL_FARMERS} farmers linked", AMBER),
                        kpi_card("Invoices Funded", FUNDED_COUNT, f"{FUNDED_TOTAL:,} KSH financed", RED),
                        kpi_card("Value Created", f"{INV_TOTAL_AMOUNT:,.0f} KSH", "Across all invoices", GREEN),
                        kpi_card("% Value Financed", f"{round(FUNDED_TOTAL/INV_TOTAL_AMOUNT*100,1)}%", "Funded ÷ Created value", GRAY),
                    ],
                ),
                note(
                    f"Only {FUNDED_TOTAL:,} KSH of the {INV_TOTAL_AMOUNT:,.0f} KSH in invoices created so far has "
                    "actually been factored/funded — most vets are still using BufferPesa purely as a tracking "
                    "tool rather than selling invoices for financing.",
                ),

                # ---- Funnels ----
                section_head("Funnels"),
                html.Div(
                    style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "14px"},
                    children=[
                        chart_card([
                            html.H3("Vet Onboarding Funnel", style={"fontFamily": HEAD_FONT, "fontWeight": "700",
                                                                     "fontSize": ".88rem", "color": NAVY, "marginBottom": ".25rem"}),
                            html.Div("Pipeline → Download → KYC → Actively invoicing", style={"fontSize": ".75rem", "color": MUTED, "marginBottom": ".5rem"}),
                            dcc.Graph(id="vet-funnel", config={"displayModeBar": False}),
                        ]),
                        chart_card([
                            html.H3("Invoice Funnel", style={"fontFamily": HEAD_FONT, "fontWeight": "700",
                                                              "fontSize": ".88rem", "color": NAVY, "marginBottom": ".25rem"}),
                            html.Div("Created → Funded (by count)", style={"fontSize": ".75rem", "color": MUTED, "marginBottom": ".5rem"}),
                            dcc.Graph(id="invoice-funnel", config={"displayModeBar": False}),
                        ]),
                    ],
                ),

                # ---- Regional breakdown ----
                section_head("Regional Breakdown"),
                html.Div(
                    style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "14px"},
                    children=[
                        chart_card([
                            html.H3("Vets by Region", style={"fontFamily": HEAD_FONT, "fontWeight": "700",
                                                              "fontSize": ".88rem", "color": NAVY, "marginBottom": ".5rem"}),
                            dcc.Dropdown(
                                id="region-metric",
                                options=[
                                    {"label": "Total Vets", "value": "total"},
                                    {"label": "App Downloaded", "value": "downloaded"},
                                    {"label": "KYC Approved", "value": "kyc"},
                                ],
                                value="total", clearable=False, style={"marginBottom": ".75rem"},
                            ),
                            dcc.Graph(id="region-bar", config={"displayModeBar": False}),
                        ], flex="1.2"),
                        chart_card([
                            html.H3("Download & KYC Status", style={"fontFamily": HEAD_FONT, "fontWeight": "700",
                                                                     "fontSize": ".88rem", "color": NAVY, "marginBottom": ".5rem"}),
                            dcc.Graph(id="status-donut", config={"displayModeBar": False}),
                        ]),
                    ],
                ),
                html.Div(
                    style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "14px"},
                    children=[
                        chart_card([
                            html.H3("Business Type Mix", style={"fontFamily": HEAD_FONT, "fontWeight": "700",
                                                                  "fontSize": ".85rem", "color": NAVY, "marginBottom": ".5rem"}),
                            dcc.Graph(id="biz-chart", config={"displayModeBar": False}),
                        ]),
                        chart_card([
                            html.H3("Vets by KAM", style={"fontFamily": HEAD_FONT, "fontWeight": "700",
                                                           "fontSize": ".85rem", "color": NAVY, "marginBottom": ".5rem"}),
                            dcc.Graph(id="kam-chart", config={"displayModeBar": False}),
                        ]),
                    ],
                ),

                # ---- Kenya Map ----
                section_head("Kenya Region Map"),
                chart_card([
                    html.H3("Vet Distribution Across Kenya", style={"fontFamily": HEAD_FONT, "fontWeight": "700",
                                                                      "fontSize": ".88rem", "color": NAVY, "marginBottom": ".25rem"}),
                    html.Div("Bubble size = number of vets. Hover for region detail.", style={"fontSize": ".75rem", "color": MUTED, "marginBottom": ".5rem"}),
                    dcc.Dropdown(
                        id="map-metric",
                        options=[
                            {"label": "Total Vets", "value": "total"},
                            {"label": "App Downloaded", "value": "downloaded"},
                            {"label": "KYC Approved", "value": "kyc"},
                        ],
                        value="total", clearable=False, style={"marginBottom": ".75rem", "maxWidth": "260px"},
                    ),
                    dcc.Graph(id="kenya-map", config={"displayModeBar": False}),
                ]),

                # ---- Invoices created table ----
                section_head("Invoices Created (Tracking Use, Not Yet Factored)"),
                html.Div(
                    style={"background": CARD, "border": f"1px solid {BORDER}", "borderRadius": "14px", "overflow": "hidden", "marginBottom": "14px"},
                    children=[
                        dash_table.DataTable(
                            columns=[{"name": c, "id": c} for c in INV_COLS],
                            data=[dict(zip(INV_COLS, row)) for row in INVOICES_CREATED] +
                                 [{"Vet Name": "TOTAL", "Region": "", "Amount (KSH)": f"{INV_TOTAL_AMOUNT:,.2f}",
                                   "Invoice Count": INV_TOTAL_COUNT, "Farmers": INV_TOTAL_FARMERS}],
                            style_header={"backgroundColor": NAVY, "color": "white", "fontWeight": "600",
                                          "fontSize": ".72rem", "textTransform": "uppercase"},
                            style_cell={"fontFamily": FONT, "fontSize": ".82rem", "padding": "9px 12px", "textAlign": "left"},
                            style_data_conditional=[
                                {"if": {"row_index": "odd"}, "backgroundColor": "#FAFAF8"},
                                {"if": {"filter_query": '{Vet Name} = "TOTAL"'}, "fontWeight": "700", "backgroundColor": "#E8F1FB"},
                            ],
                        ),
                    ],
                ),

                # ---- Full vet pipeline table ----
                section_head("Full Vet Pipeline (47)"),
                html.Div(
                    style={"background": CARD, "border": f"1px solid {BORDER}", "borderRadius": "14px", "overflow": "hidden"},
                    children=[
                        dash_table.DataTable(
                            columns=[{"name": c, "id": c} for c in VET_COLS],
                            data=[dict(zip(VET_COLS, row)) for row in VETS],
                            style_header={"backgroundColor": NAVY, "color": "white", "fontWeight": "600",
                                          "fontSize": ".7rem", "textTransform": "uppercase"},
                            style_cell={"fontFamily": FONT, "fontSize": ".78rem", "padding": "8px 10px", "textAlign": "left"},
                            style_data_conditional=[
                                {"if": {"row_index": "odd"}, "backgroundColor": "#FAFAF8"},
                                {"if": {"filter_query": '{KYC} = "Approved"', "column_id": "KYC"},
                                 "color": GREEN, "fontWeight": "600"},
                                {"if": {"filter_query": '{KYC} = "Pending"', "column_id": "KYC"},
                                 "color": AMBER, "fontWeight": "600"},
                                {"if": {"filter_query": '{Download} = "Yes"', "column_id": "Download"},
                                 "color": GREEN, "fontWeight": "600"},
                                {"if": {"filter_query": '{Download} = "No"', "column_id": "Download"},
                                 "color": RED, "fontWeight": "600"},
                                {"if": {"filter_query": '{Download} = "Pending"', "column_id": "Download"},
                                 "color": AMBER, "fontWeight": "600"},
                            ],
                            filter_action="native", sort_action="native", page_size=12,
                        ),
                    ],
                ),
                html.Div(style={"height": "2rem"}),
            ],
        ),
    ],
)

# =====================================================================
# CALLBACKS
# =====================================================================
@app.callback(Output("vet-funnel", "figure"), Input("vet-funnel", "id"))
def render_vet_funnel(_):
    labels = ["Pipeline", "App Downloaded", "KYC Approved", "Actively Invoicing"]
    values = [TOTAL_VETS, TOTAL_DL_YES, TOTAL_KYC_APPROVED, ACTIVE_INVOICING_VETS]
    fig = go.Figure(go.Funnel(
        y=labels, x=values, text=[f"{v}" for v in values], textposition="inside",
        marker={"color": [NAVY, BLUE, TEAL, PURPLE]},
        connector={"line": {"color": BORDER, "width": 1}},
    ))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300,
                       paper_bgcolor="rgba(0,0,0,0)", font=dict(family=FONT, size=12, color=TEXT))
    return fig


@app.callback(Output("invoice-funnel", "figure"), Input("invoice-funnel", "id"))
def render_invoice_funnel(_):
    labels = ["Invoices Created", "Invoices Funded"]
    values = [INV_TOTAL_COUNT, FUNDED_COUNT]
    fig = go.Figure(go.Funnel(
        y=labels, x=values, text=[f"{v}" for v in values], textposition="inside",
        marker={"color": [AMBER, RED]},
        connector={"line": {"color": BORDER, "width": 1}},
    ))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300,
                       paper_bgcolor="rgba(0,0,0,0)", font=dict(family=FONT, size=12, color=TEXT))
    return fig


@app.callback(Output("region-bar", "figure"), Input("region-metric", "value"))
def render_region_bar(metric):
    if metric == "total":
        data = [region_counts.get(r, 0) for r in REGIONS]
    elif metric == "downloaded":
        data = [region_dl_yes.get(r, 0) for r in REGIONS]
    else:
        data = [region_kyc_approved.get(r, 0) for r in REGIONS]
    colors = [REGION_COLORS[r] for r in REGIONS]
    fig = go.Figure(go.Bar(x=REGIONS, y=data, marker_color=colors, text=data, textposition="outside"))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280,
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       font=dict(family=FONT, size=12, color=TEXT),
                       yaxis=dict(gridcolor="rgba(0,0,0,0.06)"), showlegend=False)
    return fig


@app.callback(Output("status-donut", "figure"), Input("status-donut", "id"))
def render_status_donut(_):
    fig = go.Figure(go.Pie(
        labels=["Downloaded", "Download Pending", "Not Downloaded"],
        values=[TOTAL_DL_YES, TOTAL_DL_PENDING, TOTAL_DL_NO],
        hole=0.65, marker=dict(colors=[TEAL, AMBER, RED]),
    ))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280,
                       paper_bgcolor="rgba(0,0,0,0)", font=dict(family=FONT, size=12, color=TEXT),
                       legend=dict(orientation="h", y=-0.1))
    return fig


@app.callback(Output("biz-chart", "figure"), Input("biz-chart", "id"))
def render_biz(_):
    labels = list(biz_counts.keys())
    values = [biz_counts[k] for k in labels]
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=[BLUE, TEAL, PURPLE, AMBER, GREEN, GRAY][:len(labels)]))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=240,
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       font=dict(family=FONT, size=10, color=TEXT),
                       yaxis=dict(gridcolor="rgba(0,0,0,0.06)"), showlegend=False)
    return fig


@app.callback(Output("kam-chart", "figure"), Input("kam-chart", "id"))
def render_kam(_):
    labels = list(kam_counts.keys())
    values = [kam_counts[k] for k in labels]
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=[NAVY, BLUE, GRAY][:len(labels)],
                            text=values, textposition="outside"))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=240,
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       font=dict(family=FONT, size=11, color=TEXT),
                       yaxis=dict(gridcolor="rgba(0,0,0,0.06)"), showlegend=False)
    return fig


@app.callback(Output("kenya-map", "figure"), Input("map-metric", "value"))
def render_kenya_map(metric):
    if metric == "total":
        counts = {r: region_counts.get(r, 0) for r in REGIONS}
    elif metric == "downloaded":
        counts = {r: region_dl_yes.get(r, 0) for r in REGIONS}
    else:
        counts = {r: region_kyc_approved.get(r, 0) for r in REGIONS}

    lats = [REGION_COORDS[r][0] for r in REGIONS]
    lons = [REGION_COORDS[r][1] for r in REGIONS]
    sizes = [counts[r] * 4 + 18 for r in REGIONS]
    colors = [REGION_COLORS[r] for r in REGIONS]
    hover = [f"<b>{r}</b><br>Total vets: {region_counts.get(r,0)}<br>"
             f"Downloaded: {region_dl_yes.get(r,0)}<br>KYC Approved: {region_kyc_approved.get(r,0)}"
             for r in REGIONS]

    fig = go.Figure(go.Scattergeo(
        lat=lats, lon=lons,
        text=[f"{r}<br>{counts[r]}" for r in REGIONS],
        mode="markers+text",
        marker=dict(size=sizes, color=colors, opacity=0.85, line=dict(width=1, color="white")),
        textfont=dict(color="white", size=11, family=HEAD_FONT),
        textposition="middle center",
        hovertext=hover, hoverinfo="text",
    ))
    fig.update_geos(
        scope="africa",
        center=dict(lat=-1.0, lon=37.5),
        projection_scale=7,
        showland=True, landcolor="#E8EDF5",
        showcountries=True, countrycolor="#B8C4D8",
        showcoastlines=True, coastlinecolor="#B8C4D8",
        showlakes=True, lakecolor="#C8DCF0",
        showsubunits=False, resolution=50,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=420,
                       paper_bgcolor="rgba(0,0,0,0)", font=dict(family=FONT))
    return fig


server = app.server  # expose the Flask server

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
