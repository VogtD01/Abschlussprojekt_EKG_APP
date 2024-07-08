
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
    
    person_names = read_person_data.get_person_list(read_person_data.load_person_data())

    # Initialisiere Session State, Versuchperson, Bild, EKG-Test
    sf.initialize_session_state()


    st.markdown("<h1 style='color: white;'>EKG APP</h1>", unsafe_allow_html=True)

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
            person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
            st.session_state.picture_path = person_dict.get("picture_path")

            if st.session_state.picture_path:
                image = Image.open(st.session_state.picture_path)
                st.image(image, caption=st.session_state.aktuelle_versuchsperson)
            else:
                st.write("Kein Bild verfügbar")

            if person_dict and 'polar_tests' in person_dict and person_dict['polar_tests']:
                polar_test_ids = [test['date'] for test in person_dict['polar_tests']]
                st.session_state.selected_polar_test = st.selectbox(
                    "Wählen Sie einen Polar-Test",
                    options=polar_test_ids,
                    key="sbPolarTest"
                )

                if st.session_state.selected_polar_test is not None:
                    polardata_dict = next(test for test in person_dict['polar_tests'] if test['date'] == st.session_state.selected_polar_test)
                    polar_data = PolarData(polardata_dict)
                    total_duration, total_distance, average_hr, total_calories = polar_data.calculate_summary_stats()

                    st.write(f"Gesamtzeit: {total_duration}")
                    st.write(f"Gesamtdistanz: {total_distance} km")
                    st.write(f"Durchschnittlicher Puls: {average_hr} bpm")
                    st.write(f"Verbrannte Kalorien: {total_calories}")
            else:
                st.write("Keine Polar-Test-Daten verfügbar.")