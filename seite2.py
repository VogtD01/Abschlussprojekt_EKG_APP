import streamlit as st
from streamlit_option_menu import option_menu
import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person
from PIL import Image
import numpy as np
import myfunctions as mf


def seite2():
    # Zu Beginn

    # Lade alle Personen
    person_names = read_person_data.get_person_list(read_person_data.load_person_data())

    # Initialisiere Session State, Versuchperson, Bild, EKG-Test
    mf.initialize_session_state()

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


            


    #Öffne EKG-Daten
    ekgdata_dict = ekgdata.EKGdata.load_by_id(person_dict["id"])

    st.write("## EKG-Daten auswählen")
    # TODO: Für eine Person gibt es ggf. mehrere EKG-Daten. Diese müssen über den Pfad ausgewählt werden können
    ekg_list = []
    for ekg in ekgdata_dict:
        ekg_list.append(ekg["id"])

    # Auswahlbox für EKG-Daten
    st.session_state.ekg_test = st.selectbox(
        'EKG-Test',
        options = ekg_list)

    # EKG-Daten anzeigen
    current_ekg_data = ekgdata.EKGdata.load_by_id(person_dict["id"], st.session_state.ekg_test)
    current_ekg_data_class = ekgdata.EKGdata(current_ekg_data)

    st.write("## EKG-Daten")
    st.write("Datum: ", current_ekg_data["date"])

    # EKG-Daten als Matplotlib Plot anzeigen
    
    # add number input for start and end of the plot 
    start = st.number_input("Start des Plots", 0, len(current_ekg_data_class.df), 0)
    end = st.number_input("Ende des Plots", 0, len(current_ekg_data_class.df), 1000)
    

    # add peaks botton 
    peaks = False
    if st.toggle("T-Peaks anzeigen", False):
        peaks = True

    # EKG-Daten als Matplotlib Plot anzeigen
    fig = current_ekg_data_class.plot_time_series(start, end, peaks)
    st.plotly_chart(fig)

    # Herzrate bestimmen
    heartrate_array, mean_heartrate = current_ekg_data_class.estimate_heartrate()
    fig2 = current_ekg_data_class.plot_heartrate(heartrate_array)
    st.write("durchschnittliche Herzfrequenz: ", int(mean_heartrate))
    st.plotly_chart(fig2)

