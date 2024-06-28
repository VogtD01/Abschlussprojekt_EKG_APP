import json
import pandas as pd
import scipy.signal as signal
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden
class EKGdata:

    @staticmethod
    def load_by_id(PersonID, EKGID = "None"):
        '''A function that loads the EKG Data by id and returns the Data as a dictionary.'''

        # load the person data
        file = open("data/person_db.json")
        person_data = json.load(file)

        # get the ekg data
        if PersonID  == "None":
            return None
        
        if EKGID == "None":
            for eintrag in person_data:
                if eintrag["id"] == PersonID:
                    return eintrag["ekg_tests"]
            else:
                return {}
            
        for eintrag in person_data:
            if eintrag["id"] == PersonID:
                for ekg_test in eintrag["ekg_tests"]:
                    if ekg_test["id"] == EKGID:  
                        return ekg_test
        else:
            return {}

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])
        # Die Zeitspalte neu starten von 0 bis zum Ende der Daten
        self.df['New Time in ms'] = self.df['Time in ms'] - self.df['Time in ms'].iloc[0]
        # Die Abtastfrequenz berechnen
        self.sample_rate = 1 / (self.df['New Time in ms'].iloc[1] - self.df['New Time in ms'].iloc[0])


    def find_peaks(self, start = None, end = None):
        '''A function that finds the peaks in the EKG data and returns the R-peaks as an array.'''
        
        peaks, _ = signal.find_peaks(self.df['EKG in mV'][start:end], height=340)

        return peaks
    
    def find_t_peaks(self):
        '''A function that finds the T-Peaks in the EKG data and returns the T-peaks as a list.'''

        t_peaks, _ = signal.find_peaks(self.df['EKG in mV'], height=[320, 340])

        return t_peaks


    def estimate_heartrate(self):
        '''A function that estimates the heart rate from the EKG data and returns the heart rate as an array.'''
        peaks = self.find_peaks()
        
        # calculate the time between the peaks
        time_between_peaks_in_ms = np.arange(0, len(peaks)-1, 1, dtype='int64')
        for i in range(len(peaks)-1):
            time_between_peaks_in_ms[i] = (self.df['New Time in ms'][peaks[i+1]] - self.df['New Time in ms'][peaks[i]])
            
        # convert the time between the peaks to minutes
        time_between_peaks_in_ms = np.array(time_between_peaks_in_ms)
        time_between_peaks = (time_between_peaks_in_ms / 1000) / 60
        
        # calculate the heart rate
        heart_rate_array = 1 / time_between_peaks
        
        # mean heart rate
        mean_heart_rate = np.mean(heart_rate_array)

        #max heart rate
        max_heart_rate = np.max(heart_rate_array)

        #min heart rate
        min_heart_rate = np.min(heart_rate_array)  

        return heart_rate_array, mean_heart_rate, max_heart_rate, min_heart_rate
    
    def calc_heartrate_for_time(self, start, end):
        '''A function that calculates the heart rate for a given time range.'''
        peaks = self.find_peaks(start, end)
        
        # calculate the time between the peaks
        time_between_peaks_in_ms = np.arange(0, len(peaks)-1, 1, dtype='int64')
        for i in range(len(peaks)-1):
            time_between_peaks_in_ms[i] = (self.df['New Time in ms'][peaks[i+1]] - self.df['New Time in ms'][peaks[i]])
            
        # convert the time between the peaks to minutes
        time_between_peaks_in_ms = np.array(time_between_peaks_in_ms)
        time_between_peaks = (time_between_peaks_in_ms / 1000) / 60
        
        # calculate the heart rate
        heart_rate_array = 1 / time_between_peaks
        
        # mean heart rate
        mean_heart_rate = np.mean(heart_rate_array)

        #max heart rate
        max_heart_rate = np.max(heart_rate_array)

        #min heart rate
        min_heart_rate = np.min(heart_rate_array)

        return mean_heart_rate, heart_rate_array, max_heart_rate, min_heart_rate


    def plot_heartrate(self, heart_rate):
        '''A function that plots the heart rate from the EKG data.'''

        peaks = self.find_peaks()

        #smooth the heart rate 
        heart_rate = signal.savgol_filter(heart_rate, 100, 2)
        
        # plot the heart rate
        time_ms = self.df['New Time in ms'][peaks]
        time_s = time_ms / 1000

        # create a figure
        fig = go.Figure()

        # add the heart rate to the figure
        fig.add_trace(go.Scatter(
            x = time_s, 
            y = heart_rate, 
            mode='lines', 
            name='Heart Rate'))
        
        # add the mean heart rate
        fig.add_trace(go.Scatter(
            x = time_s, 
            y = np.mean(heart_rate) * np.ones(len(heart_rate)), # plot the mean heart rate
            mode='lines',
            line=dict(dash='dash'), 
            name='Mean Heart Rate'))
    
        # add the layout
        fig.update_layout(
            title='Heart Rate',
            xaxis_title='Time in s',
            yaxis_title='Heart Rate in bpm'
        )
        return fig

    def plot_time_series(self, start = None, end = None, peaks = False):
        '''A function that plots the EKG data as a time series.'''

        # create a  empty figure
        fig = go.Figure()
        
        # add the EKG data
        mV = self.df['EKG in mV']
        time = self.df['New Time in ms'] / 1000

        # cut the data
        mV = mV[start:end]
        time = time[start:end]  

        fig.add_trace(go.Scatter(
            x=time,
            y=mV,
            mode='lines',
            name='EKG Data'
        ))
        
        if peaks == True:
            # add the peaks 
            peaks = self.find_peaks(start, end)
            fig.add_trace(go.Scatter(
                x=[time[j] for j in peaks],
                y=[mV[j] for j in peaks],
                mode='markers',
                marker=dict(
                    size=8,
                    color='red',
                    symbol='cross'
                ),
                name='R-Peaks'
                ))

        # add the layout
        fig.update_layout(
            title='EKG Data',
            xaxis_title='Time in s',
            yaxis_title='EKG in mV'
        )
        return fig

    def heartratevariability(self): # nicht fertig
        '''A function that plots the heart rate variability.'''

        peaks = self.find_peaks()
        
        # calculate the time between the peaks
        time_between_peaks_in_ms = np.arange(0, len(peaks)-1, 1, dtype='int64')
        for i in range(len(peaks)-1):
            time_between_peaks_in_ms[i] = (self.df['New Time in ms'][peaks[i+1]] - self.df['New Time in ms'][peaks[i]])
        
        #create the figure
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x = np.arange(0, len(time_between_peaks_in_ms), 1),
            y = time_between_peaks_in_ms,
            mode='lines',
            name='Heart Rate Variability'
            ))

        return fig
    
    def RT_interval(self): # fehlerhaft; Ausgabe ist zum teil negativ
        '''A function that calculates the RT interval.'''
        r_peaks = self.find_peaks()
        t_peaks = self.find_t_peaks()
        
        # check if the first peak is a T-peak
        if r_peaks[0] > t_peaks[0]:
            t_peaks = t_peaks[1:]
        
        # check if the last peak is a T-peak
        if r_peaks[-1] > t_peaks[-1]:
            r_peaks = r_peaks[:-1]

        # check if the length of the peaks is the same
        if len(r_peaks) > len(t_peaks):
            r_peaks = r_peaks[:len(t_peaks)]

        elif len(t_peaks) > len(r_peaks):
            t_peaks = t_peaks[:len(r_peaks)]

        RT_interval = np.zeros(len(r_peaks))
        for i in range(len(r_peaks)):
            RT_interval[i] = self.df['New Time in ms'][t_peaks[i]] - self.df['New Time in ms'][r_peaks[i]]

        return RT_interval


if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    
    ekg_dict = EKGdata.load_by_id(1, 1)
    ekg = EKGdata(ekg_dict)
    	
    time_s = ekg.df['New Time in ms'] / 1000
    #plt = ekg.heartratevariability()
    p_peaks = ekg.find_peaks()
    t_peaks = ekg.find_t_peaks()
    
    RT_interval = ekg.RT_interval()
    print(RT_interval)  
    #plt = px.line(x = len(RT_interval), y = RT_interval)
    #plt.show()

    

    
    
    
    
