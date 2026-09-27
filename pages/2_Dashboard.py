import streamlit as st
import random

from utils.style import load_style

# =========================
# STYLE
# =========================

load_style()

# =========================
# LOGIN ADMIN
# =========================

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False


if not st.session_state.admin_login:

    st.title("🔐 Admin")

    st.write("Masukkan password untuk membuka dashboard.")

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Masukkan password...",
    )

    if st.button(
        "Masuk",
        type="primary",
        use_container_width=True,
    ):

        if password == "admin123":

            st.session_state.admin_login = True
            st.rerun()

        else:

            st.error("❌ Password salah.")

    st.stop()


# =========================
# HALAMAN
# =========================

st.title("🎓 Dashboard")

st.write("Pantau jawaban yang masuk dan pilih kelompok secara acak.")

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

if pertemuan is None:
    st.info("Silakan pilih pertemuan terlebih dahulu.")
    st.stop()


st.divider()


# =========================
# DATA DUMMY SUBMISSION
# =========================

submission = [
    {
        "nomor": 1,
        "anggota": ["Andi", "Budi", "Citra"],
        "jawaban": (
            "Data penjualan sebuah toko berupa jumlah "
            "barang yang terjual setiap hari. Data tersebut "
            "diolah menjadi informasi total penjualan, "
            "kemudian diketahui bahwa penjualan tertinggi "
            "terjadi pada akhir pekan. Insight tersebut "
            "digunakan untuk menentukan keputusan "
            "menambah stok sebelum akhir pekan."
        ),
        "waktu": "09:42",
        "status": "Belum Dipanggil",
    },
    {
        "nomor": 2,
        "anggota": ["Dinda", "Eka"],
        "jawaban": (
            "Data nilai mahasiswa digunakan untuk menghitung "
            "rata-rata nilai kelas. Dari informasi tersebut "
            "terlihat bahwa sebagian besar mahasiswa "
            "memiliki nilai rendah pada materi tertentu. "
            "Dosen kemudian memutuskan memberikan latihan "
            "tambahan."
        ),
        "waktu": "09:45",
        "status": "Belum Dipanggil",
    },
    {
        "nomor": 3,
        "anggota": ["Fajar", "Gilang", "Hana"],
        "jawaban": (
            "Data kehadiran mahasiswa dikumpulkan setiap "
            "pertemuan. Data tersebut menghasilkan informasi "
            "persentase kehadiran. Insight menunjukkan "
            "beberapa mahasiswa sering tidak hadir. "
            "Keputusan yang diambil adalah melakukan "
            "pendekatan kepada mahasiswa tersebut."
        ),
        "waktu": "09:47",
        "status": "Sudah Dipanggil",
    },
    {
        "nomor": 4,
        "anggota": ["Intan", "Joko"],
        "jawaban": (
            "Data penggunaan listrik selama satu minggu "
            "diolah menjadi informasi penggunaan listrik "
            "setiap hari. Insight menunjukkan penggunaan "
            "tertinggi terjadi pada sore hari. Keputusan "
            "yang diambil adalah mengurangi penggunaan "
            "peralatan yang tidak diperlukan."
        ),
        "waktu": "09:51",
        "status": "Belum Dipanggil",
    },
    {
        "nomor": 5,
        "anggota": ["Kiki", "Lala", "Maya"],
        "jawaban": (
            "Data transaksi pelanggan digunakan untuk "
            "mengetahui produk yang paling sering dibeli. "
            "Insight menunjukkan produk tertentu memiliki "
            "permintaan tinggi. Keputusan yang diambil "
            "adalah menambah stok produk tersebut."
        ),
        "waktu": "09:54",
        "status": "Belum Dipanggil",
    },
]


# =========================
# RINGKASAN
# =========================

st.subheader("📊 Ringkasan")

total_submission = len(submission)

sudah_dipanggil = sum(1 for item in submission if item["status"] == "Sudah Dipanggil")

