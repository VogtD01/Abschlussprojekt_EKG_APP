import streamlit as st
from streamlit_option_menu import option_menu
import read_person_data
import ekgdata
import matplotlib.pyplot as plt
import person
from PIL import Image



def seite2():
    # Zu Beginn

    # Lade alle Personen
    person_names = read_person_data.get_person_list(read_person_data.load_person_data())

    # Anlegen diverser Session States
    ## Gewählte Versuchsperson
    if 'aktuelle_versuchsperson' not in st.session_state:
        st.session_state.aktuelle_versuchsperson = 'None'

    ## Anlegen des Session State. Bild, wenn es kein Bild gibt
    if 'picture_path' not in st.session_state:
        st.session_state.picture_path = 'data/pictures/none.jpg'

    ## Anlegen des Session State. EKG-Test, wenn es kein EKG-Test gibt
    if 'ekg_test' not in st.session_state:
        st.session_state.ekg_test = None

    # Schreibe die Überschrift
    st.write("# EKG APP")
    st.write("## Versuchsperson auswählen")

    # Auswahlbox, wenn Personen anzulegen sind
    st.session_state.aktuelle_versuchsperson = st.selectbox(
        'Versuchsperson',
        options = person_names, key="sbVersuchsperson")

    # Name der Versuchsperson
    st.write("Der Name ist: ", st.session_state.aktuelle_versuchsperson) 

    # Weitere Daten wie Geburtsdatum etc. schön anzeigen
    person_dict = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)
    Person_class = person.Person(person_dict)

    st.write("## Daten von ", st.session_state.aktuelle_versuchsperson)
    st.write("Geburtsdatum: ", person_dict["date_of_birth"])
    st.write("Alter: ", Person_class.calc_age())
    st.write("ID: ", person_dict["id"])
    st.write("maximale Herzfrequenz: ", Person_class.calc_max_heart_rate())



    # Nachdem eine Versuchsperson ausgewählt wurde, die auch in der Datenbank ist
    # Finde den Pfad zur Bilddatei
    if st.session_state.aktuelle_versuchsperson in person_names:
        st.session_state.picture_path = read_person_data.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)["picture_path"]
        # st.write("Der Pfad ist: ", st.session_state.picture_path) 

    #Bild anzeigen
    image = Image.open(st.session_state.picture_path)
    st.image(image, caption=st.session_state.aktuelle_versuchsperson)

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
    fig = current_ekg_data_class.plot_time_series()

    st.plotly_chart(fig)

    # Herzrate bestimmen
    heartrate_array, mean_heartrate = current_ekg_data_class.estimate_heartrate()
    fig2 = current_ekg_data_class.plot_heartrate(heartrate_array)
    st.write("durchschnittliche Herzfrequenz: ", int(mean_heartrate))
    st.plotly_chart(fig2)

