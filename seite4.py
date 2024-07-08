
import streamlit as st
from streamlit_option_menu import option_menu
import read_person_data
import ekgdata
import polardata
import matplotlib.pyplot as plt
import person
import streamlit_functions as sf
from PIL import Image
from polardata import PolarData
import pandas as pd
import os

def seite4():
    
    # Lade alle Personen
    person_names = read_person_data.get_person_list(read_person_data.load_person_data())

    # Initialisiere Session State, Versuchperson, Bild, EKG-Test
    sf.initialize_session_state()

    # Schreibe die Überschrift
    st.markdown("<h1 style='color: white;'>EKG APP</h1>", unsafe_allow_html=True)

    # Verwende columns, um die Elemente nebeneinander anzuzeigen
    col1, col2, col3 = st.columns([1, 0.5, 1])

    with col3:
        st.session_state.aktuelle_versuchsperson = st.selectbox(
            " ",
            options=person_names,
            key="sbVersuchsperson"
            )

    with col2:
        pass
        

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

    # Öffne Polar-Daten für die ausgewählte Person
    polardata_dict = PolarData.load_by_id(person_dict["id"])

    st.markdown("<h2 style='color: white;'>Polar-Daten auswählen</h2>", unsafe_allow_html=True)
    
    # Für eine Person gibt es ggf. mehrere Daten. Diese müssen über den Pfad ausgewählt werden können
    polar_list = []
    date_id_mapping = {}

    for polar in polardata_dict:
        polar_list.append(polar["date"])
        date_id_mapping[polar["date"]] = polar["id"]

    # Erstellen Sie eine Spaltenanordnung
    col1, col2 = st.columns(2)

    with col1:
        # Auswahlbox für Polar-Daten
        st.session_state.polar_test_date = st.selectbox(
            'Polar-Test Datum',
            options=polar_list)

    try:
        with col2:
            selected_date = st.session_state.polar_test_date
            selected_polar_id = date_id_mapping[selected_date]

            current_polar_data = PolarData.load_by_id(person_dict["id"], selected_polar_id)
            # Erstellen Sie eine Instanz der PolarData-Klasse für das ausgewählte Polar-Test-Datum
            current_polar_data_instance = PolarData(current_polar_data)

            # Berechnung der Zusammenfassungsstatistiken
            total_duration, total_distance, average_hr, total_calories = current_polar_data_instance.calculate_summary_stats()

        # Anzeigen der berechneten Statistiken
        tab1, tab2 = st.columns(2)

        with tab1:
            st.markdown("<h4 style='color: white;'>Zusammenfassungsstatistiken für Polar-Daten</h4>", unsafe_allow_html=True)
            st.write(f"Gesamtzeit: {total_duration}")
            st.write(f"Gesamtdistanz: {total_distance} km")
            st.write(f"Durchschnittlicher Puls: {average_hr} bpm")
            st.write(f"Verbrannte Kalorien: {total_calories}")

    except KeyError:
        st.warning("Wählen Sie ein gültiges Datum aus der Liste aus.")
    except Exception as e:
        st.error(f"Fehler beim Laden und Berechnen der Polar-Daten: {e}")

    