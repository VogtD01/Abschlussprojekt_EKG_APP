import streamlit as st
from streamlit_option_menu import option_menu
from seite1 import seite1
from seite2 import seite2
from seite3 import seite3   
import streamlit_functions as sf

# Anwenden des benutzerdefinierten CSS
sf.set_bg_hack()

# Sidebar-Menü erstellen
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",  # Erster Menü-Titel
        options=["Home", "Seite 2", "Seite 3"],  # Menü-Optionen
        icons=["house", "gear", "book"],  # Icons für die Menü-Optionen
        menu_icon="cast",  # Icon für das Menü
        default_index=0,  # Standardmäßig ausgewählte Option
    )

# Hauptinhalt der App
# Logik zum Anzeigen der ausgewählten Seite
if selected == "Home":
    seite1()
elif selected == "Seite 2":
    
    seite2()
elif selected == "Seite 3":
    
    seite3()
    