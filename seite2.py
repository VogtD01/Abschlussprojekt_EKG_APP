import streamlit as st
from streamlit_option_menu import option_menu
import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person
from PIL import Image
import numpy as np
import streamlit_functions as sf


def seite2():
    # Zu Beginn

    # Lade alle Personen
    person_names = read_person_data.get_person_list(read_person_data.load_person_data())

    # Initialisiere Session State, Versuchperson, Bild, EKG-Test
    sf.initialize_session_state()

    # Schreibe die Überschrift
    st.write("# EKG APP")

    # Verwende columns, um die Elemente nebeneinander anzuzeigen
    col1, col2, col3 = st.columns([1, 1, 2])

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

    with col3:
        if st.session_state.aktuelle_versuchsperson:
            # Weitere Daten wie Geburtsdatum etc. schön anzeigen
            person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
            Person_class = person.Person(person_dict)

        # Erste Möglichkeit: Daten in einer Tabelle anzeigen
        """data = {
                "Attribut": ["Geburtsdatum", "Alter", "ID", "Maximale Herzfrequenz"],
                "Wert": [
                    person_dict["date_of_birth"], 
                    Person_class.calc_age(), 
                    person_dict["id"], 
                    Person_class.calc_max_heart_rate()
                ]
            }
        st.table(data)"""

        # Zweite Möglichkeit: Daten einzeln anzeigen, muss noch entschieden werden
        st.write("Daten von ", st.session_state.aktuelle_versuchsperson)
            
        st.markdown(f"**Geburtsdatum:** {person_dict['date_of_birth']}")
        st.markdown(f"**Alter:** {Person_class.calc_age()}")
        st.markdown(f"**ID:** {person_dict['id']}")
        st.markdown(f"**Maximale Herzfrequenz:** {Person_class.calc_max_heart_rate()}")


            


    # Öffne EKG-Daten
    ekgdata_dict = ekgdata.EKGdata.load_by_id(person_dict["id"])

    st.write("## EKG-Daten auswählen")
    # Für eine Person gibt es ggf. mehrere EKG-Daten. Diese müssen über den Pfad ausgewählt werden können
    ekg_list = []
    date_id_mapping = {}

    for ekg in ekgdata_dict:
        ekg_list.append(ekg["date"])
        date_id_mapping[ekg["date"]] = ekg["id"]

    # Erstellen Sie eine Spaltenanordnung
    col1, col2 = st.columns(2)

    with col1:
        # Auswahlbox für EKG-Daten
        st.session_state.ekg_test_date = st.selectbox(
            'EKG-Test Datum',
            options=ekg_list)

    with col2:
        selected_date = st.session_state.ekg_test_date
        selected_ekg_id = date_id_mapping[selected_date]

        current_ekg_data = ekgdata.EKGdata.load_by_id(person_dict["id"], selected_ekg_id)
        current_ekg_data_class = ekgdata.EKGdata(current_ekg_data)

       
        # Berechnung der maximalen Zeit in Sekunden
        max_time_seconds = len(current_ekg_data_class.df) / 1000

        # Fügen Sie eine Nummerneingabe für Start und Ende des Plots hinzu (in Sekunden)
        start_seconds = st.number_input("Start des Plots (in Sekunden)", 0.0, max_time_seconds, 0.0)
        end_seconds = st.number_input("Ende des Plots (in Sekunden)", 0.0, max_time_seconds, max_time_seconds)

        # Umrechnung der Eingabewerte in Millisekunden
        start = int(start_seconds * 1000)
        end = int(end_seconds * 1000)



    # Fügen Sie einen Schalter für Peaks hinzu
    peaks = False
    if st.checkbox("T-Peaks anzeigen", False):
        peaks = True

    # EKG-Daten als Matplotlib Plot anzeigen
    fig = current_ekg_data_class.plot_time_series(start, end, peaks)
    st.plotly_chart(fig)

    # Herzrate bestimmen
    heartrate_array, mean_heartrate = current_ekg_data_class.estimate_heartrate()
    fig2 = current_ekg_data_class.plot_heartrate(heartrate_array)
    st.write("durchschnittliche Herzfrequenz: ", int(mean_heartrate))
    st.plotly_chart(fig2)
