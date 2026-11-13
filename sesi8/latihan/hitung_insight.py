# sesi8/latihan/hitung_insight.py — menghitung insight & rekomendasi (bab 8.7) dari data + model
# Jalankan: python sesi8/latihan/hitung_insight.py
# Hasil : sesi8/latihan/insight_dan_rekomendasi.md  (juga dicetak di terminal)
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))
from utils.model_utils import load_model, load_metadata, predict

META, MODEL = load_metadata(), load_model()
raw = pd.read_csv(ROOT / "data" / "customer_churn.csv", parse_dates=["signup_date"])
raw["total_charges"] = raw["total_charges"].fillna(raw["monthly_charges"] * raw["tenure_months"])
D = predict(MODEL, raw, META)
baru = predict(MODEL, pd.read_csv(ROOT / "data" / "new_customers.csv"), META)


def rp(x):
    return f"Rp{x:,.0f}".replace(",", ".")


def pct(x, d=1):
    return f"{x * 100:.{d}f}%".replace(".", ",")


def num(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


H = D[D.risk_category == "Tinggi"]
share = lambda col: D.groupby(col).apply(lambda g: (g.risk_category == "Tinggi").mean(),
                                         include_groups=False).sort_values(ascending=False)
pay, reg = share("payment_method"), share("region")
churn_by_risk = D.groupby("risk_category").churn.mean()
aktif_tinggi = H[H.churn == 0]
b_tinggi = baru[baru.risk_category == "Tinggi"]

insights = [
    (f"{len(H):,} pelanggan ({pct(len(H) / len(D))}) berada pada kategori risiko tinggi, dengan total "
     f"tagihan {rp(H.monthly_charges.sum())} per bulan.",
     "Jadikan kelompok ini prioritas program retensi bulan ini."),
    (f"{pct((H.contract_type == 'Bulanan').mean(), 0)} pelanggan risiko tinggi berkontrak Bulanan.",
     "Program migrasi ke kontrak Tahunan dengan insentif diskon untuk pelanggan Bulanan berisiko tinggi."),
    (f"Rata-rata tenure pelanggan risiko tinggi {num(H.tenure_months.mean())} bulan, dibanding "
     f"{num(D.tenure_months.mean())} bulan untuk seluruh pelanggan.",
     "Perkuat onboarding dan kontak proaktif pada 12 bulan pertama."),
    (f"Rata-rata keluhan pelanggan risiko tinggi {num(H.num_complaints.mean(), 2)}, dibanding "
     f"{num(D.num_complaints.mean(), 2)} untuk seluruh pelanggan.",
     "Terapkan SLA penyelesaian keluhan maksimal 48 jam untuk pelanggan berisiko tinggi."),
    (f"Proporsi risiko tinggi per metode pembayaran: " +
     ", ".join(f"{k} {pct(v)}" for k, v in pay.items()) + f". Tertinggi: {pay.index[0]}.",
     f"Dorong autodebit atau e-wallet untuk mengurangi friksi pembayaran pada pengguna {pay.index[0]}."),
    (f"{reg.index[0]} memiliki proporsi risiko tinggi terbesar ({pct(reg.iloc[0])}), sedangkan "
     f"{reg.index[-1]} terendah ({pct(reg.iloc[-1])}).",
     f"Prioritaskan kampanye retensi regional di {reg.index[0]}."),
    (f"Kategori risiko konsisten dengan data historis: churn aktual {pct(churn_by_risk['Tinggi'])} pada "
     f"kelompok Tinggi, {pct(churn_by_risk['Sedang'])} pada Sedang, dan {pct(churn_by_risk['Rendah'])} "
     f"pada Rendah. Catatan: model dilatih dengan data ini, sehingga angkanya cenderung lebih baik "
     f"daripada pada pelanggan baru; acuan yang adil adalah metrik holdout "
     f"(ROC-AUC {META['holdout_metrics']['roc_auc']}, akurasi {META['holdout_metrics']['accuracy']}, "
     f"F1 {META['holdout_metrics']['f1']}).",
     "Gunakan kategori risiko sebagai alat prioritisasi, bukan kepastian."),
    (f"{len(aktif_tinggi):,} pelanggan yang masih aktif (belum churn) masuk kategori risiko tinggi.",
     "Jadikan pelanggan ini daftar kerja pertama tim retensi minggu ini."),
    (f"Pada {len(baru)} pelanggan baru (new_customers.csv), {len(b_tinggi)} berisiko tinggi dan "
     f"{int(baru.predicted_churn.sum())} diprediksi churn (threshold {META['decision_threshold']}); "
     f"tagihan bulanan berisiko tinggi {rp(b_tinggi.monthly_charges.sum())}.",
     "Jalankan inference rutin untuk pelanggan baru dan masukkan yang berisiko tinggi ke daftar kerja."),
]

md = ["# Insight & Rekomendasi — Customer Churn Intelligence Dashboard", "",
      "Dihitung otomatis dari `data/customer_churn.csv`, `data/new_customers.csv`, dan model final "
      "(`python sesi8/latihan/hitung_insight.py`).", "",
      "| # | Insight | Rekomendasi |", "|---|---------|-------------|"]
md += [f"| {i} | {a} | {b} |" for i, (a, b) in enumerate(insights, 1)]
md += ["", "## Struktur presentasi 5–7 menit", "",
       "1. Masalah bisnis (30 detik) — siapa pelanggan yang berisiko churn dan apa tindakannya.",
       "2. Data dan model (45 detik) — 3.000 pelanggan, model final GradientBoosting, arti probabilitas "
       "dan kategori risiko (Rendah < 0,30 · Sedang 0,30–0,60 · Tinggi ≥ 0,60).",
       "3. Tur dashboard (2 menit) — KPI, chart utama, filter, tabel prioritas.",
       "4. Demo interaksi (1 menit) — satu filter dan satu simulasi prediksi langsung.",
       "5. Insight (1,5 menit) — 3 sampai 5 temuan terpenting di atas.",
       "6. Rekomendasi dan keterbatasan (1 menit) — tindakan dan batasan data/model "
       "(data sintetis, model dilatih pada data yang sama).", "",
       "## Template final project (isi minimum)", "",
       "| Bagian | Isian |", "|---|---|",
       "| 1. Business Problem | Pelanggan mana yang berisiko churn, di segmen mana risiko terkonsentrasi, "
       "dan apa tindakannya? |",
       f"| 2. Data Understanding | customer_churn.csv — {len(D):,} baris, 13 kolom, target `churn` "
       f"({pct(D.churn.mean())} churn); `total_charges` kosong pada {int(raw.total_charges.isna().sum()) or 0} "
       "baris sebelum diisi bulanan × tenure |",
       "| 3. EDA | Sesi 2; churn tertinggi pada kontrak Bulanan dan tenure pendek |",
       "| 4. Visualization | 6 chart Plotly + gauge di `sesi8/app_final_dashboard.py` |",
       f"| 5. Final ML Model | {META['algorithm']}, tanpa training ulang |",
       "| 6. Model Loading & Inference | `utils/model_utils.py` — load, validate_input, predict |",
       "| 7. Prediction Output | churn_probability, predicted_churn, risk_category |",
       "| 8. Interactive Components | 5 filter sidebar + form simulasi 9 input |",
       "| 9. Callback / App Logic | `update_overview` (5 filter → KPI, 6 chart, tabel) dan "
       "`run_prediction` (tombol + 9 State) |",
       "| 10. Dashboard | 4 KPI, 6 visualisasi, 5 filter, prediksi, tabel prioritas |",
       "| 11. Insight & Recommendation | Lihat tabel di atas |"]
out = ROOT / "sesi8" / "latihan" / "insight_dan_rekomendasi.md"
out.write_text("\n".join(md) + "\n", encoding="utf-8")
print("\n".join(f"{i}. {a}\n   -> {b}" for i, (a, b) in enumerate(insights, 1)))
print("\nTersimpan di", out)
