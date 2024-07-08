import streamlit as st
from streamlit_option_menu import option_menu

import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person
import streamlit_functions as sf
from PIL import Image
from polardata import PolarData
import pandas as pd
import os


# Funktion für Seite 3
def seite3():
    tab1, tab2, tab3, tab4 = st.tabs([
        "Personendaten editieren/ergänzen", "Daten hinzufügen", "Daten löschen", "Neue Person hinzufügen"])


    with tab1:
        st.markdown("<h1 style='color: white;'>Personendaten editieren/ergänzen</h1>", unsafe_allow_html=True)

        # Lade alle Personen
        person_names = read_person_data.get_person_list(read_person_data.load_person_data())
        # Initialisiere Session State, Versuchperson, Bild, EKG-Test
        sf.initialize_session_state()

        col1, col2 = st.columns([1, 2])
        with col2:
            st.write("Versuchsperson auswählen")
            selected_person = st.selectbox('Versuchsperson', options=person_names, key="sbVersuchsperson")
            st.session_state.aktuelle_versuchsperson = selected_person

        if selected_person:
            person_dict = read_person_data.find_person_data_by_name(selected_person)
            st.session_state.picture_path = person_dict.get("picture_path", "")

        with col1:
            if st.session_state.picture_path:
                image = Image.open(st.session_state.picture_path)
                st.image(image, caption=selected_person)
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
                current_value = person_dict.get(key, "")
                if key == "Gender":
                    try:
                        new_value = st.selectbox(f"Neuer {field}", options=placeholder, index=placeholder.index(current_value) if current_value in placeholder else 0)
                    except ValueError:
                        st.warning(f"Der gespeicherte Wert '{current_value}' für {field} ist nicht in der Liste der gültigen Optionen.")
                        new_value = st.selectbox(f"Neuer {field}", options=placeholder)
                else:
                    new_value = st.text_input(f"Neuer {field}", value=current_value, placeholder=placeholder)
            with col3:
                if st.button(f"ändern", key=f"btn_{key}_change"):
                    person_dict[key] = new_value
                    read_person_data.update_person_data(person_dict)
                    st.write(f"{field} wurde geändert")

        # Bild ändern
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown("**Bild**")
        with col2:
            image = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])
        with col3:
            if st.button("ändern", key="btn_picture_change"):
                if "picture_path" in person_dict:
                    sf.delete_image(person_dict['picture_path'])
                if image is not None:
                    path = sf.save_image(image.name, image)
                    person_dict['picture_path'] = path
                    read_person_data.update_person_data(person_dict)
                    st.write("Bild wurde geändert")


        ##################################################

        # Herzfrequenzzonen hinzufügen
        st.markdown("<h3 style='color: white;'>Herzfrequenzzonen ändern</h3>", unsafe_allow_html=True)

        # Initialisiere maximale Herzfrequenz
        max_hr = st.number_input("Maximale Herzfrequenz (bpm)", value=float(person_dict.get("max_hr_individual", 200)), step=1.0)

        # Definiere Standardzonen als Prozentsätze
        default_zones = {
            "zone_1": (0.50, 0.60),
            "zone_2": (0.60, 0.70),
            "zone_3": (0.70, 0.80),
            "zone_4": (0.80, 0.90),
            "zone_5": (0.90, 1.00)
        }

        # Überprüfen, ob ein Benutzerwechsel stattgefunden hat und entsprechend die Zonen zurücksetzen
        if "last_selected_user" not in st.session_state:
            st.session_state.last_selected_user = None

        # Benutzerwechsel erkennen
        if st.session_state.last_selected_user != st.session_state.aktuelle_versuchsperson:
            st.session_state.last_selected_user = st.session_state.aktuelle_versuchsperson
            # Zonen auf Standardwerte setzen, wenn der Benutzer keine individuellen Zonen hat
            if "heart_rate_zones" not in person_dict or not person_dict["heart_rate_zones"]:
                person_dict["heart_rate_zones"] = default_zones

        # Hole die gespeicherten Zonen oder setze die Standardwerte
        person_zones = person_dict.get("heart_rate_zones", default_zones)

        # Berechne die bpm-Werte für die Zonen
        zone_bpm_values = {}
        for zone, (default_min, default_max) in default_zones.items():
            if zone in person_zones:
                min_bpm = person_zones[zone][0] * max_hr
                max_bpm = person_zones[zone][1] * max_hr
            else:
                min_bpm = default_min * max_hr
                max_bpm = default_max * max_hr
            zone_bpm_values[zone] = (min_bpm, max_bpm)

        # Eingabefelder für die Zonen
        col1, col2 = st.columns(2)
        previous_max_bpm = 0
        for i, (zone, (min_bpm, max_bpm)) in enumerate(zone_bpm_values.items()):
            if i > 0:
                min_bpm = previous_max_bpm  # Das Ende der vorherigen Zone ist der Anfang der aktuellen Zone
            
            with col1:
                st.markdown(f"**{zone.replace('_', ' ').title()} Min (bpm)**")
                min_bpm = st.number_input(f"{zone}_min", value=float(min_bpm), step=1.0, key=f"{zone}_min_input", format="%.0f")
            with col2:
                st.markdown(f"**{zone.replace('_', ' ').title()} Max (bpm)**")
                max_bpm = st.number_input(f"{zone}_max", value=float(max_bpm), step=1.0, key=f"{zone}_max_input", format="%.0f")
            
            zone_bpm_values[zone] = (min_bpm, max_bpm)
            previous_max_bpm = max_bpm

        # Speichern und Zurücksetzen der Zonen
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("Speichern"):
                # Speichern der maximalen Herzfrequenz
                person_dict["max_hr_individual"] = max_hr
                
                # Umwandeln der bpm-Werte in Prozent der maxHR
                person_zones_percent = {zone: (min_bpm / max_hr, max_bpm / max_hr) for zone, (min_bpm, max_bpm) in zone_bpm_values.items()}
                person_dict["heart_rate_zones"] = person_zones_percent
                read_person_data.update_person_data(person_dict)
                st.write("Herzfrequenzzonen wurden gespeichert")

        with col2:
            if st.button("Zonen zurücksetzen"):
                # Löschen der Herzfrequenzzonen
                person_dict.pop("heart_rate_zones", None)
                # Löschen der maximalen Herzfrequenz
                person_dict.pop("max_hr_individual", None)
                read_person_data.update_person_data(person_dict)
                st.write("Herzfrequenzzonen wurden zurückgesetzt")
                st.write("bitte nochmal drücken, um die Änderungen zu übernehmen")

        with col3:
            # Info-Box
            if "show_zone_info" not in st.session_state:
                st.session_state.show_zone_info = False

            if st.button("Info zu individuellen Herzfrequenz-Zonen"):
                st.session_state.show_zone_info = not st.session_state.show_zone_info

        if st.session_state.show_zone_info:
            st.write("""
                **Nutzen von individuellen Herzfrequenz-Zonen**

                *Ihre individuellen Herzfrequenz-Zonen sind maßgeschneidert auf Ihre persönlichen Fähigkeiten und Trainingsziele. Diese Zonen spiegeln Ihren Fitness-Level und Ihre aktuelle körperliche Leistungsfähigkeit wider und helfen Ihnen, Ihr Training besser zu steuern und zu optimieren.

                **Warum sind individuelle Zonen wichtig?**

                Individuelle Zonen sind wichtig, da jeder Athlet einzigartige physiologische Merkmale aufweist, die seine individuellen Trainingsbereiche beeinflussen. Durch die Angabe Ihrer persönlichen Zonen können Sie sicherstellen, dass das Training auf Ihre spezifischen Bedürfnisse und Ziele zugeschnitten ist.

                **Was bringt es Ihnen?**

                * Verbesserung der Trainingsgenauigkeit: Individuelle Zonen helfen Ihnen, Ihre Intensität während des Trainings besser zu kontrollieren und die Effektivität Ihrer Trainingssitzungen zu maximieren.
                * Vermeidung von Übertraining: Individuelle Zonen können Sie dabei unterstützen, sich nicht zu sehr anzustrengen und Ihren Körper Schaden zuzufügen.
                * Anpassung an Ihre Trainingsziele: Individuelle Zonen ermöglichen es Ihnen, Ihr Training besser auf spezifische Ziele wie Ausdauer, Kraft oder Fettverbrennung auszurichten.

                **Wie können Sie Ihre persönlichen Zonen festlegen?**

                Um Ihre persönlichen Zonen zu bestimmen, müssen Sie Ihre maximalen und minimalen Herzfrequenzen sowie Ihre aerobe und anaerobe Schwelle kennen. Diese Werte können mit Hilfe von Leistungstests oder durch Arbeit mit einem Trainingsprofi ermittelt werden.
            """)

    ###########################################################################
    """with tab2:
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

                st.write("Polar-Test wurde hinzugefügt")"""


    with tab2:
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
                if polar_test is not None:
                    # Speichern der hochgeladenen Datei als temporäre Datei
                    temp_polar_path = os.path.join('temp', polar_test.name)
                    with open(temp_polar_path, "wb") as f:
                        f.write(polar_test.getbuffer())
                    
                    # Aufruf der Funktion zum Speichern der Polar-Daten
                    summary_path, data_path = sf.save_polar_data(temp_polar_path, polar_test.name)
                    
                    # Löschen der temporären Datei
                    os.remove(temp_polar_path)
                    
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
                        "summary_link": summary_path,
                        "data_link": data_path
                    }

                    if 'polar_tests' not in person_dict:
                        person_dict['polar_tests'] = []

                    person_dict['polar_tests'].append(new_polartest)
                    read_person_data.update_person_data(person_dict)

                    st.write("Polar-Test wurde hinzugefügt")
                else:
                    st.write("Bitte laden Sie eine CSV-Datei hoch.")

   


#######################################################################
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
                        link_summary = polar["summary_link"]
                        link_data = polar["data_link"]
                

                if st.button("Polar-Test löschen"):
                    PolarData.delete_by_id(person_dict["id"], selected_polar_id, link_summary, link_data)
                    
                    st.write("Polar-Test wurde gelöscht")


                """if st.button("Polar-Test löschen"):
                    PolarData.delete_by_id(person_dict["id"], selected_polar_id, link_data)

                    st.write("Polar-Test wurde gelöscht")"""


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