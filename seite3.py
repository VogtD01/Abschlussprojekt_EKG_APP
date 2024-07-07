import streamlit as st
from streamlit_option_menu import option_menu

import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person
import streamlit_functions as sf
from PIL import Image
from polardata import PolarData

# Funktion für Seite 3
def seite3():
    tab1, tab2, tab3, tab4 = st.tabs([
        "Personendaten editieren/ergänzen", "Daten hinzufügen", "Daten löschen", "Neue Person hinzufügen"])

    with tab1:
        #st.title("Personendaten editieren/ergänzen")
        st.markdown("<h1 style='color: white;'>Personendaten editieren/ergänzen</h1>", unsafe_allow_html=True)

        

        # Lade alle Personen
        person_names = read_person_data.get_person_list(read_person_data.load_person_data())
        # Initialisiere Session State, Versuchperson, Bild, EKG-Test
        sf.initialize_session_state()

        col1, col2 = st.columns([1, 2])
        with col2:
            st.write("Versuchsperson auswählen")
            st.session_state.aktuelle_versuchsperson = st.selectbox(
                'Versuchsperson', options=person_names, key="sbVersuchsperson")
        
        with col1:
            if st.session_state.aktuelle_versuchsperson:
                person_dict = read_person_data.find_person_data_by_name(
                    st.session_state.aktuelle_versuchsperson)
                st.session_state.picture_path = person_dict.get("picture_path", "")
                if st.session_state.picture_path:
                    image = Image.open(st.session_state.picture_path)
                    st.image(image, caption=st.session_state.aktuelle_versuchsperson)
                else:
                    st.write("Kein Bild verfügbar")

        
        st.markdown("<h3 style='color: white;'>Daten ändern</h3>", unsafe_allow_html=True)
        

        # Definiere die Felder
        fields = [
            ("Vorname", "firstname", "z.B. Max"),
            ("Nachname", "lastname", "z.B. Mustermann"),
            ("Geburtsdatum", "date_of_birth", "z.B. 1990"),
            ("Körpergröße (cm)", "height", "z.B. 180"),
            ("Körpergewicht (kg)", "weight", "z.B. 75"),
            ("Geschlecht", "Gender", ["männlich", "weiblich", "divers"])
        ]

        # Erstelle eine Tabelle mit den Feldern
        for field, key, placeholder in fields:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.markdown(f"**{field}**")
            with col2:
                if key in person_dict:
                    current_value = person_dict[key]
                    if key == "Gender":
                        new_value = option_menu("Geschlecht", placeholder, key=f"option_menu_{key}", styles={
                            
                        })
                    else:
                        new_value = st.text_input(f"Neuer {field}", value=current_value, placeholder=placeholder)
                else:
                    if key == "Gender":
                        new_value = option_menu("Geschlecht", placeholder, key=f"option_menu_{key}", styles={
                            
                        })
                    else:
                        new_value = st.text_input(f"Neuer {field}", placeholder=placeholder)
            with col3:
                if key in person_dict:
                    if st.button(f"ändern", key=f"btn_{key}_change"):
                        person_dict[key] = new_value
                        read_person_data.update_person_data(person_dict)
                        st.write(f"{field} wurde geändert")
                else:
                    if st.button(f"hinzufügen", key=f"btn_{key}_add"):
                        person_dict[key] = new_value
                        read_person_data.update_person_data(person_dict)
                        st.write(f"{field} wurde hinzugefügt")

        # Bild ändern
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown("**Bild**")
        with col2:
            image = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])
        with col3:
            if st.session_state.picture_path:
                if st.button("ändern", key="btn_picture_change"):
                    sf.delete_image(person_dict['picture_path'])
                    path = sf.save_image(image.name, image)
                    person_dict['picture_path'] = path
                    read_person_data.update_person_data(person_dict)
                    st.write("Bild wurde geändert")
            else:
                if st.button("hinzufügen", key="btn_picture_add"):
                    path = sf.save_image(image.name, image)
                    person_dict['picture_path'] = path
                    read_person_data.update_person_data(person_dict)
                    st.write("Bild wurde hinzugefügt")


    
    with tab2:
        #st.markdown("<h1 style='color: white; font-size: 24px;'>EKG/Polar-Daten hinzufügen</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: white;'>EKG/Polar-Daten hinzufügen</h1>", unsafe_allow_html=True)
        # Lade alle Personen
        person_names = read_person_data.get_person_list(read_person_data.load_person_data())
        
        # Initialisiere Session State, Versuchperson, Bild, EKG-Test
        sf.initialize_session_state()
        
        # Personenauswahl und Bild
        col1, col2 = st.columns([1, 2])

        with col2:
            st.write("Versuchsperson auswählen")
            st.session_state.aktuelle_versuchsperson = st.selectbox(
                'Versuchsperson',
                options=person_names, key="sbVersuchsperson2")
            
        with col1:
            if st.session_state.aktuelle_versuchsperson:
                # Finde den Pfad zur Bilddatei
                person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
                st.session_state.picture_path = person_dict.get("picture_path")
                if st.session_state.picture_path:
                    image = Image.open(st.session_state.picture_path)
                    st.image(image, caption=st.session_state.aktuelle_versuchsperson)
                else:
                    st.write("Kein Bild verfügbar")
        
        # Zwei Spalten für Upload-Felder
        col1, col2 = st.columns([1, 1])

        with col2:
            st.markdown("<h3 style='color: white; font-size: 18px;'>Polar-Test hochladen</h3>", unsafe_allow_html=True)
            polar_test = st.file_uploader("", type=["CSV"])  # Leerer String für Platzhalter
            polar_datum = st.text_input("Datum des Polar-Tests", placeholder="z.B. 23.12.2021")
            
            if st.button("Polar-Test hinzufügen"):
                path = sf.save_polar_data(polar_test, polar_test.name)
                
                # Aktuelle Personendaten aktualisieren
                person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
                
                if 'polar_tests' in person_dict:
                    # IDs der vorhandenen Polar-Tests sammeln
                    existing_polar_ids = [test['id'] for test in person_dict['polar_tests']]
                    next_polar_id = max(existing_polar_ids, default=0) + 1
                else:
                    next_polar_id = 1
                
                new_polartest = {
                    "id": next_polar_id,
                    "date": polar_datum,
                    "result_link": path
                }

                if 'polar_tests' not in person_dict:
                    person_dict['polar_tests'] = []

                person_dict['polar_tests'].append(new_polartest)
                read_person_data.update_person_data(person_dict)

                st.write("Polar-Test wurde hinzugefügt")

        with col1:
            st.markdown("<h3 style='color: white; font-size: 18px;'>EKG-Test hochladen</h3>", unsafe_allow_html=True)
            ekg_test = st.file_uploader("", type=["txt"])  # Leerer String für Platzhalter
            ekg_datum = st.text_input("Datum des EKG-Tests", placeholder="z.B. 23.12.2021")

            if st.button("EKG-Test hinzufügen"):
                path = sf.save_ekg_data(ekg_test, ekg_test.name)
                
                # EKG IDs sammeln
                all_ekg_ids = [test['id'] for person in read_person_data.load_person_data() for test in person.get('ekg_tests', [])]
                
                new_ekg_test = {
                    "id": person.Person.get_new_id(all_ekg_ids),
                    "date": ekg_datum,
                    "result_link": path
                }

                person_dict['ekg_tests'].append(new_ekg_test)
                read_person_data.update_person_data(person_dict)

                st.write("EKG-Test wurde hinzugefügt")
                    
                
    with tab3:
        st.markdown("<h1 style='color: white;'>EKG/Polar-Daten löschen</h1>", unsafe_allow_html=True)
        # Lade alle Personen
        person_names = read_person_data.get_person_list(read_person_data.load_person_data())
        # Initialisiere Session State, Versuchperson, Bild, EKG-Test
        sf.initialize_session_state()

        col1, col2 = st.columns([1, 2])

        with col2:
            st.write("Versuchsperson auswählen")
            st.session_state.aktuelle_versuchsperson = st.selectbox(
                'Versuchsperson',
                options=person_names, key="sbVersuchsperson3")
            
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

        
        
        col1, col2 = st.columns([1, 1])

        with col1:
            # Öffne EKG-Daten
            ekgdata_dict = ekgdata.EKGdata.load_by_id(person_dict["id"])

            st.markdown("<h3 style='color: white;'>EKG-Daten auswählen</h3>", unsafe_allow_html=True)
            
            # Für eine Person gibt es ggf. mehrere EKG-Daten. Diese müssen über den Pfad ausgewählt werden können
            ekg_list = []
            date_id_mapping = {}

            for ekg in ekgdata_dict:
                ekg_list.append(ekg["date"])
                date_id_mapping[ekg["date"]] = ekg["id"]

            # Auswahlbox für EKG-Daten
            st.session_state.ekg_test_date = st.selectbox(
                'EKG-Test Datum',
                options=ekg_list)

            selected_date = st.session_state.ekg_test_date
            if selected_date is not None:
                selected_ekg_id = date_id_mapping[selected_date]
                for ekg in ekgdata_dict:
                    if ekg["id"] == selected_ekg_id:
                        link = ekg["result_link"]
                        
                if st.button("EKG-Test löschen"):
                    ekgdata.EKGdata.delete_by_id(person_dict["id"], selected_ekg_id, link)
                    st.write("EKG-Test wurde gelöscht")  

        with col2:

            # Öffne Polar-Daten
            polar_dict = PolarData.load_by_id(person_dict["id"])

            st.markdown("<h3 style='color: white;'>Polar-Daten auswählen</h3>", unsafe_allow_html=True)

            # Für eine Person gibt es ggf. mehrere Polar-Daten. Diese müssen über den Pfad ausgewählt werden können
            polar_list = []
            date_id_mapping = {}

            for polar in polar_dict:
                polar_list.append(polar["date"])
                date_id_mapping[polar["date"]] = polar["id"]

            # Auswahlbox für Polar-Daten
            st.session_state.polar_test_date = st.selectbox(
                'Polar-Test Datum',
                options=polar_list)

            selected_date = st.session_state.polar_test_date
            if selected_date is not None:
                selected_polar_id = date_id_mapping[selected_date]
                for polar in polar_dict:
                    if polar["id"] == selected_polar_id:
                        link = polar["result_link"]
                
                if st.button("Polar-Test löschen"):
                    PolarData.delete_by_id(person_dict["id"], selected_polar_id, link)
                    st.write("Polar-Test wurde gelöscht")


    with tab4:
        
        st.markdown("<h1 style='color: white;'>Neue Person hinzufügen</h1>", unsafe_allow_html=True)
        st.write("Bitte geben Sie die Daten der neuen Person ein.")

        new_firstname = st.text_input("Vorname", placeholder="Max")
        new_lastname = st.text_input("Nachname", placeholder="Mustermann")
        new_date_of_birth = st.text_input("Geburtsdatum (Jahr)",placeholder="z.B. 1990")
        new_id = person.Person.get_new_id(person.Person.get_personIDs(read_person_data.load_person_data()))

        new_person = {
            "id": new_id,
            "firstname": new_firstname,
            "lastname": new_lastname,
            "date_of_birth": new_date_of_birth,
            "picture_path": None,
            "ekg_tests": []
        }

        if st.button("Person hinzufügen"):
            read_person_data.add_person(read_person_data.load_person_data(), new_person)
            st.write("Person wurde hinzugefügt")