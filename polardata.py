import pandas as pd
import plotly.express as px
import numpy as np
import json
import os
import streamlit_functions as sf
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


##############################

class PolarData:
    def __init__(self, polar_dict):
        self.id = polar_dict["id"]
        self.date = polar_dict["date"]
        self.data_link = polar_dict["data_link"]
        self.summary_link = polar_dict["summary_link"]

        self.df_data, self.df_summary = self.load_polar_data(self.data_link, self.summary_link)

    @staticmethod
    def load_polar_data(data_link, summary_link):
        df_data = pd.DataFrame()
        df_summary = pd.DataFrame()

        try:
            if os.path.getsize(data_link) > 0:  # Check if the file is not empty
                df_data = pd.read_csv(data_link)
            else:
                print(f"Die Datei {data_link} ist leer.")
        except pd.errors.EmptyDataError:
            print(f"Die Datei {data_link} ist leer oder nicht lesbar.")
        except Exception as e:
            print(f"Fehler beim Laden der Datei {data_link}: {e}")

        try:
            if os.path.getsize(summary_link) > 0:  # Check if the file is not empty
                df_summary = pd.read_csv(summary_link)
            else:
                print(f"Die Datei {summary_link} ist leer.")
        except pd.errors.EmptyDataError:
            print(f"Die Datei {summary_link} ist leer oder nicht lesbar.")
        except Exception as e:
            print(f"Fehler beim Laden der Datei {summary_link}: {e}")

        return df_data, df_summary

    @staticmethod
    def load_by_id(PersonID, PolarID=None):
        '''Eine Funktion, die die Polar-Daten anhand der ID lädt und die Daten als Dictionary zurückgibt.'''

        # Laden der Personendaten
        try:
            with open('data/person_db.json', 'r') as file:
                person_data = json.load(file)
        except FileNotFoundError:
            print("Datei nicht gefunden")
            return {}
        except json.JSONDecodeError:
            print("Fehler beim Dekodieren der JSON-Datei")
            return {}

        # Abrufen der Polar-Daten
        if PolarID is None:
            for eintrag in person_data:
                if eintrag["id"] == PersonID:
                    return eintrag.get("polar_tests", [])
            else:
                return []

        for eintrag in person_data:
            if eintrag["id"] == PersonID:
                for polar_test in eintrag.get("polar_tests", []):
                    if polar_test["id"] == PolarID:
                        return polar_test
        else:
            return {}

    @staticmethod
    def get_IDs():
        '''Eine Funktion, die alle Polar-Test-IDs aus den Personendaten abruft.'''

        ids = []
        try:
            with open('data/person_db.json', 'r') as file:
                person_data = json.load(file)
                for person in person_data:
                    if 'polar_tests' in person:
                        ids.extend([test['id'] for test in person['polar_tests']])
        except FileNotFoundError:
            print("Datei nicht gefunden")
        except json.JSONDecodeError:
            print("Fehler beim Dekodieren der JSON-Datei")
        return ids

    @staticmethod
    def delete_by_id(PersonID, PolarID, summary_link, data_link):
        '''Eine Funktion, die die Polar-Test-Daten anhand der ID löscht.'''

        # Laden der Personendaten
        try:
            with open('data/person_db.json', 'r') as file:
                person_data = json.load(file)
        except FileNotFoundError:
            print("Datei nicht gefunden")
            return
        except json.JSONDecodeError:
            print("Fehler beim Dekodieren der JSON-Datei")
            return

        # Entfernen der mit den Links verbundenen Dateien
        try:
            os.remove(summary_link)
            os.remove(data_link)
        except FileNotFoundError:
            print(f"Die Datei wurde nicht gefunden.")
        except Exception as e:
            print(f"Fehler beim Löschen der Datei: {e}")
            return

        # Finden der Polar-Test-Daten und Löschen derselben
        for eintrag in person_data:
            if eintrag["id"] == PersonID:
                if 'polar_tests' in eintrag:
                    for polar_test in eintrag["polar_tests"]:
                        if polar_test["id"] == PolarID:
                            eintrag["polar_tests"].remove(polar_test)
                            break

        # Speichern der aktualisierten Personendaten zurück in die Datei
        with open("data/person_db.json", "w") as file:
            json.dump(person_data, file, indent=4)

    
    def calculate_summary_stats(self):
        # Gesamtzeit berechnen
        total_duration = pd.to_timedelta(self.df_summary['Duration']).sum()

        # Gesamtdistanz berechnen
        total_distance = self.df_summary['Total distance (km)'].sum()

        # Durchschnittlichen Puls berechnen
        average_hr = self.df_summary['Average heart rate (bpm)'].mean()

        # Verbrannte Kalorien berechnen
        total_calories = self.df_summary['Calories'].sum()

        # Gesamtzeit in Minuten und Sekunden extrahieren
        total_minutes = int(total_duration.total_seconds() // 60)
        total_seconds = int(total_duration.total_seconds() % 60)

        # Gesamtzeit formatieren
        formatted_duration = "{}:{:02d}:{:02d}".format(total_minutes // 60, total_minutes % 60, total_seconds)

        return formatted_duration, total_distance, average_hr, total_calories
    

    
    @staticmethod
    def create_heartrate_curve(df, fs=1):
        time = np.arange(len(df)) / fs
        heartrate = df["HR (bpm)"]
        
        return pd.DataFrame({"Time": time / 60, "Heart Rate": heartrate})
    
    @staticmethod
    def create_altitude_curve(df, fs=1):
        time = np.arange(len(df)) / fs
        altitude = df["Altitude (m)"]
        
        return pd.DataFrame({"Time": time / 60, "Altitude": altitude})
    
    @staticmethod
    def create_speed_curve(df, fs=1):
        time = np.arange(len(df)) / fs
        speed = df["Speed (km/h)"]
        
        return pd.DataFrame({"Time": time / 60, "Speed": speed})
    
    @staticmethod
    def create_power_curve_overtime(df, fs=1):
        time = np.arange(len(df)) / fs
        power = df["Power (W)"]
        
        return pd.DataFrame({"Time": time / 60, "Power": power})
    ######################################
    
    def plot_heart_rate_with_zones(df, fs=1, max_heart_rate=200):
        df_heartrate = PolarData.create_heartrate_curve(df, fs)
        
        # Wenn max_heart_rate nicht angegeben ist, bestimme sie aus den Daten
        if max_heart_rate is None:
            max_heart_rate = np.max(df_heartrate['Heart Rate'])
        
        fig = px.line(df_heartrate, x='Time', y='Heart Rate', title='Herzfrequenz über Zeit')
        fig.update_layout(
            xaxis_title="Zeit (in Minuten)",
            yaxis_title="Herzfrequenz (in bpm)"
        )
        
        # Herzfrequenz-Zonen hinzufügen
        PolarData.add_heart_rate_zones(fig, df_heartrate['Time'], max_heart_rate)
        
        return fig

    def add_heart_rate_zones(fig, time_data, max_heart_rate):
        heart_rate_zones = [
            (0.5, 'Gray', 'Zone 1'),
            (0.6, 'Green', 'Zone 2'),
            (0.7, 'Yellow', 'Zone 3'),
            (0.8, 'Orange', 'Zone 4'),
            (0.9, 'Red', 'Zone 5')
        ]

        # Hinzufügen der Herzfrequenz-Zonen als Rechtecke
        for threshold, color, label in heart_rate_zones:
            fig.add_shape(
                type="rect",
                x0=time_data.iloc[0],
                y0=max_heart_rate * threshold,
                x1=time_data.iloc[-1],
                y1=max_heart_rate * (threshold + 0.1),
                line=dict(color=color, width=2),
                fillcolor=color,
                opacity=0.5,
                layer="below"
            )

            # Legende für Herzfrequenz-Zonen hinzufügen
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    color=color,
                    size=10
                ),
                name=label
            ))

