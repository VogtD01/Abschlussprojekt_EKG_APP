
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

    col1, col2 = st.columns([1, 1])

    with col2:
        st.session_state.aktuelle_versuchsperson = st.selectbox(
            "Wählen Sie eine Versuchsperson",
            options=person_names,
            key="sbVersuchsperson"
        )
    
        if st.session_state.aktuelle_versuchsperson:
            person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)

            if person_dict and 'polar_tests' in person_dict and person_dict['polar_tests']:
                polar_test_ids = [test['date'] for test in person_dict['polar_tests']]
                st.session_state.selected_polar_test = st.selectbox(
                    "Wählen Sie einen Polar-Test",
                    options=polar_test_ids,
                    key="sbPolarTest"
                )

    with col1:
        if st.session_state.aktuelle_versuchsperson:
            person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
            st.session_state.picture_path = person_dict.get("picture_path")

            if st.session_state.picture_path:
                image = Image.open(st.session_state.picture_path)
                st.image(image, caption=st.session_state.aktuelle_versuchsperson, use_column_width=True)
            else:
                st.write("Kein Bild verfügbar")

    if st.session_state.selected_polar_test:
        polardata_dict = next(test for test in person_dict['polar_tests'] if test['date'] == st.session_state.selected_polar_test)
        polar_data = PolarData(polardata_dict)
        total_duration, total_distance, average_hr, total_calories = polar_data.calculate_summary_stats()

        # Horizontale Anordnung der Statistikwerte in weißer Schrift
        st.markdown("<h3 style='color: white;'>Zusammenfassung der Testdaten:</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(" ", total_duration, "Zeit")
        col2.metric(" ", f"{total_distance} km", "Distanz")
        col3.metric(" ", f"{average_hr} bpm", "Herzfrequenz")
        col4.metric(" ", f"{total_calories} kcal", "Kalorien")

    # Tabs für Bilder und Plot
    tab1, tab2, tab3, tap4, tap5, = st.tabs(["Gesamtübersicht", "Hertzfrequenz", "Bild 3", "Bild 4", "Bild 5"])

    with tab1:
        if st.session_state.selected_polar_test:
            current_df_data = polar_data.df_data
            fig1 = polar_data.plot_polar_curves_together(current_df_data)
            st.plotly_chart(fig1)
        else:
            st.write("Keine Polar-Test-Daten verfügbar.")

    with tab2:
        if st.session_state.selected_polar_test:
            current_df_data = polar_data.df_data
            person_id = person_dict['id']
            maxHR = PolarData.load_max_hr_individual_by_id(person_id)
            zones_thresholds = PolarData.load_heart_rate_zones_by_id(person_id)

            fig2 = PolarData.plot_heart_rate_with_zones(current_df_data, 1, maxHR, zones_thresholds)
            st.plotly_chart(fig2)

    with tab3:
        if st.session_state.selected_polar_test:
            current_df_data = polar_data.df_data
            fig_heartrate, fig_altitude, fig_speed, fig_power = polar_data.plot_polar_curves(current_df_data)
            st.plotly_chart(fig_speed)

    with tab4:
        if st.session_state.selected_polar_test:
            current_df_data = polar_data.df_data
            fig_heartrate, fig_altitude, fig_speed, fig_power = polar_data.plot_polar_curves(current_df_data)
            st.plotly_chart(fig_altitude)
    with tab5:
        if st.session_state.selected_polar_test:
            current_df_data = polar_data.df_data
            fig_heartrate, fig_altitude, fig_speed, fig_power = polar_data.plot_polar_curves(current_df_data)
            st.plotly_chart(fig_power)