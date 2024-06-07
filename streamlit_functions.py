import streamlit as st

# Funktion zum Einfügen benutzerdefinierter CSS
def set_bg_hack():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #0e1117;
            color: white;
        }}
        .stApp [data-testid="stSidebar"] {{
            background-color: #1a1b1f;
        }}
        .stApp .css-1aumxhk {{
            background-color: #1a1b1f;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )