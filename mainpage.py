import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_functions as sf
from seite1 import seite1
from seite2 import seite2
from seite3 import seite3
from seite4 import seite4   

# Anwenden des benutzerdefinierten CSS
sf.set_bg_hack()

# Initialisiere den Zustand des ausgewählten Menüs
if 'selected' not in st.session_state:
    st.session_state.selected = "Home"


# Sidebar-Menü erstellen
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",  # Erster Menü-Titel
        options=["Home", "EKG-Analyse", "Benutzerdaten bearbeiten"],  # Menü-Optionen
        icons=["house", "book", "gear"],  # Icons für die Menü-Optionen
        menu_icon="cast",  # Icon für das Menü
        default_index=0,  # Standardmäßig ausgewählte Option
    )
    if selected != st.session_state.selected:
        st.session_state.selected = selected



# Hauptinhalt der App
# Logik zum Anzeigen der ausgewählten Seite
if st.session_state.selected == "Home":
    seite1()
elif st.session_state.selected == "EKG-Analyse":
    seite2()
elif st.session_state.selected == "Benutzerdaten bearbeiten":
    seite3()
elif st.session_state.selected == "Polar Sportanalyse":
    seite4()
