import pandas as pd
import plotly.express as px
import numpy as np
import json
import os
import streamlit_functions as sf


##############################

class PolarData:

    """def __init__(self, polar_dict):
        self.id = polar_dict["id"]
        self.date = polar_dict["date"]
        self.data_link = polar_dict["data_link"]
        self.summary_link = polar_dict["summary_link"]

        self.df_data, self.df_summary = sf.save_polar_data(self.data_link, self.summary_link)"""



    @staticmethod
    def load_by_id(PersonID, PolarID=None):
        '''A function that loads the Polar Data by id and returns the Data as a dictionary.'''
        
        # Load the person data
        try:
            with open('data/person_db.json', 'r') as file:
                person_data = json.load(file)
        except FileNotFoundError:
            print("Datei nicht gefunden")
            return {}
        except json.JSONDecodeError:
            print("Fehler beim Dekodieren der JSON-Datei")
            return {}
        
        # Get the polar data
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
        '''A function that retrieves all Polar test IDs from the person_data.'''
        
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

    
    def delete_by_id(PersonID, PolarID, summary_link, data_link):
        '''A function that deletes the Polar test data by id.'''
        
        # Load the person data
        try:
            with open('data/person_db.json', 'r') as file:
                person_data = json.load(file)
        except FileNotFoundError:
            print("Datei nicht gefunden")
            return
        except json.JSONDecodeError:
            print("Fehler beim Dekodieren der JSON-Datei")
            return
        
        # Remove the files associated with the links
        try:
            os.remove(summary_link)
            os.remove(data_link)
        except FileNotFoundError:
            print(f"Die Datei wurde nicht gefunden.")
        except Exception as e:
            print(f"Fehler beim Löschen der Datei: {e}")
            return
        
        # Find the Polar test data and delete it
        for eintrag in person_data:
            if eintrag["id"] == PersonID:
                if 'polar_tests' in eintrag:
                    for polar_test in eintrag["polar_tests"]:
                        if polar_test["id"] == PolarID:
                            eintrag["polar_tests"].remove(polar_test)
                            break
        
        # Save the updated person data back to the file
        with open("data/person_db.json", "w") as file:
            json.dump(person_data, file, indent=4)


    ################################################################################

    def calculate_summary_stats(self):
        # Gesamtzeit berechnen
        total_duration = pd.to_timedelta(self['Duration']).sum()
        
        # Gesamtdistanz berechnen
        total_distance = self['Total distance (km)'].sum()
        
        # Durchschnittlichen Puls berechnen
        average_hr = self['Average heart rate (bpm)'].mean()
        
        # Verbrannte Kalorien berechnen
        total_calories = self['Calories'].sum()
        
        return total_duration, total_distance, average_hr, total_calories

    # Beispiel DataFrame (ersetze dies mit deinem tatsächlichen DataFrame)

    


        
        



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

    df = pd.DataFrame("data/polar_data/Dominic_Vogt_2024-04-17_14-23-52_summary.csv")

    # Funktion aufrufen und Ergebnisse erhalten
    total_duration, total_distance, average_hr, total_calories = PolarData.calculate_summary_stats(df)

    # Ausgabe der Ergebnisse
    print(f"Gesamtzeit: {total_duration}")
    print(f"Gesamtdistanz: {total_distance} km")
    print(f"Durchschnittlicher Puls: {average_hr} bpm")
    print(f"Verbrannte Kalorien: {total_calories}")