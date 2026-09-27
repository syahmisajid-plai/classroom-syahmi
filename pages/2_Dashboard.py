import streamlit as st
import random

from datetime import datetime
from zoneinfo import ZoneInfo
import time

from utils.style import load_style
from utils.supabase_client import supabase

# =========================
# STYLE
# =========================

load_style()


def format_waktu(timestamp):
    if not timestamp:
        return "-"

    try:
        timestamp = str(timestamp)

        # Ambil YYYY-MM-DD HH:MM:SS
        tanggal = timestamp[:10]
        waktu = timestamp[11:19]

        # Buat datetime dari bagian yang diperlukan saja
        dt = datetime.strptime(f"{tanggal} {waktu}", "%Y-%m-%d %H:%M:%S")

        # Timestamp Supabase adalah UTC
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

        # Konversi ke WIB
        dt = dt.astimezone(ZoneInfo("Asia/Jakarta"))

        return dt.strftime("%d %B %Y, %H:%M WIB")

    except Exception:
        return "-"


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

col1, col2 = st.columns([5, 1])

with col1:
    st.subheader("📚 Informasi Tugas")

with col2:
    if st.button(
        "🔄 Refresh",
        use_container_width=True,
    ):
        st.rerun()


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
        "submission_members(student_id, role, students(id, nim, name))"
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

        if member["role"] == "member":
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


@st.dialog("🎲 Random Kelompok")
def random_kelompok():

    if not belum_dipanggil_data:
        st.warning("Semua kelompok sudah dipanggil.")
        return

    st.markdown("### 🎲 Memilih Kelompok...")
    st.caption("Mohon tunggu sebentar.")

    # =========================
    # ANIMASI DADU
    # =========================

    dice_placeholder = st.empty()

    dice = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

    for _ in range(20):
        dice_placeholder.markdown(
            f"""
            <div style="
                text-align: center;
                font-size: 120px;
                line-height: 1;
                margin: 30px 0;
            ">
                {random.choice(dice)}
            </div>
            """,
            unsafe_allow_html=True,
        )

        time.sleep(0.12)

    # =========================
    # HASIL RANDOM
    # =========================

    # Random hanya dilakukan jika belum ada kelompok yang dipilih
    if "submission_terpilih" not in st.session_state:

        terpilih = random.choice(belum_dipanggil_data)

        st.session_state.submission_terpilih = terpilih["id"]

        # Mulai daftar penanggap sementara
        st.session_state.penanggap_sementara = []

    else:

        # Ambil kembali kelompok yang sudah dipilih
        terpilih = next(
            item
            for item in belum_dipanggil_data
            if item["id"] == st.session_state.submission_terpilih
        )

    # =========================
    # HASIL TERPILIH
    # =========================

    dice_placeholder.markdown(
        "<div style='text-align:center; font-size:80px;'>🎉</div>",
        unsafe_allow_html=True,
    )

    st.markdown(f"# Kelompok {terpilih['nomor']}")

    st.success("🎉 Kelompok terpilih!")

    st.divider()

    # =========================
    # ANGGOTA
    # =========================

    st.markdown("#### 👥 Anggota")

    for nama in terpilih["anggota"]:
        st.write(f"• {nama}")

    # =========================
    # JAWABAN
    # =========================

    st.subheader("💬 JAWABAN")

    st.text_area(
        "Jawaban kelompok",
        value=terpilih["answer"],
        height=220,
        disabled=True,
        label_visibility="collapsed",
    )

    st.caption(f"📅 Dikumpulkan · {format_waktu(terpilih['waktu'])}")

    st.divider()

    # =========================
    # PENANGGAP
    # =========================

    st.markdown("#### 🙋 Penanggap")

    # Ambil seluruh mahasiswa di kelas
    students_response = (
        supabase.table("enrollments")
        .select("student_id, students(id, name)")
        .eq(
            "course_id",
            course_id,
        )
        .execute()
    )

    students_data = students_response.data

    # ID anggota kelompok
    member_ids = {member["student_id"] for member in terpilih["submission_members"]}

    # Semua mahasiswa yang bukan anggota kelompok
    calon_penanggap = {
        item["students"]["name"]: item["student_id"]
        for item in students_data
        if item["student_id"] not in member_ids
    }

    # =========================
    # 3 SLOT PENANGGAP
    # =========================

    nama_mahasiswa = list(calon_penanggap.keys())

    pilihan_penanggap = []

    for i in range(3):

        penanggap = st.selectbox(
            f"Penanggap {i + 1}",
            [""] + nama_mahasiswa,
            index=0,
            key=f"penanggap_{i}",
            format_func=lambda x: ("Pilih mahasiswa..." if x == "" else x),
        )

        if penanggap:
            pilihan_penanggap.append(
                {
                    "student_id": calon_penanggap[penanggap],
                    "name": penanggap,
                }
            )

    # =========================
    # TANDAI
    # =========================

    if st.button(
        "✓ Tandai Sudah Dipanggil",
        type="primary",
        use_container_width=True,
    ):

        # =========================
        # SIMPAN PENANGGAP
        # =========================

        if pilihan_penanggap:

            data_penanggap = [
                {
                    "submission_id": terpilih["id"],
                    "student_id": item["student_id"],
                    "role": "respondent",
                }
                for item in pilihan_penanggap
            ]

            supabase.table("submission_members").insert(data_penanggap).execute()

        # =========================
        # TANDAI SUDAH DIPANGGIL
        # =========================

        (
            supabase.table("submissions")
            .update({"called_at": datetime.now(ZoneInfo("UTC")).isoformat()})
            .eq(
                "id",
                terpilih["id"],
            )
            .execute()
        )

        # =========================
        # BERSIHKAN STATE
        # =========================

        st.session_state.pop(
            "submission_terpilih",
            None,
        )

        st.session_state.pop(
            "penanggap_sementara",
            None,
        )

        st.session_state.pop(
            "penanggap_submission_id",
            None,
        )

        st.rerun()


if st.button(
    "🎲 RANDOM",
    type="primary",
    use_container_width=True,
):

    random_kelompok()


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

        # =========================
        # PENANGGAP
        # =========================

        penanggap = [
            member["students"]["name"]
            for member in item["submission_members"]
            if member["role"] == "respondent"
        ]

        if penanggap:
            st.write("**Penanggap:**")

            for nama in penanggap:
                st.write(f"- {nama}")

        st.write("**Jawaban:**")

        st.write(item["answer"])

        st.write(f"**Status:** {item['status']}")
