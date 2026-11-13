# sesi5/latihan/app_latihan_sesi5.py — jawaban Latihan Mandiri Sesi 5 (no. 1-4)
# Jalankan: python sesi5/latihan/app_latihan_sesi5.py  -> buka http://127.0.0.1:8050
#
# 1. KPI card kelima: rata-rata jumlah keluhan
# 2. Grafik kedua (churn rate per region), disusun berdampingan dengan CSS grid
# 3. DataTable dengan sort_action="native" dan page_size=5
# 4. Gaya dipindah ke assets/style.css (folder sesi5/latihan/assets) dan dipakai via className
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "data" / "customer_churn.csv", parse_dates=["signup_date"])

ringkas = (df.groupby("contract_type")
             .agg(pelanggan=("customer_id", "count"), churn_rate=("churn", "mean"))
             .reset_index())
ringkas["churn_rate"] = (ringkas["churn_rate"] * 100).round(1)

per_region = (df.groupby("region", as_index=False)["churn"].mean()
                .rename(columns={"churn": "churn_rate"}))
per_region["churn_rate"] = (per_region["churn_rate"] * 100).round(1)
per_region = per_region.sort_values("churn_rate", ascending=False)

fig_kontrak = px.bar(ringkas, x="contract_type", y="churn_rate", template="plotly_white",
                     color_discrete_sequence=["#C44E52"], text_auto=".1f",
                     labels={"contract_type": "Jenis kontrak", "churn_rate": "Churn rate (%)"},
                     title="Churn rate per jenis kontrak")
fig_region = px.bar(per_region, x="region", y="churn_rate", template="plotly_white",
                    color_discrete_sequence=["#4C72B0"], text_auto=".1f",
                    labels={"region": "Region", "churn_rate": "Churn rate (%)"},
                    title="Churn rate per region")
for f in (fig_kontrak, fig_region):
    f.update_layout(height=350)

app = Dash(__name__, title="Latihan Sesi 5")   # assets/ di samping file ini dimuat otomatis


def kartu(judul, nilai):
    return html.Div([html.P(judul, className="kartu-judul"),
                     html.H2(nilai, className="kartu-nilai")], className="kartu")


app.layout = html.Div(className="halaman", children=[
    html.H1("Dashboard Churn — Latihan Sesi 5"),
    html.P("KPI ke-5, dua grafik berdampingan, tabel dengan sorting & paging, dan CSS eksternal."),

    # 1. Lima KPI card
    html.Div(className="baris-kartu", children=[
        kartu("Total pelanggan", f"{len(df):,}"),
        kartu("Churn rate", f"{df.churn.mean():.1%}"),
        kartu("Rata-rata tenure", f"{df.tenure_months.mean():.1f} bln"),
        kartu("Region", df.region.nunique()),
        kartu("Rata-rata keluhan", f"{df.num_complaints.mean():.2f}"),
    ]),

    # 2. Dua grafik berdampingan (CSS grid)
    html.H3("Perbandingan churn rate"),
    html.Div(className="grid-2", children=[dcc.Graph(figure=fig_kontrak),
                                           dcc.Graph(figure=fig_region)]),

    # 3. DataTable dengan sorting dan paging
    html.H3("Ringkasan per kontrak dan region"),
    dash_table.DataTable(
        data=df.groupby(["contract_type", "region"], as_index=False)
               .agg(pelanggan=("customer_id", "count"), churn_rate=("churn", "mean"))
               .round(3).to_dict("records"),
        columns=[{"name": c, "id": c} for c in ["contract_type", "region", "pelanggan", "churn_rate"]],
        sort_action="native", page_size=5,
        style_cell={"padding": "6px", "textAlign": "left"},
        style_header={"fontWeight": "bold", "background": "#E9EDF5"}),

    html.Hr(),
    html.Small("Sumber: data latihan sintetis customer_churn.csv"),
])

if __name__ == "__main__":
    app.run(debug=True, port=8050)
