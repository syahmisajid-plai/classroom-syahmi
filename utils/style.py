import streamlit as st


def load_style():

    st.markdown(
        """
        <style>

        /* =========================
           GLOBAL
        ========================= */

        .stApp {
            background-color: #f5f7fb;
        }

        .main {
            padding-top: 2rem;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }


        /* =========================
           SIDEBAR
        ========================= */

        [data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #1f2937;
        }

        [data-testid="stSidebar"] * {
            color: #e5e7eb;
        }


        /* =========================
           HERO
        ========================= */

        .hero {
            background: linear-gradient(
                135deg,
                #111827 0%,
                #1e3a8a 100%
            );

            padding: 2.5rem;
            border-radius: 24px;
            margin-bottom: 2rem;

            box-shadow:
                0 10px 30px rgba(15, 23, 42, 0.12);
        }

        .hero-title {
            color: white;
            font-size: 2.3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 1.05rem;
            line-height: 1.6;
        }


        /* =========================
           CARD
        ========================= */

        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 18px;
            border: 1px solid #e5e7eb;

            box-shadow:
                0 4px 15px rgba(15, 23, 42, 0.05);

            height: 100%;
        }


        /* =========================
           BUTTON
        ========================= */

        .stButton > button {
            border-radius: 10px;
            border: 1px solid #d1d5db;
            font-weight: 600;
        }


        /* =========================
           INPUT
        ========================= */

        .stTextInput input,
        .stTextArea textarea {
            border-radius: 10px;
        }

        div[data-baseweb="select"] > div {
            border-radius: 10px;
        }


        /* =========================
           METRIC
        ========================= */

        [data-testid="stMetric"] {
            background: white;
            padding: 1.2rem;
            border-radius: 16px;
            border: 1px solid #e5e7eb;

            box-shadow:
                0 4px 15px rgba(15, 23, 42, 0.04);
        }

        .random-result-card {
            background: linear-gradient(135deg, #111827 0%, #1e3a8a 100%);
            padding: 28px 24px;
            border-radius: 20px;
            text-align: center;
            margin: 10px 0 22px 0;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
        }

        .random-result-label {
            color: #cbd5e1;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 1px;
        }

        .random-result-number {
            color: white;
            font-size: 38px;
            font-weight: 800;
            line-height: 1.15;
        }

        .random-result-subtitle {
            color: #bfdbfe;
            font-size: 14px;
            margin-top: 10px;
        }


        /* =========================
           MOBILE
        ========================= */

        @media (max-width: 768px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero {
                padding: 1.8rem;
                border-radius: 18px;
            }

            .hero-title {
                font-size: 1.8rem;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )
