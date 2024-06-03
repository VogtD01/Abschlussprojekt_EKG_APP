import streamlit as st
from streamlit_option_menu import option_menu

import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person

# Funktion für Seite 3
def seite3():
    st.title("Seite 3")
    st.write("Willkommen auf Seite 3!")
    # Füge hier deinen Inhalt für Seite 3 hinzu