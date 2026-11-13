# sesi7/latihan/app_latihan_callback.py — jawaban Latihan Mandiri Sesi 7 (no. 1-5)
# Jalankan: python sesi7/latihan/app_latihan_callback.py  -> buka http://127.0.0.1:8052
#
# 1. dcc.Checklist untuk internet_service, dihubungkan ke filter_df()
# 2. Output kelima pada callback utama: histogram tenure yang ikut terfilter
# 3. Klik titik scatter -> detail pelanggan (ID, region, kontrak, keluhan) di sebuah html.Div
# 4. dcc.Store menyimpan hasil filter (to_dict("records")) sekali; callback tabel membacanya dari store
# 5. Tantangan: selectedData (box/lasso select) pada scatter memfilter tabel
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table, Input, Output, State, callback, ctx, no_update
from dash.exceptions import PreventUpdate

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "customer_churn.csv", parse_dates=["signup_date"])
df["status"] = df["churn"].map({0: "Bertahan", 1: "Churn"})
WARNA = {"Bertahan": "#4C72B0", "Churn": "#C44E52"}
KARTU = {"flex": 1, "padding": "14px", "borderRadius": "10px", "background": "#F4F6FA",
         "textAlign": "center"}
TABEL_COLS = ["customer_id", "region", "segment", "contract_type", "tenure_months",
              "monthly_charges", "num_complaints", "status"]
LAYANAN = sorted(df.internet_service.unique())

app = Dash(__name__, title="Latihan Sesi 7")
server = app.server
app.layout = html.Div(style={"maxWidth": "1200px", "margin": "auto", "fontFamily": "Arial"}, children=[
    html.H1("Latihan Mandiri Sesi 7 — Dash Callback"),

    # ---- Panel filter ----
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr 1fr", "gap": "16px"}, children=[
        html.Div([html.Label("Region"),
                  dcc.Dropdown(id="dd-region", options=sorted(df.region.unique()), multi=True,
                               placeholder="Semua region")]),
        html.Div([html.Label("Segmen (opsi bergantung region)"),
                  dcc.Dropdown(id="dd-segment", multi=True, placeholder="Semua segmen")]),
        html.Div([html.Label("Jenis kontrak"),
                  dcc.RadioItems(id="rd-kontrak", inline=True, value="Semua",
                                 options=["Semua", "Bulanan", "Tahunan", "Dua Tahun"])]),
        # Latihan 1: checklist layanan internet
        html.Div([html.Label("Layanan internet"),
                  dcc.Checklist(id="cl-layanan", options=LAYANAN, value=LAYANAN, inline=True)]),
    ]),
    html.Div(style={"marginTop": "12px"}, children=[
        html.Label("Tenure (bulan)"),
        dcc.RangeSlider(id="rs-tenure", min=1, max=72, step=1, value=[1, 72],
                        marks={i: str(i) for i in (1, 12, 24, 36, 48, 60, 72)}),
    ]),
    html.Div(style={"display": "flex", "gap": "8px", "alignItems": "center"}, children=[
        html.Label("Minimal jumlah keluhan:"),
        dcc.Input(id="in-keluhan", type="number", min=0, max=10, value=0, style={"width": "70px"}),
        html.Button("Terapkan", id="btn-terapkan", n_clicks=0),
        html.Button("Reset filter", id="btn-reset", n_clicks=0),
        html.Span(id="info-keluhan", style={"color": "#666"}),
    ]),
    dcc.Store(id="store-keluhan", data=0),
    dcc.Store(id="store-data", data=[]),         # Latihan 4: hasil filter disimpan sekali di sini

    # ---- KPI ----
    html.Div(id="kpi", style={"display": "flex", "gap": "12px", "margin": "16px 0"}),

    # ---- Charts (Latihan 2: histogram ditambahkan) ----
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px"}, children=[
        dcc.Graph(id="g-bar"), dcc.Graph(id="g-hist"),
        dcc.Graph(id="g-scatter"),
        # Latihan 3: panel detail untuk titik scatter yang diklik
        html.Div(style={"padding": "16px", "background": "#F4F6FA", "borderRadius": "10px"}, children=[
            html.H4("Detail pelanggan (klik satu titik scatter)", style={"marginTop": 0}),
            html.Div(id="detail", children=html.P("Belum ada titik yang dipilih.",
                                                  style={"color": "#666"}))]),
    ]),
    html.P("Tip: klik batang region, atau drag (box/lasso select) pada scatter untuk memfilter tabel.",
           style={"color": "#666"}),
    html.H3(id="judul-tabel"),
    dash_table.DataTable(id="tbl", page_size=10, sort_action="native",
                         columns=[{"name": c, "id": c} for c in TABEL_COLS],
                         style_cell={"padding": "6px", "textAlign": "left"},
                         style_header={"fontWeight": "bold", "background": "#E9EDF5"},
                         style_data_conditional=[{"if": {"filter_query": "{status} = 'Churn'"},
                                                  "backgroundColor": "#FBE9EA"}]),
])


def filter_df(region, segment, kontrak, tenure, min_keluhan, layanan):
    d = df
    if region:
        d = d[d.region.isin(region)]
    if segment:
        d = d[d.segment.isin(segment)]
    if kontrak and kontrak != "Semua":
        d = d[d.contract_type == kontrak]
    d = d[d.tenure_months.between(tenure[0], tenure[1])]
    d = d[d.num_complaints >= (min_keluhan or 0)]
    return d[d.internet_service.isin(layanan or [])]        # Latihan 1


