# Insight & Rekomendasi — Customer Churn Intelligence Dashboard

Dihitung otomatis dari `data/customer_churn.csv`, `data/new_customers.csv`, dan model final (`python sesi8/latihan/hitung_insight.py`).

| # | Insight | Rekomendasi |
|---|---------|-------------|
| 1 | 605 pelanggan (20,2%) berada pada kategori risiko tinggi, dengan total tagihan Rp285.260.000 per bulan. | Jadikan kelompok ini prioritas program retensi bulan ini. |
| 2 | 96% pelanggan risiko tinggi berkontrak Bulanan. | Program migrasi ke kontrak Tahunan dengan insentif diskon untuk pelanggan Bulanan berisiko tinggi. |
| 3 | Rata-rata tenure pelanggan risiko tinggi 14,9 bulan, dibanding 26,5 bulan untuk seluruh pelanggan. | Perkuat onboarding dan kontak proaktif pada 12 bulan pertama. |
| 4 | Rata-rata keluhan pelanggan risiko tinggi 1,89, dibanding 1,13 untuk seluruh pelanggan. | Terapkan SLA penyelesaian keluhan maksimal 48 jam untuk pelanggan berisiko tinggi. |
| 5 | Proporsi risiko tinggi per metode pembayaran: Transfer Bank 25,4%, Kartu Kredit 18,8%, E-Wallet 18,8%, Virtual Account 15,6%. Tertinggi: Transfer Bank. | Dorong autodebit atau e-wallet untuk mengurangi friksi pembayaran pada pengguna Transfer Bank. |
| 6 | Sumatera memiliki proporsi risiko tinggi terbesar (22,1%), sedangkan Sulawesi terendah (17,9%). | Prioritaskan kampanye retensi regional di Sumatera. |
| 7 | Kategori risiko konsisten dengan data historis: churn aktual 80,0% pada kelompok Tinggi, 44,4% pada Sedang, dan 9,1% pada Rendah. Catatan: model dilatih dengan data ini, sehingga angkanya cenderung lebih baik daripada pada pelanggan baru; acuan yang adil adalah metrik holdout (ROC-AUC 0.7875, akurasi 0.7133, F1 0.5585). | Gunakan kategori risiko sebagai alat prioritisasi, bukan kepastian. |
| 8 | 121 pelanggan yang masih aktif (belum churn) masuk kategori risiko tinggi. | Jadikan pelanggan ini daftar kerja pertama tim retensi minggu ini. |
| 9 | Pada 200 pelanggan baru (new_customers.csv), 45 berisiko tinggi dan 64 diprediksi churn (threshold 0.5); tagihan bulanan berisiko tinggi Rp21.911.000. | Jalankan inference rutin untuk pelanggan baru dan masukkan yang berisiko tinggi ke daftar kerja. |

## Struktur presentasi 5–7 menit

1. Masalah bisnis (30 detik) — siapa pelanggan yang berisiko churn dan apa tindakannya.
2. Data dan model (45 detik) — 3.000 pelanggan, model final GradientBoosting, arti probabilitas dan kategori risiko (Rendah < 0,30 · Sedang 0,30–0,60 · Tinggi ≥ 0,60).
3. Tur dashboard (2 menit) — KPI, chart utama, filter, tabel prioritas.
4. Demo interaksi (1 menit) — satu filter dan satu simulasi prediksi langsung.
5. Insight (1,5 menit) — 3 sampai 5 temuan terpenting di atas.
6. Rekomendasi dan keterbatasan (1 menit) — tindakan dan batasan data/model (data sintetis, model dilatih pada data yang sama).

## Template final project (isi minimum)

| Bagian | Isian |
|---|---|
| 1. Business Problem | Pelanggan mana yang berisiko churn, di segmen mana risiko terkonsentrasi, dan apa tindakannya? |
| 2. Data Understanding | customer_churn.csv — 3,000 baris, 13 kolom, target `churn` (34,9% churn); `total_charges` kosong pada 0 baris sebelum diisi bulanan × tenure |
| 3. EDA | Sesi 2; churn tertinggi pada kontrak Bulanan dan tenure pendek |
| 4. Visualization | 6 chart Plotly + gauge di `sesi8/app_final_dashboard.py` |
| 5. Final ML Model | GradientBoostingClassifier (scikit-learn Pipeline), tanpa training ulang |
| 6. Model Loading & Inference | `utils/model_utils.py` — load, validate_input, predict |
| 7. Prediction Output | churn_probability, predicted_churn, risk_category |
| 8. Interactive Components | 5 filter sidebar + form simulasi 9 input |
| 9. Callback / App Logic | `update_overview` (5 filter → KPI, 6 chart, tabel) dan `run_prediction` (tombol + 9 State) |
| 10. Dashboard | 4 KPI, 6 visualisasi, 5 filter, prediksi, tabel prioritas |
| 11. Insight & Recommendation | Lihat tabel di atas |
