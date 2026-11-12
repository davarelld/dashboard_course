
# app_latihan_mandiri.py — LATIHAN MANDIRI SESI 1

import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Latihan Mandiri Sesi 1",
    page_icon="🧩",
    layout="centered"
)

st.title("🧩 Latihan Mandiri Sesi 1")
st.write("Aplikasi Kalkulator Tagihan dan Profil Peserta.")

# ==================================================
# 1. KALKULATOR TAGIHAN INTERNET
# ==================================================

st.header("1. Kalkulator Tagihan Internet")

# Daftar harga layanan (termasuk layanan Satelit)
HARGA = {
    "DSL": 260_000,
    "Fiber": 420_000,
    "Mobile Broadband": 310_000,
    "Satelit": 550_000
}

DISKON = {
    "Bulanan": 0.00,
    "Tahunan": 0.10,
    "Dua Tahun": 0.18
}

layanan = st.selectbox("Jenis layanan", list(HARGA))

kontrak = st.radio(
    "Jenis kontrak",
    list(DISKON),
    horizontal=True
)

bulan = st.number_input(
    "Durasi (bulan)",
    min_value=1,
    max_value=72,
    value=12,
    step=1
)

ppn = st.checkbox("Tambahkan PPN 11%", value=True)

# ==================================================
# 2. DISKON PROMOSI TAMBAHAN
# ==================================================

st.subheader("2. Diskon Promosi Tambahan")

diskon_promo = st.slider(
    "Pilih diskon promosi (%)",
    min_value=0,
    max_value=20,
    value=0,
    step=1
)

# ==================================================
# 3. TOMBOL HITUNG DAN SESSION STATE
# ==================================================

st.subheader("3. Hasil Perhitungan")

# Inisialisasi session state untuk menghitung klik
if "jumlah_klik" not in st.session_state:
    st.session_state.jumlah_klik = 0

if st.button("Hitung", type="primary"):

    # Menambah jumlah klik tombol
    st.session_state.jumlah_klik += 1

    # Menghitung harga setelah diskon kontrak
    per_bulan = HARGA[layanan] * (1 - DISKON[kontrak])

    # Menghitung harga setelah diskon promosi
    per_bulan = per_bulan * (1 - diskon_promo / 100)

    # Menghitung total tagihan
    total = per_bulan * bulan * (1.11 if ppn else 1)

    # Menampilkan hasil
    st.success("Perhitungan berhasil!")

    st.metric(
        "Biaya per bulan",
        f"Rp{per_bulan:,.0f}".replace(",", ".")
    )

    st.metric(
        "Total estimasi tagihan",
        f"Rp{total:,.0f}".replace(",", ".")
    )

    st.write(f"Diskon kontrak: {DISKON[kontrak]:.0%}")
    st.write(f"Diskon promosi: {diskon_promo}%")

# Menampilkan jumlah klik tombol
st.info(
    f"Tombol Hitung sudah diklik sebanyak "
    f"{st.session_state.jumlah_klik} kali."
)

st.caption("Estimasi tagihan bersifat ilustratif untuk latihan.")

# ==================================================
# 4. APLIKASI PROFIL PESERTA
# ==================================================

st.divider()

st.header("4. Profil Peserta")

nama = st.text_input("Masukkan nama peserta")

divisi = st.selectbox(
    "Pilih divisi",
    ["Human Resources", "Finance", "Marketing", "IT", "Operations"]
)

pengalaman = st.slider(
    "Tahun pengalaman kerja",
    min_value=0,
    max_value=30,
    value=1
)

if st.button("Tampilkan Profil"):

    if nama:
        st.info(
            f"""
            **Ringkasan Profil Peserta**

            Nama: {nama}

            Divisi: {divisi}

            Pengalaman Kerja: {pengalaman} tahun
            """
        )
    else:
        st.warning("Silakan masukkan nama peserta terlebih dahulu.")
