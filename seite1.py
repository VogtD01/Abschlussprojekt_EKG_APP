import streamlit as st
from streamlit_option_menu import option_menu

import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person


# Funktion für Seite 1

def seite1():
    st.title("Mainpage")
    st.write("Willkommen auf Seite 1!")
    # Füge hier deinen Inhalt für Seite 1 hinzu
    st.image("Bilder/test.jpg", caption="Beispielbild", width=800)

