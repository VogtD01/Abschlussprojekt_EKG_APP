from polardata import PolarData

# Beispiel: Erstellung eines PolarData-Objekts mit Dummy-Daten
# Annahme: Die Daten sind bereits als pandas DataFrame geladen oder werden hier direkt geladen

# Dummy-Daten für den Test
import pandas as pd
import numpy as np

from polardata import PolarData
#from polardata import create_heartrate_curve

# Erstelle eine Instanz von PolarData mit spezifischen Daten
polar_data_instance = PolarData({
    "id": 1,
    "date": "2024-04-17",
    "data_link": "data/polar_data/Dominic_Vogt_2024-04-17_14-23-52_data.csv",
    "summary_link": "data/polar_data/Dominic_Vogt_2024-04-17_14-23-52_summary.csv"
})

# Zugriff auf die geladenen Daten
df_data = polar_data_instance.df_data
df_summary = polar_data_instance.df_summary

# Annahme: Die Methode plot_heart_rate_over_time ist in der Klasse PolarData definiert
#fig = polar_data_instance.plot_heart_rate_over_time(df_data)
#fig.show()

#print(polar_data_instance.create_heartrate_curve(df_data))

df = df_data
modified_df = PolarData.create_heartrate_curve(df)
print(modified_df)


fig_heartrate, fig_altitude, fig_speed, fig_power = PolarData.plot_polar_curves(df)
fig1 = PolarData.plot_polar_curves_together(df)
fig2 = PolarData.plot_heart_rate_over_time(df)

#fig_heartrate.show()
#fig_altitude.show()
#fig_speed.show()
#fig_power.show()

fig1.show()
fig2.show()



