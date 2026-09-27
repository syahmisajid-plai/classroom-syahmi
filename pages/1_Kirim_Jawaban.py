import streamlit as st

from utils.style import load_style
from utils.supabase_client import supabase

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


# =========================
# MATA KULIAH
# =========================

courses_response = (
    supabase.table("courses").select("id, code, name").eq("is_active", True).execute()
)

courses = courses_response.data

mata_kuliah_options = {course["name"]: course["id"] for course in courses}

mata_kuliah = st.selectbox(
    "Mata Kuliah",
    list(mata_kuliah_options.keys()),
    index=None,
    placeholder="Pilih mata kuliah...",
)


# Jika mata kuliah belum dipilih
if mata_kuliah is None:
    st.info("Silakan pilih mata kuliah terlebih dahulu.")
    st.stop()


# Ambil ID mata kuliah yang dipilih
course_id = mata_kuliah_options[mata_kuliah]


# =========================
# PERTEMUAN
# =========================

meetings_response = (
    supabase.table("meetings")
    .select("id, meeting_number, title, question")
    .eq("course_id", course_id)
    .eq("is_active", True)
    .order("meeting_number")
    .execute()
)

meetings = meetings_response.data

pertemuan_options = {
    f"Pertemuan {meeting['meeting_number']}": meeting for meeting in meetings
}

pertemuan = st.selectbox(
    "Pertemuan",
    list(pertemuan_options.keys()),
    index=None,
    placeholder="Pilih pertemuan...",
)


# Jika pertemuan belum dipilih
if pertemuan is None:
    st.info("Silakan pilih pertemuan terlebih dahulu.")
    st.stop()


# Ambil data pertemuan yang dipilih
meeting = pertemuan_options[pertemuan]

meeting_id = meeting["id"]
pertanyaan = meeting["question"]


# =========================
# PERTANYAAN
# =========================

st.divider()

st.subheader("❓ Pertanyaan")

st.info(pertanyaan)


# =========================
# ANGGOTA KELOMPOK
# =========================

st.divider()

st.subheader("👥 Anggota Kelompok")

st.caption("Pilih nama mahasiswa yang menjadi anggota kelompok.")


# =========================
# AMBIL DATA MAHASISWA
# =========================

students_response = (
    supabase.table("students")
    .select("id, nim, name")
    .eq("is_active", True)
    .order("name")
    .execute()
)

students = students_response.data

daftar_mahasiswa = {student["name"]: student["id"] for student in students}


# =========================
# JUMLAH ANGGOTA
# =========================

if "jumlah_anggota" not in st.session_state:
    st.session_state.jumlah_anggota = 2


nama_anggota = []

for i in range(st.session_state.jumlah_anggota):

    nama_terpilih = [nama for nama in nama_anggota if nama is not None]

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

if st.button(
    "🚀 Kirim Jawaban",
    type="primary",
    use_container_width=True,
):

    nama_valid = [nama.strip() for nama in nama_anggota if nama and nama.strip()]

    if len(nama_valid) == 0:
        st.warning("Silakan masukkan minimal satu nama anggota.")

    elif jawaban.strip() == "":
        st.warning("Silakan isi jawaban kelompok terlebih dahulu.")

    else:

        try:
            # =========================
            # SIMPAN SUBMISSION
            # =========================

            response = (
                supabase.table("submissions")
                .insert(
                    {
                        "meeting_id": meeting_id,
                        "answer": jawaban.strip(),
                    }
                )
                .execute()
            )

            submission_id = response.data[0]["id"]

            # =========================
            # SIMPAN ANGGOTA KELOMPOK
            # =========================

            members_data = [
                {
                    "submission_id": submission_id,
                    "student_id": daftar_mahasiswa[nama],
                }
                for nama in nama_valid
            ]

            supabase.table("submission_members").insert(members_data).execute()

            # =========================
            # BERHASIL
            # =========================

            st.success("🎉 Jawaban kelompok berhasil dikirim!")

            st.markdown(f"""
                ### {mata_kuliah}
                **{pertemuan}**
                """)

            st.write("**👥 Anggota Kelompok**")
            st.write(" • ".join(nama_valid))

            st.info("💬 Jawaban kelompok telah tersimpan.")

            st.caption(
                "Terima kasih. Jawaban Anda telah berhasil dikirim kepada dosen."
            )

        except Exception as e:
            st.error("❌ Gagal menyimpan jawaban ke Supabase.")
            st.exception(e)
