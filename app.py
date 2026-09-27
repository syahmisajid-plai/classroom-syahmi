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
# CONTENT
# =========================

st.title("🎓 Classroom App")

st.write("Aplikasi aktivitas kelompok di kelas.")