##########################################
    def plot_polar_curves(df, fs=1):
        df_heartrate = PolarData.create_heartrate_curve(df, fs)
        df_altitude = PolarData.create_altitude_curve(df, fs)
        df_speed = PolarData.create_speed_curve(df, fs)
        df_power = PolarData.create_power_curve_overtime(df, fs)

        fig_heartrate = px.line(df_heartrate, x='Time', y='Heart Rate', title='Herzfrequenz über Zeit')
        fig_heartrate.update_layout(
            title="Herzfrequenz über Zeit",
            xaxis_title="Zeit (in Minuten)",
            yaxis_title="Herzfrequenz (in bpm)"
        )

        fig_altitude = px.line(df_altitude, x='Time', y='Altitude', title='Höhe über Zeit')
        fig_altitude.update_layout(
            title="Höhe über Zeit",
            xaxis_title="Zeit (in Minuten)",
            yaxis_title="Höhe (in Metern)"
        )

        fig_speed = px.line(df_speed, x='Time', y='Speed', title='Geschwindigkeit über Zeit')
        fig_speed.update_layout(
            title="Geschwindigkeit über Zeit",
            xaxis_title="Zeit (in Minuten)",
            yaxis_title="Geschwindigkeit (in km/h)"
        )

        fig_power = px.line(df_power, x='Time', y='Power', title='Leistung über Zeit')
        fig_power.update_layout(
            title="Leistung über Zeit",
            xaxis_title="Zeit (in Minuten)",
            yaxis_title="Leistung (in Watt)"
        )

        return fig_heartrate, fig_altitude, fig_speed, fig_power
    
    #plotten einer herzfrequenzkurve mit den herzfrequenzonen
    def plot_heartrate_with_zones(df, fs=1):
        df_heartrate = PolarData.create_heartrate_curve(df, fs)
        df_heartrate_zones = PolarData.create_heartrate_zones(df, fs)
        
        


    
    @staticmethod
    def plot_polar_curves_together(df, fs=1):
        df_heartrate = PolarData.create_heartrate_curve(df, fs)
        df_speed = PolarData.create_speed_curve(df, fs)
        df_altitude = PolarData.create_altitude_curve(df, fs)
        df_power = PolarData.create_power_curve_overtime(df, fs)

        fig = make_subplots(
            rows=4, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.1,
            subplot_titles=(
                "Herzfrequenz über Zeit",
                "Geschwindigkeit über Zeit",
                "Leistung über Zeit",
                "Höhe über Zeit"
            )
        )

        fig.add_trace(
            go.Scatter(x=df_heartrate['Time'], y=df_heartrate['Heart Rate'], name="Herzfrequenz", line=dict(color='red'), 
                    hoverinfo='x+y', mode='lines'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=df_speed['Time'], y=df_speed['Speed'], name="Geschwindigkeit", line=dict(color='blue'),
                    hoverinfo='x+y', mode='lines'),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=df_power['Time'], y=df_power['Power'], name="Leistung", line=dict(color='green'),
                    hoverinfo='x+y', mode='lines'),
            row=3, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=df_altitude['Time'], y=df_altitude['Altitude'], name="Höhe", line=dict(color='orange'),
                    hoverinfo='x+y', mode='lines'),
            row=4, col=1
        )

        fig.update_layout(
            height=900, 
            title_text="",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="right",
                x=1
            ),
            hovermode='x'
        )

        fig.update_xaxes(title_text="Zeit (in Minuten)", row=4, col=1)
        fig.update_yaxes(title_text="Herzfrequenz (in bpm)", row=1, col=1)
        fig.update_yaxes(title_text="Geschwindigkeit (in km/h)", row=2, col=1)
        fig.update_yaxes(title_text="Leistung (in Watt)", row=3, col=1)
        fig.update_yaxes(title_text="Höhe (in Metern)", row=4, col=1)

        return fig
    
    