# 1) Chained callback: opsi segmen bergantung pada region terpilih
@callback(Output("dd-segment", "options"), Input("dd-region", "value"))
def update_segment_options(region):
    d = df[df.region.isin(region)] if region else df
    return sorted(d.segment.unique())


# 2) State + tombol; reset juga mengembalikan checklist layanan ke semua
@callback(Output("store-keluhan", "data"), Output("in-keluhan", "value"),
          Output("dd-region", "value"), Output("dd-segment", "value"),
          Output("rd-kontrak", "value"), Output("rs-tenure", "value"),
          Output("cl-layanan", "value"),
          Input("btn-terapkan", "n_clicks"), Input("btn-reset", "n_clicks"),
          State("in-keluhan", "value"), prevent_initial_call=True)
def terapkan_atau_reset(n_apply, n_reset, nilai):
    if ctx.triggered_id == "btn-reset":
        return 0, 0, None, None, "Semua", [1, 72], LAYANAN
    if nilai is None:
        raise PreventUpdate
    return nilai, no_update, no_update, no_update, no_update, no_update, no_update


# 3) Callback utama: filter dihitung SEKALI, hasilnya ke KPI, 3 chart, info, dan dcc.Store (Latihan 4)
@callback(Output("kpi", "children"), Output("g-bar", "figure"), Output("g-scatter", "figure"),
          Output("g-hist", "figure"),                       # Latihan 2: Output kelima
          Output("info-keluhan", "children"), Output("store-data", "data"),
          Input("dd-region", "value"), Input("dd-segment", "value"), Input("rd-kontrak", "value"),
          Input("rs-tenure", "value"), Input("store-keluhan", "data"), Input("cl-layanan", "value"))
def update_dashboard(region, segment, kontrak, tenure, min_keluhan, layanan):
    d = filter_df(region, segment, kontrak, tenure, min_keluhan, layanan)
    info = f"Filter keluhan aktif: ≥ {min_keluhan}"
    if d.empty:
        kosong = px.scatter(title="Tidak ada data untuk filter ini")
        return [html.Div("Data kosong", style=KARTU)], kosong, kosong, kosong, info, []

    def kartu(j, v):
        return html.Div([html.Small(j), html.H2(v, style={"margin": "4px 0"})], style=KARTU)

    kpi = [kartu("Pelanggan", f"{len(d):,}"), kartu("Churn rate", f"{d.churn.mean():.1%}"),
           kartu("Rata-rata tagihan", f"Rp{d.monthly_charges.mean():,.0f}".replace(",", ".")),
           kartu("Rata-rata keluhan", f"{d.num_complaints.mean():.2f}")]

    reg = d.groupby("region", as_index=False)["churn"].mean().sort_values("churn", ascending=False)
    bar = px.bar(reg, x="region", y="churn", template="plotly_white", title="Churn rate per region",
                 labels={"churn": "Churn rate", "region": ""}, color_discrete_sequence=["#C44E52"])
    bar.update_yaxes(tickformat=".0%")

    # custom_data dibutuhkan agar clickData / selectedData membawa customer_id (Latihan 3 & 5)
    sc = px.scatter(d, x="tenure_months", y="monthly_charges", color="status", opacity=0.6,
                    color_discrete_map=WARNA, template="plotly_white", hover_name="customer_id",
                    custom_data=["customer_id"], title="Tenure vs tagihan",
                    labels={"tenure_months": "Tenure (bulan)", "monthly_charges": "Tagihan (Rp)"})
    sc.update_layout(dragmode="select")

    hist = px.histogram(d, x="tenure_months", color="status", nbins=36, barmode="overlay",
                        opacity=0.7, color_discrete_map=WARNA, template="plotly_white",
                        title="Distribusi tenure (ikut terfilter)",
                        labels={"tenure_months": "Tenure (bulan)", "status": "Status"})

    return kpi, bar, sc, hist, info, d[TABEL_COLS].to_dict("records")


# 4) Latihan 3: klik titik scatter -> detail pelanggan
@callback(Output("detail", "children"), Input("g-scatter", "clickData"))
def tampil_detail(click):
    if not click:
        raise PreventUpdate
    cid = click["points"][0]["customdata"][0]
    r = df.loc[df.customer_id == cid].iloc[0]
    return html.Ul([html.Li(f"ID: {r.customer_id}"), html.Li(f"Region: {r.region}"),
                    html.Li(f"Kontrak: {r.contract_type}"), html.Li(f"Keluhan: {r.num_complaints}")])


# 5) Latihan 4 & 5: tabel membaca dari dcc.Store; klik batang ATAU select pada scatter memfilter
@callback(Output("tbl", "data"), Output("judul-tabel", "children"),
          Input("g-bar", "clickData"), Input("g-scatter", "selectedData"),
          Input("store-data", "data"))
def update_tabel(click_bar, selected, data):
    if not data:
        return [], "Tidak ada data"
    d = pd.DataFrame(data)                                   # dibaca dari store, tanpa menghitung ulang filter
    judul = "Detail pelanggan (semua hasil filter)"
    if ctx.triggered_id == "g-bar" and click_bar:
        reg = click_bar["points"][0]["x"]
        d = d[d.region == reg]
        judul = f"Detail pelanggan — region {reg}"
    elif ctx.triggered_id == "g-scatter" and selected and selected.get("points"):
        ids = [p["customdata"][0] for p in selected["points"]]
        d = d[d.customer_id.isin(ids)]
        judul = f"Detail pelanggan — {len(d)} titik terpilih di scatter"
    return d.to_dict("records"), judul


if __name__ == "__main__":
    app.run(debug=True, port=8052)
