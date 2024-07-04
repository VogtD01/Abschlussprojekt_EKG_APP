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

        try:
            st.markdown(f"**Geburtsdatum:** {person_dict['date_of_birth']}")
        except:
            pass

        try:
            st.markdown(f"**Alter:** {Person_class.calc_age()}")
        except:
            pass

        try:
            st.markdown(f"**ID:** {person_dict['id']}")
        except:
            pass

        try:
            st.markdown(f"**Maximale Herzfrequenz:** {Person_class.calc_max_heart_rate()}")
        except:
            pass

        try:
            st.markdown(f"**Geschlecht:** {person_dict['Gender']}")
        except:
            pass
        
        try:
            st.markdown(f"**Größe:** {person_dict['height']} cm")
        except:
            pass

        try:
            st.markdown(f"**Gewicht:** {person_dict['height']} kg")
        except:
            pass
            


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
        current_sample_rate = current_ekg_data_class.sample_rate    # Abtastfrequenz des aktuellen EKGs

       
        # Berechnung der maximalen Zeit in Sekunden
        max_time_seconds = current_ekg_data_class.df['New Time in ms'].iloc[-1] / 1000


        # Bestimmung der Start- und Endzeit des Plots
        start, end = sf.get_plot_time_range(max_time_seconds, current_sample_rate, 0, 10) 
        """
        Hier kann die Funktion get_plot_time_range aus streamlit_functions.py verwendet werden, um die Start- und Endzeit des Plots zu bestimmen.
        Mit der dritten und vierten Zahl in der Funktion können die Standardwerte für die Start- und Endzeit des Plots festgelegt werden."""



    # Berechnen Sie die Peaks und die Herzfrequenz als schätzende Werte
    heartrate_array, mean_heartrate, max_heartrate, min_heartrate = current_ekg_data_class.estimate_heartrate()

    # heart rate variability
    fig_heart_rate_variability, mean_heart_rate_variability, max_heart_rate_variability, min_heart_rate_variability = current_ekg_data_class.heartratevariability()

    # rt interval
    mean_RT_interval, max_RT_interval, min_RT_interval = current_ekg_data_class.RT_interval()

    #create new columns
    col1, col2 = st.columns(2)

    with col1:
        #header for the first column in white
        st.markdown("<h3 style='color: white;'>EKG-Daten für die gesamte Aktivität</h3>", unsafe_allow_html=True)
        # length of the activity
        st.write("Länge der Aktivität: ", max_time_seconds, " Sekunden")
        # mean heart rate
        st.write("Durchschnittliche Herzfrequenz: ", int(mean_heartrate), "bpm")
        # max heart rate
        st.write("Maximale Herzfrequenz: ", int(max_heartrate), "bpm")
        st.write("Minimale Herzfrequenz: ", int(min_heartrate), "bpm")

        # heart rate variability
        st.write("Durchschnittliche Herzfrequenzvariabilität: ", int(mean_heart_rate_variability), "ms")
        st.write("Maximale Herzfrequenzvariabilität: ", int(max_heart_rate_variability), "ms")
        st.write("Minimale Herzfrequenzvariabilität: ", int(min_heart_rate_variability), "ms")

        # rt interval
        st.write("Durchschnittliche Zeit RT-Intervall: ", int(mean_RT_interval), "ms")
        st.write("Maximale Zeit RT-Intervall: ", int(max_RT_interval), "ms")
        st.write("Minimale Zeit RT-Intervall: ", int(min_RT_interval), "ms")



    with col2:
        # get the heart rate for the selected time
        mean_heart_rate_1, heart_rate_array_1, max_heart_rate1, min_heart_rate1 = current_ekg_data_class.calc_heartrate_for_time(start, end)
        # header for the second column in white
        st.markdown("<h3 style='color: white;'>EKG-Daten für die eingegebene Zeit</h3>", unsafe_allow_html=True)
        st.write(".")
        # mean heart rate for the selected time
        st.write("Durchschnittliche Herzfrequenz: ", int(mean_heart_rate_1), "bpm")
        # max heart rate for the selected time
        st.write("Maximale Herzfrequenz: ", int(max_heart_rate1), "bpm")
        # min heart rate for the selected time
        st.write("Minimale Herzfrequenz: ", int(min_heart_rate1), "bpm")



    #Schalter für R_Peaks
    peaks = False
    if st.checkbox("R-Peaks anzeigen", False):
        peaks = True

    #Schaler für T_Peaks
    t_peaks = False
    if st.checkbox("T-Peaks anzeigen", False):
        t_peaks = True

    # EKG-Daten als Plot anzeigen
    fig = current_ekg_data_class.plot_time_series(start, end, peaks, t_peaks)
    st.plotly_chart(fig)

    # Herzrate bestimmen
    
    fig2 = current_ekg_data_class.plot_heartrate(heartrate_array, Person_class.calc_max_heart_rate())
    
    st.plotly_chart(fig2)

    # heart rate variability plot
    st.plotly_chart(fig_heart_rate_variability)


