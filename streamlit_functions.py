import streamlit as st

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
        </style>
        """,
        unsafe_allow_html=True
    )


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

    