############################################
   


#################################################################################################

def read_activity_csv_polar(path):
    df = pd.read_csv(path, sep=",", skiprows=2)
    return df

def find_best_effort(df, t_interval, fs=1):
    windowsize = t_interval * fs
    meanpower = df["Power (W)"].rolling(window=windowsize).mean()
    bestpower = meanpower.max()
    return bestpower

def create_power_curve(df, fs=1):
    intervals = np.arange(len(df)) / fs
    powercurve = [find_best_effort(df, int(i), fs) for i in intervals]
    return pd.DataFrame({"Powercurve": powercurve, "Intervall": intervals / 60})

def create_power_curve_easy(df, fs=1):
    intervals = [1, 5, 10, 30, 60, 120, 180, 300, 600, 1200, 1800, 3600, 5400, 7200]
    max_interval = len(df) / fs

    intervals = [i for i in intervals if i < max_interval]
    while intervals[-1] < max_interval:
        intervals.append(intervals[-1] * 2)

    powercurve = [find_best_effort(df, int(i), fs) for i in intervals]
    return pd.DataFrame({"Powercurve": powercurve, "Intervall": intervals})

def format_zeit(intervall):
    minuten = intervall // 60
    sekunden = intervall % 60
    return f"{minuten}:{sekunden:02d}"

def plot_powercurve_polar(df, fs=1):
    df_powercurve_easy = create_power_curve_easy(df, fs)
    df_powercurve = create_power_curve(df, fs)

    df_powercurve_easy['Formatierter Intervall'] = df_powercurve_easy['Intervall'].apply(format_zeit)

    fig_curve_sprinter = px.line(df_powercurve_easy, x='Formatierter Intervall', y='Powercurve', title='Powerkurve')
    fig_curve_sprinter.update_layout(
        title="Powerkurve Ansicht Logarithmisch",
        xaxis_title="Intervall (Minuten:Sekunden)",
        yaxis_title="Power in Watt"
    )

    fig_curve_normal = px.line(df_powercurve, x='Intervall', y='Powercurve', title='Lineare Skala auf der X-Achse')
    fig_curve_normal.update_layout(
        title="Powerkurve Normalansicht",
        xaxis_title="Intervall in Minuten",
        yaxis_title="Power in Watt"
    )
    return fig_curve_sprinter, fig_curve_normal

if __name__ == "__main__":


    """#df = read_activity_csv_polar("data/polar_data/Dominic_Vogt_2024-04-17_14-23-52_data.CSV")
    df = read_activity_csv_polar("data/polar_data/test.CSV")
    print(df.head())
    best_effort = find_best_effort(df, 1)
    print(best_effort)
    fig1, fig2 = plot_powercurve_polar(df, 1)
    fig1.show()
    fig2.show()"""

  