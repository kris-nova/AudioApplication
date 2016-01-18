###############################################################################
#
# AudioSignal
# 
#
# (c) 2015-2016 
# Soundeavor Holdings LLC
# All Rights Reserved
# More Information: `info@soundeavor.com`
#
# Author: Nick Featherstone
# Author: Kris Childress
#
###############################################################################
import matplotlib.pyplot as plt
import numpy as np
import sys
import operator

from pprint import pprint
from stream import IntervalData
from analysis import variables
from stream import music_scale as ms
# DEF  - Default (unknown)
# MIC  - Local microphone
# WEB  - Web application via protocol
# DSK  - Local disk
# ARCH - Archived data via S3 
__SOURCE_ENUM__ = ["DEF", "MIC", "WEB", "DSK", "ARCH"]

class AudioSignal:
    '''
        AudioSignal
        
        Used to model the data for an incoming stream of data
        Also contains methods for interacting and manipulating the stream
    '''
    
    consistent = False
    ''' bool
    Flag to show if we have consistent data for the object '''
    
    seg_length_to_analysis_level = {}
    ''' dict
    key-value pairs of segment lengths in seconds to their corresponding run levels'''
    
    
    num_segment_lengths = -1
    ''' int
    The number of segment lengths to run levels we are working with'''

    chunk_size = -1
    '''
        The number of audio samples added at once.
    '''
    
    dt = -1
    ''' float
    The time (in seconds) between adjacent audio samples.  This is typically around 1/44100 seconds.
    '''
    
    source_type = -1
    ''' int
    Enum for source types
    '''
    
    signal = []
    ''' list
    The full captured signal
    '''
    
    intervals = []
    ''' list
    List of IntervalData objects
    '''
    
    segment_data = []
    ''' list
    List of numpy arrays used in segment analysis
    '''

    workspace = []
    ''' list
    List of numpy arrays that will hold segment_data x a window function just before FFT is computed
    '''

    segment_nt = []
    ''' list
    Number of time samples associated with each segment size (i.e., length of each numpy array)
    '''

    window_functions = []
    ''' list
    List of numpy arrays containing the apodization window used when computing each segment power array
    '''

    segment_time = []
    ''' list
    List of numpy arrays containing the time axis corresponding to each segment_data array
    '''

    segment_power = []
    ''' list
    List of numpy arrays containing the power associated with each segment data array
    '''

    df = []
    ''' list
    List of delta_f for each frequency array below (spacing in frequency space between adjacent pixels)
    '''

    segment_frequency = []
    ''' list
    List of numpy arrays containing the frequency associated with each segment power array
    '''

    tindex = []
    ''' list
    tindex[i] is starting index within segment_data[i] at which to add a new chunk
    '''

    nseg_sizes = 1
    '''
    Number of different segment sizes
    '''

    set_dtype = -1
    ''' int
    The datatype for each measurement'''

    segment_counter = 0
    ''' int
    How many segments have been added
    '''
    
    variable_score = None
    ''' VariableScore
    The variable score object for this submission
    '''


    notes = []
    ''' list
    List of tuples containing note information (letter, frequency, flat/sharp)
    '''

    note_frequency = []
    ''' list
    Just the frequency from the list of tuples above
    '''

    bounds = []
    ''' list
    List of 2-D lists containing the min/max frequency bracketing each note in notes
    '''

    #//////////////////////////

    
    interval_ratios = {}
    
    def __init__ (self, chunk_size, delta_time=.001, seg_par = [[1536],[1536*3],[1]], bytes_per_measurement=32, source=0):
        '''
            Will build and validate the object
            Will populate the data structures
            
            delta_time
        '''
        #seg_length_to_analysis_level = sorted(seg_length_to_analysis_level.items(), key=operator.itemgetter(0))
        #Todo = we need to sort the dict, or fix the list problems. Right now we are assuming the values are always sorted
        if (delta_time < 0):
            print "Major Error, Invalid input in AudioSignal"
            return -1
        self.consistent = True
        #self.seg_length_to_analysis_level = seg_length_to_analysis_level
        #self.num_segment_lengths = len(seg_length_to_analysis_level)
        self.dt = delta_time
        self.source_type = __SOURCE_ENUM__[source]
        self.set_dtype(bytes_per_measurement)
        self.variable_score = variables.VariableScore()
        self.chunk_size = chunk_size


        #Ready the workspace for each segment size:
        #Create arrays for data, window functions, power


        self.analysis_interval = seg_par[0]
        self.seg_sizes = seg_par[1]
        self.analysis_level = seg_par[2]

        self.nseg_sizes = len(self.seg_sizes)
        for i in range(self.nseg_sizes):
            nt = self.seg_sizes[i]
            a = np.zeros(nt,dtype='float32')
            self.segment_data.append(a)
            b = np.zeros(nt,dtype='float32')
            self.workspace.append(b)
            t = self.build_time(nt,self.dt)
            self.segment_time.append(t)

            w = self.build_window(nt)
            self.window_functions.append(w)

            nf = nt//2+1
            df = 1.0/(nt*self.dt)
            self.df.append(df)
            p = np.zeros(nf,dtype='float32')
            self.segment_power.append(p)
            f = self.build_time(nf,df) # get the frequency array
            self.segment_frequency.append(f)

            self.tindex.append(0) # time index used for adding chunks, adjusts as analysis proceeds


        for seg_secs, analysis_level in self.seg_length_to_analysis_level.iteritems():
            self.interval_ratios[analysis_level] = 1


        self.notes = ms.gen_notes(full_keyboard=True)
        for n in self.notes:
            self.note_frequency.append(n[1])
        self.get_bounds()

        #Initialize the numpy arrays that will hold the raw data for the different segment lengths
        
            
    def check_consistency(self):
        '''
            Will return the consistency value for the object
        '''
        return self.consistent

    def set_dtype(self, bytes_per_measurement):
        '''
            Used for setting the datatype based on bytes per measurement
        '''
        if (bytes_per_measurement == 32):
            self.dtype = 'float32'

    def build_window(self,n,sharp=50,roll = 0.1):
        #Builds a simple tanh apodization window
        x = np.zeros(n,dtype='float32')
        dx = 1.0/float(n-1)
        for i in range(n):
            x[i] = i*dx-0.5
        x1 = x.min()+roll
        x2 = x.max()-roll
        t1 = np.tanh((x-x1)*sharp)
        t2 = 1-np.tanh((x-x2)*sharp)
        result = 0.5*(t1+t2-1)
        return result

    def build_time(self,nt,dt):
        time = np.zeros(nt,dtype='float32')
        for i in range(nt):
            time[i] = i*dt
        return time


    def add_chunk(self,chunk, plot_info = -1):
        '''
            Used to add a chunk of data
                chunk - SIGNED number (float or int)
        '''
        #This code handles the power spectrum creation
        for i in range(self.nseg_sizes):
            nt = self.seg_sizes[i]
            i0 = self.tindex[i]
            i1 = i0+self.chunk_size
            self.segment_data[i][i0:i1] = chunk[0:self.chunk_size]
            if (i1 % self.analysis_interval[i] == 0):
                #print 'Analyzing level: ', i
                if (self.analysis_level[i] > 0):
                    #Spacing between samples and sample width are not necessarily the same
                    #We need to multiply by the appropriately shifted window function
                    #The end of the sample always sits at index i1-1
                    i2 = nt - i1
                    self.workspace[i][0:i1] = self.segment_data[i][0:i1]*self.window_functions[i][i2:nt]
                    self.workspace[i][i1:nt] = self.segment_data[i][i1:nt]*self.window_functions[i][0:i2]
                    self.segment_power[i][0:nt] = np.abs(np.fft.rfft(self.workspace[i]))

                    #print i0, i1, i2
                    #plt.subplot(311)
                    #plt.plot(self.segment_data[i])
                    #plt.subplot(312)
                    #plt.plot(self.segment_frequency[i],self.segment_power[i])
                    #plt.subplot(313)
                    #plt.plot(self.workspace[i])
                    binned = self.bin_pow(self.segment_power[i],self.segment_frequency[i],self.bounds)
                    binned = binned/np.max(binned)
                    if (i == 0 and plot_info != -1):
                        #plt.plot(self.note_frequency,binned,'ro')
                        #plt.show()
                        #print 'showing!'
                        plot_info.set_data(self.note_frequency,binned)
                    #interval = IntervalData.IntervalData(self.analysis_level[i],data, power = self.power[i], freq = self.frequency[i])
                else:
                    #interval = IntervalData.IntervalData(self.analysis_level[i],data)
                    pass

                #self.intervals[i].append(interval)
            self.tindex[i] += self.chunk_size
            self.tindex[i] = self.tindex[i] % nt  #Keep the time index within the appropriate range

    #///////////////////////////////////////////////////
    # These two routines are for generating a histogram of note power, binned by piano key
    # Ultimately, they might need to be moved to the interval object
    def get_bounds(self,wfactor=0.15):
        notes = self.notes
        num_notes = len(notes)
        half_width = (notes[1][1]-notes[0][1])*wfactor
        mn = notes[0][1] - half_width
        mx = notes[0][1] + half_width
        bounds = [[mn,mx] ]
        for i in range(1,num_notes-1):
            f = notes[i][1]
            mn = notes[i][1] - half_width
            half_width = (notes[i+1][1]-f)*wfactor
            mx = notes[i][1] + half_width
            bounds.append([mn,mx])

        half_width = (notes[num_notes-1][1]-notes[num_notes-1][1])*wfactor    

        mn = notes[num_notes-1][1] - half_width
        mx = notes[num_notes-1][1] + half_width
        bounds.append([mn,mx])
        self.bounds = bounds

    #///////////////////////////////////////////////////////////////////
    #Loop over the power spectrum, sum the power within each bin
    def bin_pow(self,power,frequency,bounds):
        num_notes = len(bounds)
        note_pow = np.empty(num_notes,dtype = 'float32')

        df = frequency[1]-frequency[0]
        for i in range(num_notes):
            i0 = int(bounds[i][0]/df)
            i1 = int(bounds[i][1]/df)
            psum = np.sum(power[i0:i1])
            note_pow[i] = psum
        return note_pow



    def add_chunk_defunct(self, chunk):
        '''
            Used to add a chunk of data
                chunk - SIGNED number (float or int)
        '''
        self.signal.append(chunk)
        self.segment_counter += 1
        self.segment_data.append(chunk)
        for seg_secs, analysis_level in reversed(self.seg_length_to_analysis_level.items()): #Loop in reverse
            n = (int(seg_secs / self.delta_time) * self.interval_ratios[analysis_level])
            # We have been adding chunks until our index reaches the defined number of elements
            if n == self.segment_counter:
                ia = seg_secs
                chunk_to_send = []
                while ia >= 1:
                    chunk_to_send.append(self.segment_data[self.segment_counter - ia])
                    ia -= 1
                #chunk_to_send was breaking Nick's code, only sending the chunk
                interval = IntervalData.IntervalData(chunk_to_send, analysis_level)
                self.intervals.append(interval)
                #
                # THREAD HERE
                #
                #    Eventually we will need to do some serious under the hood processing here
                #    For now, leaving this as a serial thread for ease in developing
                #
                # THREAD HERE
                #
                self.variable_score.update_variables(self, interval)  # Recursive object oriented programming, cool :D
            if (self.segment_counter % n) == 0:
                self.interval_ratios[analysis_level] += 1
            
            
                
            
            