belum_dipanggil = total_submission - sudah_dipanggil


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📝 Jawaban Masuk", total_submission)

with col2:
    st.metric("✅ Sudah Dipanggil", sudah_dipanggil)

with col3:
    st.metric("⏳ Belum Dipanggil", belum_dipanggil)


st.divider()

# =========================
# MAHASISWA BELUM MENGUMPULKAN
# =========================

st.divider()

st.subheader("👤 Mahasiswa Belum Mengumpulkan")

# Daftar seluruh mahasiswa di kelas
daftar_mahasiswa = [
    "Andi",
    "Budi",
    "Citra",
    "Dinda",
    "Eka",
    "Fajar",
    "Gilang",
    "Hana",
    "Intan",
    "Joko",
    "Kiki",
    "Lala",
    "Maya",
    "Nanda",
    "Oki",
    "Putri",
    "Rizky",
    "Salsa",
    "Tio",
    "Vina",
]


# Ambil semua mahasiswa yang sudah mengumpulkan
mahasiswa_sudah_mengumpulkan = []

for item in submission:

    for nama in item["anggota"]:

        mahasiswa_sudah_mengumpulkan.append(nama)


# Cari mahasiswa yang belum mengumpulkan
mahasiswa_belum_mengumpulkan = [
    nama for nama in daftar_mahasiswa if nama not in mahasiswa_sudah_mengumpulkan
]


# Ringkasan
col1, col2 = st.columns(2)

with col1:
    st.metric("👥 Total Mahasiswa", len(daftar_mahasiswa))

with col2:
    st.metric("⏳ Belum Mengumpulkan", len(mahasiswa_belum_mengumpulkan))


# Tampilkan daftar
if mahasiswa_belum_mengumpulkan:

    for i, nama in enumerate(mahasiswa_belum_mengumpulkan, start=1):

        st.write(f"{i}. {nama}")

else:

    st.success("🎉 Semua mahasiswa sudah mengumpulkan.")


# =========================
# RANDOM
# =========================

st.subheader("🎲 Random Jawaban")

belum_dipanggil_data = [
    item for item in submission if item["status"] == "Belum Dipanggil"
]


if st.button("🎲 RANDOM", type="primary", use_container_width=True):

    if belum_dipanggil_data:

        terpilih = random.choice(belum_dipanggil_data)

        st.session_state.submission_terpilih = terpilih["nomor"]

    else:

        st.warning("Semua kelompok sudah dipanggil.")


# =========================
# HASIL RANDOM
# =========================

if "submission_terpilih" in st.session_state:

    nomor_terpilih = st.session_state.submission_terpilih

    terpilih = next(item for item in submission if item["nomor"] == nomor_terpilih)

    st.success(f"🎉 Kelompok {terpilih['nomor']}")

    st.write(f"🕘 **Waktu mengumpulkan:** " f"{terpilih['waktu']}")

    st.subheader("👥 Anggota")

    for nama in terpilih["anggota"]:
        st.write(f"- {nama}")

    st.subheader("💬 Jawaban")

    st.info(terpilih["jawaban"])

    if st.button("✓ Tandai Sudah Dipanggil", use_container_width=True):

        terpilih["status"] = "Sudah Dipanggil"

        del st.session_state.submission_terpilih

        st.rerun()


st.divider()


# =========================
# DAFTAR JAWABAN
# =========================

st.subheader("📋 Jawaban Masuk")

for item in submission:

    if item["status"] == "Sudah Dipanggil":
        icon = "✅"
    else:
        icon = "⏳"

    with st.expander(f"{icon} Kelompok {item['nomor']} • " f"{item['waktu']}"):

        st.write("**Anggota:**")

        for nama in item["anggota"]:
            st.write(f"- {nama}")

        st.write("**Jawaban:**")

        st.write(item["jawaban"])

        st.write(f"**Status:** {item['status']}")
