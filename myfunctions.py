import streamlit as st

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