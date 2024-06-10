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


# Funktion zum Initialisieren des Session State

def initialize_session_state(): # Funktion zum Initialisieren des Session State
    # Anlegen des Session State. Aktuelle Versuchsperson, wenn es keine gibt
    if 'aktuelle_versuchsperson' not in st.session_state:
        st.session_state.aktuelle_versuchsperson = 'None'

    # Anlegen des Session State. Bild, wenn es kein Bild gibt
    if 'picture_path' not in st.session_state:
        st.session_state.picture_path = 'data/pictures/none.jpg'

    # Anlegen des Session State. EKG-Test, wenn es kein EKG-Test gibt
    if 'ekg_test' not in st.session_state:
        st.session_state.ekg_test = None

# Aufruf der Funktion, um den Session State zu initialisieren
initialize_session_state()   