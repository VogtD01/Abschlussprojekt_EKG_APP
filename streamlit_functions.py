import streamlit as st
import os
from PIL import Image
import pandas as pd

import streamlit as st

# Beispielpersonen
person_names = ["Person 1", "Person 2", "Person 3"]

# Funktion zum Einfügen benutzerdefinierter CSS
def set_bg_hack():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #0e1117;
            color: white;
        }}
        .stApp [data-testid="stSidebar"] {{
            background-color: #1a1b1f;
        }}
        .stApp .css-1aumxhk {{
            background-color: #1a1b1f;
            color: white;
        }}
        .stApp .stSelectbox label {{
            color: white;  /* Farbe des Labels ändern */
        }}
        .stApp .stTextInput label {{
            color: white;  /* Farbe des Labels für Eingabeboxen ändern */
        }}
        .stApp .stTextArea label {{
            color: white;  /* Farbe des Labels für Textarea ändern */
        }}
        .stApp .stNumberInput label {{
            color: white;  /* Farbe des Labels für Number Input ändern */
        }}
        .stApp .stDateInput label {{
            color: white;  /* Farbe des Labels für Date Input ändern */
        }}
        .stApp .stTimeInput label {{
            color: white;  /* Farbe des Labels für Time Input ändern */
        }}
        .stApp .stFileUploader label {{
            color: white;  /* Farbe des Labels für File Uploader ändern */
        }}
        .stApp .stColorPicker label {{
            color: white;  /* Farbe des Labels für Color Picker ändern */
        }}
        .stApp .stCheckbox div[data-testid="stCheckboxLabel"] > label {{
            color: white;  /* Farbe des Labels für Checkbox ändern */
        }}
        .stApp .stTabs [role="tab"] {{
            color: white;  /* Farbe des Texts in den Tabs ändern */
        }}
        .stApp .stTabs [role="tab"][aria-selected="true"] {{
            background-color: #1a1b1f;  /* Hintergrundfarbe des ausgewählten Tabs ändern */
            color: white;  /* Textfarbe des ausgewählten Tabs */
        }}
        .stApp .stImage .caption-container > .caption {{
            color: white;  /* Farbe der Bildunterschrift ändern */
        }}
        .stButton button {{
            background-color: #4CAF50; /* Green background */
            color: white; /* White text */
            border: none;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }}
        .stButton button:hover {{
            background-color: #45a049; /* Darker green on hover */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    

# Aufruf der Funktion zum Setzen der benutzerdefinierten CSS-Styles
set_bg_hack()




# Funktion zum Initialisieren des Session State

def initialize_session_state(): # Funktion zum Initialisieren des Session State
    # Anlegen des Session State. Aktuelle Versuchsperson, wenn es keine gibt
    if 'aktuelle_versuchsperson' not in st.session_state:
        st.session_state.aktuelle_versuchsperson = 'None'

    # Anlegen des Session State. Bild, wenn es kein Bild gibt
    if 'picture_path' not in st.session_state:
        st.session_state.picture_path = 'data/pictures/none.jpg'

    # Anlegen des Session State. EKG-Test, wenn es kein EKG-Test gibt
    if 'ekg_test' not in st.session_state:
        st.session_state.ekg_test = None

# Aufruf der Funktion, um den Session State zu initialisieren
initialize_session_state()  

# Funktion zum Anzeigen der Eingabeaufforderung für die Start- und Endzeit des Plots
def get_plot_time_range(max_time_seconds, sample_rate, default_start=0.0, default_end=10.0):
    """
    Bestimmt die Start- und Endzeit des Plots, falls keine Eingabe vom Benutzer erfolgt.

    Parameters:
    max_time_seconds (float): Die maximale Zeit in Sekunden.
    sample_rate (float): Die Abtastfrequenz des aktuellen EKGs.
    default_start (float): Die Standardstartzeit in Sekunden. Default ist 0.0.
    default_end (float): Die Standardendzeit in Sekunden. Default ist 10.0.

    Returns:
    int, int: Die berechneten Start- und Endwerte in Millisekunden.
    """
    # Fügen Sie eine Nummerneingabe für Start und Ende des Plots hinzu (in Sekunden)
    start_seconds = st.number_input("Start des Plots (in Sekunden)", 0.0, float(max_time_seconds), float(default_start))
    end_seconds = st.number_input("Ende des Plots (in Sekunden)", 0.0, float(max_time_seconds), float(default_end))

    # Standardwerte setzen, wenn keine Eingabe erfolgt
    if start_seconds == default_start:
        start_seconds = default_start  # Startzeitpunkt des Plots

    if end_seconds == float(max_time_seconds):
        end_seconds = default_end  # Endzeitpunkt des Plots

    # Umrechnung der Eingabewerte in Millisekunden
    start = int(start_seconds * 1000 * sample_rate)  # Sample-Rate gibt die Anzahl der Samples pro Sekunde an
    end = int(end_seconds * 1000 * sample_rate)

    return start, end

def save_image(image_name, image):
    '''Speichert das Bild im Ordner pictures ab.'''

    folder_name = 'data/pictures'
    name_of_file = image_name
    completeName = os.path.join(folder_name, name_of_file)

    image = Image.open(image)

    image.save(completeName)
    
    return completeName

def delete_image(image_path):
    '''Löscht das Bild aus dem Ordner pictures.'''

    os.remove(image_path)


def save_ekg_data(ekg_data, file_name):
    '''Speichert die EKG-Daten im Ordner data ab.'''

    folder_name = 'data/ekg_data'
    name_of_file = file_name
    completeName = os.path.join(folder_name, name_of_file)

    # EKG-Daten in ein DataFrame einlesen
    df = pd.read_csv(ekg_data, sep='\t', header=None, names=['EKG in mV','Time in ms',])

    mV = df['EKG in mV']
    mV = mV.tolist()

    time = df['Time in ms']
    time = time.tolist()

    # EKG-Daten in eine Textdatei schreiben
    with open(completeName, 'w') as file:
        for i in range(len(mV)):
            file.write(str(mV[i]) + '\t' + str(time[i]) + '\n')
        



    return completeName
        

    

        

