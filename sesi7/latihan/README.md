# Latihan Mandiri Sesi 7
Jalankan dari folder akar: `python sesi7/latihan/app_latihan_callback.py` → http://127.0.0.1:8052

| No. | Soal | Di mana jawabannya |
|-----|------|--------------------|
| 1 | Checklist `internet_service` ke `filter_df()` | `dcc.Checklist(id="cl-layanan")`, parameter `layanan` di `filter_df` |
| 2 | Output kelima: histogram tenure terfilter | `Output("g-hist", "figure")` di `update_dashboard` |
| 3 | Klik titik scatter → detail pelanggan | `tampil_detail` + `custom_data=["customer_id"]` |
| 4 | `dcc.Store` menyimpan hasil filter | `store-data`; `update_tabel` membaca dari store |
| 5 | Tantangan: `selectedData` memfilter tabel | Input `g-scatter.selectedData` di `update_tabel` (box/lasso select) |
