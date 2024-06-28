import streamlit as st
from streamlit_option_menu import option_menu

import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person
import streamlit_functions as sf
from PIL import Image

# Funktion für Seite 3
def seite3():

    st.title("Personendaten editieren")
    # Lade alle Personen
    person_names = read_person_data.get_person_list(read_person_data.load_person_data())
    # Initialisiere Session State, Versuchperson, Bild, EKG-Test
    sf.initialize_session_state()

    
    col1, col2 = st.columns([1, 2])

    with col2:
        st.write("Versuchsperson auswählen")
        st.session_state.aktuelle_versuchsperson = st.selectbox(
            'Versuchsperson',
            options=person_names, key="sbVersuchsperson")
        
    with col1:
        if st.session_state.aktuelle_versuchsperson:
            # Finde den Pfad zur Bilddatei
            person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
            st.session_state.picture_path = person_dict["picture_path"]
            if st.session_state.picture_path:
                image = Image.open(st.session_state.picture_path)
                st.image(image, caption=st.session_state.aktuelle_versuchsperson)
            else:
                st.write("Kein Bild verfügbar")
    
    
    # Vorname der Person ändern
    st.subheader("Voramen ändern")
    st.write("Aktueller Vorname: ", person_dict['firstname'] )
    new_firstname = st.text_input("Neuer Name")
    if st.button("Vorname ändern"):
        person_dict['firstname'] = new_firstname
        read_person_data.update_person_data(person_dict)
        st.write("Vorname wurde geändert")

    # Nachname der Person ändern
    st.subheader("Nachnamen ändern")
    st.write("Aktueller Nachname: ", person_dict['lastname'] )
    new_lastname = st.text_input("Neuer Nachname")
    if st.button("Nachname ändern"):
        person_dict['lastname'] = new_lastname
        read_person_data.update_person_data(person_dict)
        st.write("Nachname wurde geändert")

    # Custom CSS to ensure button text visibility
    st.markdown("""
        <style>
        .stButton button {
            color: black; /* Change the color to ensure visibility */
            font-size: 16px; /* Adjust font size as needed */
        }
        </style>
        """, unsafe_allow_html=True)

    # Geburtsdatum der Person ändern
    st.subheader("Geburtsdatum ändern")
    st.write("Aktuelles Geburtsdatum: ", person_dict['date_of_birth'] )
    st.write("Geben Sie nur das Geburstjahr an, z.B. 1990")
    new_date_of_birth = st.text_input("Neues Geburtsdatum")
    if st.button("Geburtsdatum ändern"):
        person_dict['date_of_birth'] = int(new_date_of_birth)
        read_person_data.update_person_data(person_dict)
        st.write("Geburtsdatum wurde geändert")

    # Bild der Person ändern
    st.subheader("Bild ändern")


