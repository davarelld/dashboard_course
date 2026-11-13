# sesi6/latihan/latihan_sesi6.py — jawaban Latihan Mandiri Sesi 6 (no. 1-4)
# Jalankan: python sesi6/latihan/latihan_sesi6.py  -> 4 file HTML di sesi6/latihan/output/
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATUS = {"Bertahan": "#2a78d6", "Churn": "#eb6834"}


def load():
    df = pd.read_csv(ROOT / "data" / "customer_churn.csv", parse_dates=["signup_date"])
    df["status"] = df["churn"].map({0: "Bertahan", 1: "Churn"})
    return df


def buat_figur(df):
    fig = {}

    # 1. Bar horizontal churn rate per payment_method, tertinggi di paling atas, + garis rata-rata
    pm = (df.groupby("payment_method", as_index=False)["churn"].mean()
            .sort_values("churn", ascending=True))          # horizontal: baris terakhir = paling atas
    f = px.bar(pm, x="churn", y="payment_method", orientation="h", text_auto=".1%",
               color_discrete_sequence=["#eb6834"],
               labels={"churn": "Churn rate", "payment_method": ""},
               title="Churn rate per metode pembayaran (diurutkan dari tertinggi)")
    f.add_vline(x=df.churn.mean(), line_dash="dot", annotation_text="rata-rata nasional")
    f.update_xaxes(tickformat=".0%")
    fig["1_bar_horizontal"] = f

    # 2. Bubble chart: scatter dengan size="support_calls"
    fig["2_bubble"] = px.scatter(
        df, x="tenure_months", y="monthly_charges", color="status", size="support_calls",
        size_max=14, opacity=0.55, color_discrete_map=STATUS, hover_name="customer_id",
        hover_data=["region", "contract_type", "support_calls"],
        labels={"tenure_months": "Tenure (bulan)", "monthly_charges": "Tagihan (Rp)",
                "status": "Status"},
        title="Tenure vs tagihan (ukuran gelembung = jumlah panggilan CS)")

    # 3. Sunburst region -> segmen -> kontrak
    #    Cara membaca: lingkar dalam = region, tengah = segmen, luar = kontrak.
    #    Luas irisan sebanding dengan jumlah pelanggan; klik irisan untuk memperbesar cabang itu.
    cnt = (df.groupby(["region", "segment", "contract_type"]).size()
             .reset_index(name="pelanggan"))
    fig["3_sunburst"] = px.sunburst(
        cnt, path=["region", "segment", "contract_type"], values="pelanggan",
        title="Sunburst: region → segmen → kontrak (luas = jumlah pelanggan)")

    # 4. Gauge churn rate keseluruhan
    fig["4_gauge"] = go.Figure(go.Indicator(
        mode="gauge+number", value=df.churn.mean() * 100, number={"suffix": "%"},
        title={"text": "Churn rate keseluruhan"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#eb6834"}}))

    for f in fig.values():
        f.update_layout(template="plotly_white")
    return fig


if __name__ == "__main__":
    OUT = Path(__file__).resolve().parent / "output"
    OUT.mkdir(exist_ok=True)
    figs = buat_figur(load())
    for nama, f in figs.items():
        f.write_html(OUT / f"{nama}.html", include_plotlyjs="cdn")
    print(f"{len(figs)} chart latihan tersimpan di", OUT)
