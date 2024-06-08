import streamlit as st
from streamlit_option_menu import option_menu

import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person
import myfunctions as mf


def seite2():
    person_names = read_person_data.get_person_list(read_person_data.load_person_data())

    st.markdown("<h1 style='color:#ADD8E6;'>Benutzer auswählen</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:blue;'>Bitte benutzer auswählen!</p>", unsafe_allow_html=True)
    

    mf.initialize_session_state()   # Initialisieren des Session State

    # Schreibe die Überschrift
    st.write("# EKG APP")
    st.write("## Versuchsperson auswählen")
    # Erstelle zwei Spalten
    col1, col2 = st.columns([1, 2])  # Verhältnis der Spaltenbreite

    with col1:

        # Auswahlbox, wenn Personen anzulegen sind
        st.session_state.aktuelle_versuchsperson = st.selectbox(
            'Versuchsperson',
            options = person_names, key="sbVersuchsperson")

        # Name der Versuchsperson
        st.write("Der Name ist: ", st.session_state.aktuelle_versuchsperson) 

        person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
        Person_class = person.Person(person_dict)

        if st.session_state.aktuelle_versuchsperson in person_names:
            st.session_state.picture_path = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["picture_path"]
            # st.write("Der Pfad ist: ", st.session_state.picture_path) 

    with col2:
        #Bild anzeigen
        from PIL import Image
        image = Image.open(st.session_state.picture_path)
        st.image(image, caption=st.session_state.aktuelle_versuchsperson)

        #Öffne EKG-Daten
        ekgdata_dict = ekgdata.EKGdata.load_by_id(person_dict["id"])

