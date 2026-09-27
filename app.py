import streamlit as st

from utils.style import load_style

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Classroom App",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# STYLE
# =========================

load_style()

# =========================
# HERO
# =========================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🎓 Classroom App</div>
        <div class="hero-subtitle">
            Ruang sederhana untuk mengirim jawaban kelompok
            dan mengikuti aktivitas pembelajaran di kelas.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================
# WELCOME
# =========================

st.markdown("## Selamat Datang 👋")

st.write(
    "Gunakan Classroom App untuk mengirim hasil diskusi kelompok "
    "selama kegiatan pembelajaran berlangsung."
)

# =========================
# FEATURES
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        ### 📝 Kirim Jawaban
        Pilih mata kuliah, pertemuan, anggota kelompok,
        dan kirim jawaban hasil diskusi.
        """)

with col2:
    st.markdown("""
        ### 👥 Aktivitas Kelompok
        Catat anggota kelompok yang terlibat
        dalam setiap aktivitas pembelajaran.
        """)

with col3:
    st.markdown("""
        ### 🎲 Random Kelompok
        Dosen dapat memilih kelompok secara acak
        untuk mempresentasikan hasil diskusi.
        """)

# =========================
# ACTION
# =========================

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button(
        "📝 Kirim Jawaban",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/1_Kirim_Jawaban.py")
