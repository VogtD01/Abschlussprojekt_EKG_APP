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

    st.title("Personendaten editieren/ergänzen")
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
    
    
    # Vorname der Person hinzufügen/ändern
    if 'firstname' not in person_dict:
        st.subheader("Vornamen hinzufügen")
        new_firstname = st.text_input("Neuer Vorname")
        if st.button("Vorname hinzufügen"):
            person_dict['firstname'] = new_firstname
            read_person_data.update_person_data(person_dict)
            st.write("Vorname wurde hinzugefügt")
    else:
        st.subheader("Voramen ändern")
        st.write("Aktueller Vorname: ", person_dict['firstname'] )
        new_firstname = st.text_input("Neuer Name")
        if st.button("Vorname ändern"):
            person_dict['firstname'] = new_firstname
            read_person_data.update_person_data(person_dict)
            st.write("Vorname wurde geändert")

    # Nachname der Person Hinzuüfgen/ändern
    if 'lastname' not in person_dict:
        st.subheader("Nachnamen hinzufügen")
        new_lastname = st.text_input("Neuer Nachname")
        if st.button("Nachname hinzufügen"):
            person_dict['lastname'] = new_lastname
            read_person_data.update_person_data(person_dict)
            st.write("Nachname wurde hinzugefügt")
    else:
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

    # Geburtsdatum der Person hinzufügen/ändern
    if 'date_of_birth' not in person_dict:
        st.subheader("Geburtsdatum hinzufügen")
        st.write("Geben Sie nur das Geburstjahr an, z.B. 1990")
        new_date_of_birth = st.text_input("Neues Geburtsdatum")
        if st.button("Geburtsdatum hinzufügen"):
            person_dict['date_of_birth'] = int(new_date_of_birth)
            read_person_data.update_person_data(person_dict)
            st.write("Geburtsdatum wurde hinzugefügt")

    else:
        st.subheader("Geburtsdatum ändern")
        st.write("Aktuelles Geburtsdatum: ", person_dict['date_of_birth'] )
        st.write("Geben Sie nur das Geburstjahr an, z.B. 1990")
        new_date_of_birth = st.text_input("Neues Geburtsdatum")
        if st.button("Geburtsdatum ändern"):
            person_dict['date_of_birth'] = int(new_date_of_birth)
            read_person_data.update_person_data(person_dict)
            st.write("Geburtsdatum wurde geändert")

    # Bild der Person ändern
    if 'picture_path' not in person_dict:
        st.subheader("Bild hinzufügen")
        image = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])
        if st.button("Bild hinzufügen"):
            #Speichern des Bildes
            path = sf.save_image(image.name, image)
            person_dict['picture_path'] = path
            read_person_data.update_person_data(person_dict)
            st.write("Bild wurde hinzugefügt")

    else:
        st.subheader("Bild ändern")
        image = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])
        if st.button("Bild ändern"):
            #Speichern des Bildes
            path = sf.save_image(image.name, image)
            person_dict['picture_path'] = path
            read_person_data.update_person_data(person_dict)
            st.write("Bild wurde geändert")

    
   
    #Körpergröße hinzufügen/ändern
    if 'height' not in person_dict:
        st.subheader("Körpergröße hinzufügen")
        new_height = st.number_input("Neue Körpergröße in cm")
        if st.button("Körpergröße hinzuüfgen"):
            person_dict['height'] = new_height
            read_person_data.update_person_data(person_dict)
            st.write("Körpergröße wurde hinzugefügt")

    else:
        st.subheader("Körpergröße ändern")
        st.write("Aktuelle Körpergröße: ", person_dict['height'], " cm")
        new_height = st.number_input("Neue Körpergröße in cm")
        if st.button("Körpergröße ändern"):
            person_dict['height'] = new_height
            read_person_data.update_person_data(person_dict)
            st.write("Körpergröße wurde geändert")

    # Körpergewicht hinzufügen/ändern
    if 'weight' not in person_dict:
        st.subheader("Körpergewicht hinzufügen")
        new_weight = st.number_input("Neues Körpergewicht in kg")
        if st.button("Körpergewicht hinzuufügen"):
            person_dict['weight'] = new_weight
            read_person_data.update_person_data(person_dict)
            st.write("Körpergewicht wurde hinzugefügt")

    else:
        st.subheader("Körpergewicht ändern")
        st.write("Aktuelles Körpergewicht: ", person_dict['weight'], " kg")
        new_weight = st.number_input("Neues Körpergewicht in kg")
        if st.button("Körpergewicht ändern"):
            person_dict['weight'] = new_weight
            read_person_data.update_person_data(person_dict)
            st.write("Körpergewicht wurde geändert")


    # Geschlecht hinzufügen/ändern
    if 'Gender' not in person_dict:
        st.subheader("Geschlecht hinzufügen")
        new_gender = option_menu("Geschlecht", ["männlich", "weiblich"])
        if st.button("Geschlecht hinzufügen"):
            person_dict['Gender'] = new_gender
            read_person_data.update_person_data(person_dict)
            st.write("Geschlecht wurde hinzugefügt")

    else:
        st.subheader("Geschlecht ändern")
        st.write("Aktuelles Geschlecht: ", person_dict['Gender'])
        new_gender = option_menu("Geschlecht", ["männlich", "weiblich"])
        if st.button("Geschlecht ändern"):
            person_dict['Gender'] = new_gender
            read_person_data.update_person_data(person_dict)
            st.write("Geschlecht wurde geändert")

    

