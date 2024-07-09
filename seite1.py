import streamlit as st
from PIL import Image

# Lade das Bild
image = Image.open('Bilder\dream_TradingCard.jpg')




# Funktion für die Titelseite
def seite1():
    # Erstelle das Layout
    st.markdown("<h1 style='color:White; text-align: center;'>Willkommen bei Cardio Coach</h1>", unsafe_allow_html=True)
    st.image(image, use_column_width=True)
    
    st.markdown("""
        <h2 style='color:White; text-align: center;'>Ihre App für umfassende Herz-Kreislauf-Überwachung und Analyse</h2>
        <p style='color:White; text-align: center;'>Cardio Coach bietet Ihnen folgende Funktionen:</p>
        <ul style='color:White;'>
            <li>EKG-Datenanalyse: Lesen Sie EKG-Daten ein und analysieren Sie diese in verschiedenen Zeitfenstern.</li>
            <li>Individuelle Herzfrequenzzonen: Definieren Sie Ihre eigenen Herzfrequenzzonen basierend auf persönlichen Daten.</li>
            <li>Polar-Datenintegration: Importieren Sie Trainingsdaten von Polar-Uhren und visualisieren Sie diese detailliert.</li>
            <li>Herzratenvariabilität (HRV): Analysieren Sie die Variationen in den Zeitintervallen zwischen aufeinanderfolgenden Herzschlägen.</li>
            <li>Benutzerverwaltung: Fügen Sie Benutzer hinzu, bearbeiten Sie deren Daten und verwalten Sie deren Aktivitäten.</li>
            <li>Vielfältige Plots: Erstellen Sie verschiedene Plots zur Visualisierung von Herzfrequenz, Leistung, Höhe und mehr.</li>
        </ul>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color:White; text-align: center;'>Starten Sie jetzt und überwachen Sie Ihre Herzgesundheit!</h3>", unsafe_allow_html=True)