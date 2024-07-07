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
    st.markdown("<h1 style='color: white;'>EKG APP</h1>", unsafe_allow_html=True)

    # Verwende columns, um die Elemente nebeneinander anzuzeigen
    col1, col2, col3 = st.columns([1, 1, 2])

    with col2:
        #st.markdown("<h4 style='color: white;'>Versuchsperson auswählen</h4>", unsafe_allow_html=True)
        st.session_state.aktuelle_versuchsperson = st.selectbox(
            " ",
            options=person_names,
            key="sbVersuchsperson"
            )


        

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

            # Daten der Versuchsperson anzeigen
            #st.markdown(f"<h3 style='color: white;'>Daten von {st.session_state.aktuelle_versuchsperson}</h3>", unsafe_allow_html=True)

            try:
                st.markdown(f"**Geburtsdatum:** {person_dict['date_of_birth']}")
            except:
                pass

            try:
                st.markdown(f"**Alter:** {Person_class.calc_age()}")
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
                st.markdown(f"**Gewicht:** {person_dict['weight']} kg")
            except:
                pass

            try:
                st.write('BMI: ' + str(round(person_dict['weight'] / ((person_dict['height'] / 100) ** 2), 1)))
            except:
                pass

    # Öffne EKG-Daten
    ekgdata_dict = ekgdata.EKGdata.load_by_id(person_dict["id"])

    st.markdown("<h2 style='color: white;'>EKG-Daten auswählen</h2>", unsafe_allow_html=True)
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
    
    try:
        with col2:
            selected_date = st.session_state.ekg_test_date
            selected_ekg_id = date_id_mapping[selected_date]

            current_ekg_data = ekgdata.EKGdata.load_by_id(person_dict["id"], selected_ekg_id)
            current_ekg_data_class = ekgdata.EKGdata(current_ekg_data)
            current_sample_rate = current_ekg_data_class.sample_rate  # Abtastfrequenz des aktuellen EKGs

            # Berechnung der maximalen Zeit in Sekunden
            max_time_seconds = current_ekg_data_class.df['New Time in ms'].iloc[-1] / 1000

            # Bestimmung der Start- und Endzeit des Plots
            start, end = sf.get_plot_time_range(max_time_seconds, current_sample_rate, 0, 10) 
            # Hier kann die Funktion get_plot_time_range aus streamlit_functions.py verwendet werden, um die Start- und Endzeit des Plots zu bestimmen.
            # Mit der dritten und vierten Zahl in der Funktion können die Standardwerte für die Start- und Endzeit des Plots festgelegt werden.

        # Berechnen Sie die Peaks und die Herzfrequenz als schätzende Werte
        heartrate_array, mean_heartrate, max_heartrate, min_heartrate = current_ekg_data_class.estimate_heartrate()

        # Heart rate variability
        fig_heart_rate_variability, mean_heart_rate_variability, max_heart_rate_variability, min_heart_rate_variability = current_ekg_data_class.heartratevariability()

        # RT interval
        fig_rt_intervall, mean_RT_interval, max_RT_interval, min_RT_interval = current_ekg_data_class.RT_interval()

        # Verwendung von Tabs zur Anzeige der verschiedenen Daten
        tab1, tab2, tab3 = st.tabs(["EKG-Daten", "Herzfrequenzvariabilität", "RT-Intervall"])

        with tab1:
            # Erstellen von zwei Spalten
            col1, col2 = st.columns(2)

            with col1:
                 # Header für die erste Tab
                st.markdown("<h4 style='color: white;'>EKG-Daten für die gesamte Aktivität</h4>", unsafe_allow_html=True)
                # Länge der Aktivität
                st.write("Länge der Aktivität: ", max_time_seconds, " Sekunden")
                # Durchschnittliche Herzfrequenz
                st.write("Durchschnittliche Herzfrequenz: ", int(mean_heartrate), " bpm")
                # Maximale Herzfrequenz
                st.write("Maximale Herzfrequenz: ", int(max_heartrate), " bpm")
                # Minimale Herzfrequenz
                st.write("Minimale Herzfrequenz: ", int(min_heartrate), " bpm")
            
            with col2:
                # Get the heart rate for the selected time
                mean_heart_rate_1, heart_rate_array_1, max_heart_rate1, min_heart_rate1 = current_ekg_data_class.calc_heartrate_for_time(start, end)
                # Header für die zweite Spalte
                st.markdown("<h4 style='color: white;'>EKG-Daten für die eingegebene Zeit</h4>", unsafe_allow_html=True)

                # Umrechnung der Differenz zwischen Start und Ende in Sekunden
                duration_milliseconds = end - start
                duration_seconds = float(duration_milliseconds) / 1000 / current_sample_rate

                st.write("Länge Intervall: ", duration_seconds, " Sekunden ")  
                # Durchschnittliche Herzfrequenz für die ausgewählte Zeit
                st.write("Durchschnittliche Herzfrequenz: ", int(mean_heart_rate_1), " bpm")
                # Maximale Herzfrequenz für die ausgewählte Zeit
                st.write("Maximale Herzfrequenz: ", int(max_heart_rate1), " bpm")
                # Minimale Herzfrequenz für die ausgewählte Zeit
                st.write("Minimale Herzfrequenz: ", int(min_heart_rate1), " bpm")

    
        
            
            # Schalter für R_Peaks
            peaks = False
            if st.checkbox("R-Peaks anzeigen", False):
                peaks = True

            # Schalter für T_Peaks
            t_peaks = False
            if st.checkbox("T-Peaks anzeigen", False):
                t_peaks = True

            # EKG-Daten als Plot anzeigen
            fig = current_ekg_data_class.plot_time_series(start, end, peaks, t_peaks)
            st.plotly_chart(fig)

            # Selectbox für X-Achsenformat
            x_axis_format = st.selectbox("X-Achsenformat", ["Sekunden", "Minuten"])

            
            # Herzrate bestimmen und als Plot anzeigen
            fig2 = current_ekg_data_class.plot_heartrate(heartrate_array, Person_class.calc_max_heart_rate(), x_axis_format, min_heartrate) ###ßßß
            st.plotly_chart(fig2)


            # EKG-Informationen anzeigen
            if "show_ekg_info" not in st.session_state:
                st.session_state.show_ekg_info = False

            if st.button("EKG Info"):
                st.session_state.show_ekg_info = not st.session_state.show_ekg_info

            if st.session_state.show_ekg_info:
                st.write("""
                    **Was ist ein EKG?**

                    Ein Elektrokardiogramm (EKG) ist eine Aufzeichnung der elektrischen Aktivität des Herzens über einen bestimmten Zeitraum. Es zeigt die Abfolge von Depolarisationen und Repolarisationen, die die Kontraktionen und Entspannungen der Herzmuskulatur steuern.

                    **Bedeutung der berechneten Werte im EKG**

                    - **Herzfrequenz (bpm)**: Misst die Anzahl der Herzschläge pro Minute. Eine normale Ruheherzfrequenz liegt bei Erwachsenen zwischen 60 und 100 bpm. Abweichungen können auf verschiedene kardiovaskuläre Zustände hinweisen.
                    - **R-Peaks**: Die R-Zacke repräsentiert den Beginn der Ventrikeldepolarisation. Die Identifikation der R-Peaks ist wichtig zur Berechnung der Herzfrequenz und zur Erkennung von Arrhythmien.
                    - **T-Peaks**: Der T-Punkt markiert die Repolarisation der Ventrikel. Veränderungen in der T-Welle können Hinweise auf Herzerkrankungen wie Ischämie oder Elektrolytstörungen geben.
                    - **RT-Intervall**: Das RT-Intervall misst die Zeit zwischen der R-Zacke und dem T-Punkt. Es gibt Aufschluss über die Dauer der ventrikulären Aktivität und kann auf Herzrhythmusstörungen hinweisen.

                    Das EKG ist ein unverzichtbares diagnostisches Werkzeug zur Bewertung der Herzgesundheit. Es hilft, Herzrhythmusstörungen, strukturelle Herzerkrankungen und die Auswirkungen von Medikamenten zu überwachen.
                """)

        with tab2:
            # Header für die zweite Tab
            st.markdown("<h3 style='color: white;'>Herzfrequenzvariabilität</h3>", unsafe_allow_html=True)
            st.write("Durchschnittliche Herzfrequenzvariabilität: ", int(mean_heart_rate_variability), " ms")
            st.write("Maximale Herzfrequenzvariabilität: ", int(max_heart_rate_variability), " ms")
            st.write("Minimale Herzfrequenzvariabilität: ", int(min_heart_rate_variability), " ms")
            st.plotly_chart(fig_heart_rate_variability)

            
            if "show_info" not in st.session_state:
                st.session_state.show_info = False

            if st.button("Informationen anzeigen"):
                st.session_state.show_info = not st.session_state.show_info

            if st.session_state.show_info:
                 st.write("""
                    **Was ist die Herzfrequenzvariabilität (HRV)?**

                    Die Herzfrequenzvariabilität (HRV) beschreibt die Schwankungen in den Zeitabständen zwischen aufeinanderfolgenden Herzschlägen. Sie reflektiert die Funktion des autonomen Nervensystems und die Balance zwischen Sympathikus und Parasympathikus.

                    **Warum ist die HRV wichtig?**
                    
                    - **Indikator für die Herzgesundheit**: Eine höhere HRV zeigt eine gute Herzgesundheit und Anpassungsfähigkeit an. Eine niedrige HRV kann auf Stress oder gesundheitliche Probleme hinweisen.
                    - **Stressbewältigung und Erholung**: Eine höhere HRV signalisiert effektive Stressbewältigung und schnelle Erholung nach Belastungen.
                    - **Autonome Regulation**: Die HRV bewertet das Gleichgewicht zwischen Sympathikus und Parasympathikus und kann auf Dysfunktionen hinweisen.

                    **Bedeutung der HRV für Sportler**
                    
                    - **Trainingssteuerung**: Sportler können ihr Training optimieren, indem sie die HRV zur Anpassung der Intensität und Erholung nutzen.
                    - **Vermeidung von Übertraining**: Eine kontinuierliche Überwachung der HRV hilft, Übertraining zu erkennen und zu vermeiden.
                    - **Stressmanagement**: Regelmäßige HRV-Messungen unterstützen das Stressmanagement und fördern das allgemeine Wohlbefinden.
                    - **Anpassung der Lebensweise**: Durch eine ausgewogene Ernährung, ausreichend Schlaf und gesunde Lebensgewohnheiten kann die HRV und somit die sportliche Leistung verbessert werden.
                """)

        with tab3:
            # Header für die dritte Tab
            st.markdown("<h3 style='color: white;'>RT-Intervall</h3>", unsafe_allow_html=True)
            st.write("Durchschnittliche Zeit RT-Intervall: ", int(mean_RT_interval), " ms")
            st.write("Maximale Zeit RT-Intervall: ", int(max_RT_interval), " ms")
            st.write("Minimale Zeit RT-Intervall: ", int(min_RT_interval), " ms")
            st.plotly_chart(fig_rt_intervall)

            if "show_rt_info" not in st.session_state:
                st.session_state.show_rt_info = False

            if st.button("RT-Intervall Info"):
                st.session_state.show_rt_info = not st.session_state.show_rt_info

            if st.session_state.show_rt_info:
                st.write("""
                    **Was ist das RT-Intervall?**

                    Das RT-Intervall misst die Zeitspanne zwischen der R-Zacke und dem T-Punkt im Elektrokardiogramm (EKG). Es gibt Auskunft über die Dauer der ventrikulären Depolarisation und die anschließende Repolarisation.

                    **Bedeutung des RT-Intervalls in der Medizin**

                    - **Herzrhythmusstörungen**: Veränderungen im RT-Intervall können auf verschiedene Arten von Arrhythmien hinweisen. Eine signifikante Verlängerung oder Verkürzung kann problematisch sein.
                    - **Herzerkrankungen**: Anomalien im RT-Intervall können Hinweise auf strukturelle oder funktionelle Herzerkrankungen geben, wie z.B. eine ventrikuläre Hypertrophie oder Ischämie.
                    - **Medikamentenüberwachung**: Bestimmte Medikamente können das RT-Intervall beeinflussen. Eine kontinuierliche Überwachung hilft, das Risiko von arzneimittelinduzierten Herzrhythmusstörungen zu minimieren.
                    - **Elektrolytstörungen**: Elektrolytstörungen wie Hypokaliämie oder Hyperkalzämie können zu Veränderungen des RT-Intervalls führen und müssen daher sorgfältig überwacht werden.

                    Das RT-Intervall bietet wertvolle diagnostische Informationen zur Beurteilung der Herzgesundheit und der Wirkung von Behandlungen. Eine regelmäßige Analyse kann helfen, potenzielle Herzprobleme frühzeitig zu erkennen und zu behandeln.
                """)



    except:
        pass



