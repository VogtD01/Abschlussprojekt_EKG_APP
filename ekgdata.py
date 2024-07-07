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
        
    @staticmethod
    def get_IDs():
        '''A function that returns all IDs of the EKG data as a list.'''

        # load the person data
        file = open("data/person_db.json")
        person_data = json.load(file)

        # get the ekg data
        ids = []
        for eintrag in person_data:
            for ekg_test in eintrag["ekg_tests"]:
                ids.append(ekg_test["id"])

        return ids

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        try:
            self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])
        except:
            self.df = pd.read_fit(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])
        # Die Zeitspalte neu starten von 0 bis zum Ende der Daten
        self.df['New Time in ms'] = self.df['Time in ms'] - self.df['Time in ms'].iloc[0]
        # Die Abtastfrequenz berechnen
        self.sample_rate = 1 / (self.df['New Time in ms'].iloc[1] - self.df['New Time in ms'].iloc[0])


    def find_peaks(self, start = None, end = None):
        '''A function that finds the peaks in the EKG data and returns the R-peaks as an array.'''
        
        peaks, _ = signal.find_peaks(self.df['EKG in mV'][start:end], height=340, distance=100, prominence=20)

        return peaks
    
    def find_t_peaks(self, start = None, end = None):
        '''A function that finds the T-Peaks in the EKG data and returns the T-peaks as a list.'''

        t_peaks, _ = signal.find_peaks(self.df['EKG in mV'][start:end], height=[320, 340], distance=100, prominence=20)

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


    def plot_heartrate(self, heart_rate, max_heart_rate):
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
        
        # add heartratezone 1
        if max(heart_rate) >= max_heart_rate * 0.5:
            fig.add_shape(
                type="rect",
                x0=time_s.iloc[0],
                y0=max_heart_rate * 0.5,
                x1=time_s.iloc[-1],
                y1=max_heart_rate * 0.6,
                line=dict(
                    color="Green",
                    width=2,
                ),
                fillcolor="Green",
                opacity=0.5,
                layer="below",
            )

            # add the heartrate zone to the legend
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    color='Green',
                    size=10,
                ),
                name='Heart Rate Zone 1'
            ))

        # add heartratezone 2
        if max(heart_rate) >= max_heart_rate * 0.6:
            fig.add_shape(
                type="rect",
                x0=time_s.iloc[0],
                y0=max_heart_rate * 0.6,
                x1=time_s.iloc[-1],
                y1=max_heart_rate * 0.7,
                line=dict(
                    color="yellow",
                    width=2,
                ),
                fillcolor="yellow",
                opacity=0.5,
                layer="below",
            )

            # add the heartrate zone to the legend
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    color='yellow',
                    size=10,
                ),
                name='Heart Rate Zone 2'
            ))

        # add heartratezone 3
        if max(heart_rate) >= max_heart_rate * 0.7:
            fig.add_shape(
                type="rect",
                x0=time_s.iloc[0],
                y0=max_heart_rate * 0.7,
                x1=time_s.iloc[-1],
                y1=max_heart_rate * 0.8,
                line=dict(
                    color="orange",
                    width=2,
                ),
                fillcolor="orange",
                opacity=0.5,
                layer="below",
            )

            # add the heartrate zone to the legend
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    color='orange',
                    size=10,
                ),
                name='Heart Rate Zone 3'
            ))

        # add heartratezone 4
        if max(heart_rate) >= max_heart_rate * 0.8:
            fig.add_shape(
                type="rect",
                x0=time_s.iloc[0],
                y0=max_heart_rate * 0.8,
                x1=time_s.iloc[-1],
                y1=max_heart_rate * 0.9,
                line=dict(
                    color="red",
                    width=2,
                ),
                fillcolor="red",
                opacity=0.5,
                layer="below",
            )

            # add the heartrate zone to the legend
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    color='red',
                    size=10,
                ),
                name='Heart Rate Zone 4'
            ))

        # add heartratezone 5
        if max(heart_rate) >= max_heart_rate * 0.9:
            fig.add_shape(
                type="rect",
                x0=time_s.iloc[0],
                y0=max_heart_rate * 0.9,
                x1=time_s.iloc[-1],
                y1=max_heart_rate,
                line=dict(
                    color="purple",
                    width=2,
                ),
                fillcolor="purple",
                opacity=0.5,
                layer="below",
            )

            # add the heartrate zone to the legend
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    color='purple',
                    size=10,
                ),
                name='Heart Rate Zone 5'
            ))

        # add the layout
        fig.update_layout(
            title='Heart Rate',
            xaxis_title='Time in s',
            yaxis_title='Heart Rate in bpm'
        )

        return fig

    def plot_time_series(self, start = None, end = None, peaks = False, t_peaks = False):
        '''A function that plots the EKG data as a time series.'''

        # create a  empty figure
        fig = go.Figure()
        
        # add the EKG data
        mV = self.df['EKG in mV']
        time = self.df['New Time in ms'] / 1000

        # cut the data
        mV_cut = np.array(mV[start:end])
        time_cut = np.array(time[start:end])  

        fig.add_trace(go.Scatter(
            x=time_cut,
            y=mV_cut,
            mode='lines',
            name='EKG Data'
        ))
        
        if peaks == True:
            # add the peaks 
            peaks = self.find_peaks(start, end)

            # Ensure all peak indices are within the valid range
            valid_peaks = [j for j in peaks if j < len(time_cut)]
            valid_peaks = np.array(valid_peaks)

            fig.add_trace(go.Scatter(
                x=[time_cut[j] for j in valid_peaks],
                y=[mV_cut[j] for j in valid_peaks],
                mode='markers',
                marker=dict(
                    size=8,
                    color='red',
                    symbol='cross'
                ),
                name='R-Peaks'
                ))
            
        if t_peaks == True:
            # add the peaks 
            t_peaks = self.find_t_peaks(start, end)

            # Ensure all peak indices are within the valid range
            valid_t_peaks = [j for j in t_peaks if j < len(time_cut)]
            valid_t_peaks = np.array(valid_t_peaks)

            fig.add_trace(go.Scatter(
                x=[time_cut[j] for j in valid_t_peaks],
                y=[mV_cut[j] for j in valid_t_peaks],
                mode='markers',
                marker=dict(
                    size=8,
                    color='green',
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

    def heartratevariability(self):
        '''A function that plots the heart rate variability.'''

        peaks = self.find_peaks()
        
        # calculate the time between the peaks
        time_between_peaks_in_ms = np.arange(0, len(peaks)-1, 1, dtype='int64')
        for i in range(len(peaks)-1):
            time_between_peaks_in_ms[i] = (self.df['New Time in ms'][peaks[i+1]] - self.df['New Time in ms'][peaks[i]])
        
        # calculate the heart rate variability
        heart_rate_variability = abs(np.diff(time_between_peaks_in_ms))

        # mean heart rate variability
        mean_heart_rate_variability = np.mean(heart_rate_variability)

        #max heart rate variability
        max_heart_rate_variability = np.max(heart_rate_variability)

        #min heart rate variability
        min_heart_rate_variability = np.min(heart_rate_variability)


        time_ms = self.df['New Time in ms'][peaks]
        time_s = time_ms / 1000

        # create a figure
        fig = go.Figure()

        # add the heart rate variability to the figure
        fig.add_trace(go.Scatter( 
            x = time_s[1:],
            y = heart_rate_variability,
            mode='lines', 
            name='Heart Rate Variability'))
        
        # add the layout
        fig.update_layout(
            title='Heart Rate Variability',
            xaxis_title='time in s',
            yaxis_title='Heart Rate Variability in ms'
        )

        return fig, mean_heart_rate_variability, max_heart_rate_variability, min_heart_rate_variability
    
    def RT_interval(self):
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

        #mean/ max/ min RT interval
        mean_RT_interval = np.mean(RT_interval)
        max_RT_interval = np.max(RT_interval)
        min_RT_interval = np.min(RT_interval)
        
        return mean_RT_interval, max_RT_interval, min_RT_interval


if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    
    ekg_dict = EKGdata.load_by_id(1, 1)
    
    ekg = EKGdata(ekg_dict)
    	
    

    

    
    
    
    
