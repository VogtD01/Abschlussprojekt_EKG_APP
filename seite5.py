import streamlit as st
from streamlit_option_menu import option_menu

import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person

def seite5():
    
    # Farbe des Textes ändern
    st.markdown("<h1 style='color:White;'>Willkommen auf Seite 10</h1>", unsafe_allow_html=True)

    # Füge hier deinen Inhalt für Seite 1 hinzu
    st.image("Bilder/test.jpg", caption="Beispielbild", width=800)