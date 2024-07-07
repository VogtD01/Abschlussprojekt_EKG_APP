import pandas as pd
import plotly.express as px
import numpy as np

def read_activity_csv_polar(path="data/polar_data/Dominic_Vogt_2024-05-18_16-02-30.CSV"):
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
    df = read_activity_csv_polar()
    print(df.head())
    best_effort = find_best_effort(df, 1)
    print(best_effort)
    fig1, fig2 = plot_powercurve_polar(df, 1)
    fig1.show()
    fig2.show()