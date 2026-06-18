import streamlit as st


def apply_custom_style() -> None:
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }

        .app-hero {
            padding: 1.5rem 1.75rem;
            border-radius: 1.25rem;
            background: linear-gradient(135deg, #eef4ff 0%, #f8fbff 100%);
            border: 1px solid #dbe7ff;
            margin-bottom: 1.5rem;
        }

        .app-hero h1 {
            margin: 0;
            font-size: 2.2rem;
        }

        .app-hero p {
            margin-top: 0.6rem;
            margin-bottom: 0;
            color: #4b5563;
            font-size: 1rem;
        }

        .section-card {
            padding: 1.25rem;
            border-radius: 1rem;
            border: 1px solid #e5e7eb;
            background-color: #ffffff;
            margin-bottom: 1rem;
        }

        .small-muted {
            color: #6b7280;
            font-size: 0.95rem;
        }

        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            padding: 1rem;
            border-radius: 1rem;
        }

        div[data-testid="stExpander"] {
            border-radius: 1rem;
            border: 1px solid #e5e7eb;
            overflow: hidden;
        }

        .stButton > button {
            border-radius: 0.7rem;
            font-weight: 600;
        }

        .danger-box {
            padding: 1rem;
            border-radius: 1rem;
            border: 1px solid #fecaca;
            background-color: #fff1f2;
            color: #991b1b;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )