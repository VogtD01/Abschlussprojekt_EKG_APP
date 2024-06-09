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

    def find_peaks(self, start = None, end = None):
        '''A function that finds the peaks in the EKG data and returns the peaks as an array.'''
        
        peaks, _ = signal.find_peaks(self.df['EKG in mV'][start:end], height=340) 
        return peaks
    
    def estimate_heartrate(self):
        '''A function that estimates the heart rate from the EKG data and returns the heart rate as an array.'''
        peaks = self.find_peaks()
        
        # calculate the time between the peaks
        time_between_peaks_in_ms = np.arange(0, len(peaks)-1, 1, dtype='int64')
        for i in range(len(peaks)-1):
            time_between_peaks_in_ms[i] = (self.df['Time in ms'][peaks[i+1]] - self.df['Time in ms'][peaks[i]])
            
        # convert the time between the peaks to minutes
        time_between_peaks_in_ms = np.array(time_between_peaks_in_ms)
        time_between_peaks = (time_between_peaks_in_ms / 1000) / 60
        
        # calculate the heart rate
        heart_rate_array = 1 / time_between_peaks
        
        # mean heart rate
        mean_heart_rate = np.mean(heart_rate_array)

        return heart_rate_array, mean_heart_rate
    
    def plot_heartrate(self, heart_rate):
        '''A function that plots the heart rate from the EKG data.'''

        peaks = self.find_peaks()

        #smooth the heart rate 
        heart_rate = signal.savgol_filter(heart_rate, 100, 2)
        
        # plot the heart rate
        time_ms = self.df['Time in ms'][peaks[1:]]
        time_s = time_ms / 1000 
        fig = px.line(x = time_s, y = heart_rate, title='Heart Rate', labels={'x':'Time in s', 'y':'Heart Rate in bpm'})
        
        return fig

    def plot_time_series(self, start, end, peaks = False):
        '''A function that plots the EKG data as a time series.'''

        # create a  empty figure
        fig = go.Figure()
        
        # add the EKG data
        mV = self.df['EKG in mV']
        time = self.df['Time in ms'] / 1000

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
            # add the peaks (optional)
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
                name='T-Peaks'
                ))
        
        # add the layout
        fig.update_layout(
            title='EKG Data',
            xaxis_title='Time in s',
            yaxis_title='EKG in mV'
        )
        return fig


if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    
    ekg_dict = EKGdata.load_by_id(1, 1)
    ekg = EKGdata(ekg_dict)
    	
    time_s = ekg.df['Time in ms'] / 1000
    plt = ekg.plot_time_series(0, 15)
    heartrate_array, meanhr = ekg.estimate_heartrate()
    fig = ekg.plot_heartrate(heartrate_array)   
    
    
