import streamlit as st
import random

from datetime import datetime
from zoneinfo import ZoneInfo

from utils.style import load_style
from utils.supabase_client import supabase

# =========================
# STYLE
# =========================

load_style()


def format_waktu(timestamp):
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    dt = dt.astimezone(ZoneInfo("Asia/Jakarta"))
    return dt.strftime("%d %B %Y, %H:%M WIB")


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

if mata_kuliah is None:
    st.info("Silakan pilih mata kuliah terlebih dahulu.")
    st.stop()


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

if pertemuan is None:
    st.info("Silakan pilih pertemuan terlebih dahulu.")
    st.stop()


meeting = pertemuan_options[pertemuan]

meeting_id = meeting["id"]


st.divider()


# =========================
# AMBIL SUBMISSION
# =========================

submissions_response = (
    supabase.table("submissions")
    .select(
        "id, answer, submitted_at, called_at, "
        "submission_members(student_id, students(id, nim, name))"
    )
    .eq("meeting_id", meeting_id)
    .order("submitted_at")
    .execute()
)

submission = submissions_response.data


# =========================
# FORMAT DATA
# =========================

for index, item in enumerate(submission, start=1):

    item["nomor"] = index

    item["anggota"] = [
        member["students"]["name"] for member in item["submission_members"]
    ]

    item["waktu"] = item["submitted_at"]

    if item["called_at"] is None:
        item["status"] = "Belum Dipanggil"
    else:
        item["status"] = "Sudah Dipanggil"


# =========================
# RINGKASAN
# =========================

st.subheader("📊 Ringkasan")

total_submission = len(submission)

sudah_dipanggil = sum(1 for item in submission if item["called_at"] is not None)

belum_dipanggil = total_submission - sudah_dipanggil


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📝 Jawaban Masuk",
        total_submission,
    )

with col2:
    st.metric(
        "✅ Sudah Dipanggil",
        sudah_dipanggil,
    )

with col3:
    st.metric(
        "⏳ Belum Dipanggil",
        belum_dipanggil,
    )


st.divider()


# =========================
# MAHASISWA BELUM MENGUMPULKAN
# =========================

st.subheader("👤 Mahasiswa Belum Mengumpulkan")


# Ambil seluruh mahasiswa yang terdaftar
enrollments_response = (
    supabase.table("enrollments")
    .select("student_id, students(id, nim, name)")
    .eq("course_id", course_id)
    .execute()
)

enrollments = enrollments_response.data


# Semua mahasiswa di kelas
daftar_mahasiswa = {
    enrollment["students"]["id"]: enrollment["students"]["name"]
    for enrollment in enrollments
}


# Mahasiswa yang sudah mengumpulkan
mahasiswa_sudah_mengumpulkan = set()

for item in submission:

    for member in item["submission_members"]:

        mahasiswa_sudah_mengumpulkan.add(member["student_id"])


# Mahasiswa yang belum mengumpulkan
mahasiswa_belum_mengumpulkan = [
    nama
    for student_id, nama in daftar_mahasiswa.items()
    if student_id not in mahasiswa_sudah_mengumpulkan
]


# Ringkasan
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "👥 Total Mahasiswa",
        len(daftar_mahasiswa),
    )

with col2:
    st.metric(
        "⏳ Belum Mengumpulkan",
        len(mahasiswa_belum_mengumpulkan),
    )


# Tampilkan daftar
if mahasiswa_belum_mengumpulkan:
    with st.expander(
        f"👀 Lihat daftar mahasiswa ({len(mahasiswa_belum_mengumpulkan)} orang)"
    ):
        for i, nama in enumerate(mahasiswa_belum_mengumpulkan, start=1):
            st.write(f"{i}. {nama}")
else:
    st.success("🎉 Semua mahasiswa sudah mengumpulkan.")


st.divider()


# =========================
# RANDOM
# =========================

st.subheader("🎲 Random Jawaban")

belum_dipanggil_data = [item for item in submission if item["called_at"] is None]


if st.button(
    "🎲 RANDOM",
    type="primary",
    use_container_width=True,
):

    if belum_dipanggil_data:

        terpilih = random.choice(belum_dipanggil_data)

        st.session_state.submission_terpilih = terpilih["id"]

    else:

        st.warning("Semua kelompok sudah dipanggil.")


# =========================
# HASIL RANDOM
# =========================

if "submission_terpilih" in st.session_state:

    submission_id = st.session_state.submission_terpilih

    terpilih = next(
        (item for item in submission if item["id"] == submission_id),
        None,
    )

    if terpilih is not None:

        st.success(f"🎉 Kelompok {terpilih['nomor']}")

        st.write("**Waktu mengumpulkan:** " f"{format_waktu(terpilih['waktu'])}")

        st.subheader("👥 Anggota")

        for nama in terpilih["anggota"]:
            st.write(f"- {nama}")

        st.subheader("💬 Jawaban")

        st.info(terpilih["answer"])

        # =========================
        # TANDAI SUDAH DIPANGGIL
        # =========================

        if st.button(
            "✓ Tandai Sudah Dipanggil",
            use_container_width=True,
        ):

            (
                supabase.table("submissions")
                .update({"called_at": "now()"})
                .eq("id", submission_id)
                .execute()
            )

            del st.session_state.submission_terpilih

            st.rerun()


st.divider()


# =========================
# DAFTAR JAWABAN
# =========================

st.subheader("📋 Jawaban Masuk")


for item in submission:

    if item["called_at"] is not None:
        icon = "✅"
    else:
        icon = "⏳"

    with st.expander(
        f"{icon} Kelompok {item['nomor']} • " f"{format_waktu(item['waktu'])}"
    ):

        st.write("**Anggota:**")

        for nama in item["anggota"]:
            st.write(f"- {nama}")

        st.write("**Jawaban:**")

        st.write(item["answer"])

        st.write(f"**Status:** {item['status']}")
