import streamlit as st

from utils.style import load_style

# =========================
# STYLE
# =========================

load_style()


# =========================
# HALAMAN
# =========================

st.title("📝 Kirim Jawaban")

st.write("Silakan isi informasi kelompok dan jawaban hasil diskusi.")

st.divider()


# =========================
# INFORMASI TUGAS
# =========================

st.subheader("📚 Informasi Tugas")

mata_kuliah = st.selectbox(
    "Mata Kuliah",
    [
        "Pengantar Sains Data Terapan",
    ],
    index=None,
    placeholder="Pilih mata kuliah...",
)

# Jika mata kuliah belum dipilih
if mata_kuliah is None:
    st.info("Silakan pilih mata kuliah terlebih dahulu.")
    st.stop()


pertemuan = st.selectbox(
    "Pertemuan",
    [
        "Pertemuan 1",
    ],
    index=None,
    placeholder="Pilih pertemuan...",
)

# Jika pertemuan belum dipilih
if pertemuan is None:
    st.info("Silakan pilih pertemuan terlebih dahulu.")
    st.stop()


# =========================
# PERTANYAAN
# =========================

st.divider()

st.subheader("❓ Pertanyaan")

st.info(
    "Buatlah sebuah contoh kasus sederhana dengan alur "
    "**Data → Information → Insight → Decision**."
)


# =========================
# ANGGOTA KELOMPOK
# =========================

st.divider()

st.subheader("👥 Anggota Kelompok")

st.caption("Pilih nama mahasiswa yang menjadi anggota kelompok.")

daftar_mahasiswa = [
    "Ahmad Fauzan",
    "Budi Santoso",
    "Citra Lestari",
]

if "jumlah_anggota" not in st.session_state:
    st.session_state.jumlah_anggota = 2


nama_anggota = []

for i in range(st.session_state.jumlah_anggota):

    # Nama yang sudah dipilih pada anggota sebelumnya
    nama_terpilih = [nama for nama in nama_anggota if nama is not None]

    # Hanya tampilkan mahasiswa yang belum dipilih
    pilihan_mahasiswa = [nama for nama in daftar_mahasiswa if nama not in nama_terpilih]

    nama = st.selectbox(
        f"Nama Anggota {i + 1}",
        pilihan_mahasiswa,
        index=None,
        placeholder="Pilih nama mahasiswa...",
        key=f"nama_{i}",
    )

    nama_anggota.append(nama)


# =========================
# TAMBAH ANGGOTA
# =========================

if st.session_state.jumlah_anggota < len(daftar_mahasiswa):

    if st.button("➕ Tambah Anggota"):
        st.session_state.jumlah_anggota += 1
        st.rerun()


# =========================
# JAWABAN
# =========================

st.divider()

st.subheader("💬 Jawaban Kelompok")

jawaban = st.text_area(
    "Tuliskan jawaban hasil diskusi kelompok",
    placeholder="Tuliskan jawaban kelompok di sini...",
    height=250,
)


# =========================
# SUBMIT
# =========================

st.divider()

if st.button("🚀 Kirim Jawaban", type="primary", use_container_width=True):

    nama_valid = [nama.strip() for nama in nama_anggota if nama.strip()]

    if len(nama_valid) == 0:
        st.warning("Silakan masukkan minimal satu nama anggota.")

    elif jawaban.strip() == "":
        st.warning("Silakan isi jawaban kelompok terlebih dahulu.")

    else:
        st.success("Jawaban kelompok berhasil dikirim!")

        st.write("**Mata Kuliah:**", mata_kuliah)
        st.write("**Pertemuan:**", pertemuan)

        st.write("**Anggota:**")
        for nama in nama_valid:
            st.write(f"- {nama}")

        st.write("**Jawaban:**")
        st.write(jawaban)
