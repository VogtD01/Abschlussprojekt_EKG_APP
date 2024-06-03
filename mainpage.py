import streamlit as st
from streamlit_option_menu import option_menu
from seite1 import seite1
from seite2 import seite2
from seite3 import seite3   

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
# Anwenden des benutzerdefinierten CSS
set_bg_hack()

# Sidebar-Menü erstellen

with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",  # Erster Menü-Titel
        options=["Seite 1", "Seite 2", "Seite 3"],  # Menü-Optionen
        icons=["house", "gear", "book"],  # Icons für die Menü-Optionen
        menu_icon="cast",  # Icon für das Menü
        default_index=0,  # Standardmäßig ausgewählte Option
    )

# Hauptinhalt der App
# Logik zum Anzeigen der ausgewählten Seite
if selected == "Seite 1":
    seite1()
elif selected == "Seite 2":
    
    seite2()
elif selected == "Seite 3":
    
    seite3()
    