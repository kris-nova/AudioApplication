###############################################################################
#
# IntervalData
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

import numpy as np
import sys

from pprint import pprint
#from functions import Bright
#from functions import Tight


class IntervalData:
    '''
        Interval Data
        
        Data modeling for each interval we have configured to process
        Intervals are defined by the
    '''

    #Level 0 analysis:  volume information 
    #Level 0 analysis do not require an FFT
    maxvol  = 0 # max volume over this interval
    minvol  = 0 # min volume over this interval
    meanvol = 0 # mean volume over this interval
    volran  = 0 # just maxvol - minvol
    stdvol  = 0 # standard deviation of volume over this TIME interval

    #Level 1 analysis:  Power Information (i.e., FREQUENCY information)
    central_freq = 0 # power-averaged mean frequency
    freq_sdev = 0    # standard deviation (2nd moment) of frequency power distribution
    freq_skew =0     # skewness (3rd moment) of frequency power distribution
    freq_kurt = 0    # kurtosis (4th moment) of frequency power distribution 
    minpow = 0       # minimum power
    maxpow = 0       # maximum power
    meanpow = 0      # mean power
    powran = 0       # max power - min power
    stdpow = 0       # standard deviation of power over this FREQUENCY interval


    data = [1]
    ''' list
    List of data
    '''
    
    analysis_level = -1
    ''' int
    The analysis level for this object
    '''
    
    fhz = []
    ''' list
    List of frequencies
    '''
    
    dt = -1
    ''' int
    Delta time for the object'''
    
    def __init__(self, data=[1], analysis_level=0, fhz=[], dt=-1, power = [],pbounds = [],
        note_frequency = [], plot_info = -1):
        '''
            Will init the class and run accordingly
        '''

        self.data = data
        self.analysis_level = analysis_level
        self.fhz = fhz
        self.dt = dt
#         for d in np.nditer(data):
#             print d
#         sys.exit(1)

        #We have a series of analysis_levels that are increasingly complex
        # analysis level N may depend on levels 0 through N-1, and so
        # we use the logic below with >=  and NOT ==.  This prevents
        # redundant code (i.e. level 0 analysis appearing in the level 1 branch)        
        if analysis_level == -1:
            # RUN LEVEL -1
            pass
        if analysis_level >= 0:
            volume = np.abs(data)
            self.maxvol  = np.max(volume)
            self.minvol  = np.min(volume)
            self.meanvol = np.mean(volume)
            self.volran = self.maxvol-self.minvol
            self.stdvol = np.std(volume)
            
        if analysis_level >= 1:
            # RUN LEVEL 1
            # Here we compute gross information about the power spectrum
            self.maxpow  = np.max(power)
            self.minpow  = np.min(power)
            self.meanpow = np.mean(power)
            self.powran  = self.maxpow-self.minpow
            self.stdpow  = np.std(power) 


            ptotal = np.sum(power)
            numerator = np.sum(power*self.fhz)
            cf = numerator/ptotal
            self.central_frequency = cf
            moment = self.fhz-cf
            self.freq_sdev = np.sum(power*(moment**2))
            self.freq_skew = np.sum(power*(moment**3))
            self.freq_kurt = np.sum(power*(moment**4))
           
        if analysis_level >= 2:
            # RUN LEVEL 2
            # Bin the power into bins associated with each piano key
            self.binned = self.bin_pow(power,fhz,pbounds)
            self.binned = self.binned/np.max(self.binned)
            if (plot_info != -1):
                plot_info.set_data(note_frequency, self.binned)
        if analysis_level >= 3:
            # RUN LEVEL 3
            # compute basic stats on the power within each bin
            self.note_stats = self.bin_stats(power,fhz,pbounds)
            
        if analysis_level >= 4:
            # RUN LEVEL 4
            pass

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

    def bin_stats(self,power,frequency,bounds):
        num_notes = len(bounds)
        nstats = 4
        note_stats = np.zeros((num_notes,nstats),dtype = 'float32')

        df = frequency[1]-frequency[0]
        for i in range(num_notes):
            i0 = int(bounds[i][0]/df)
            i1 = int(bounds[i][1]/df)
            if (i0 != i1):
                pslice = power[i0:i1]

                ptotal = np.sum(pslice)
                numerator = np.sum(pslice*frequency[i0:i1])
                cf = numerator/ptotal
                note_stats[i][0] = cf
                moment = frequency[i0:i1]-cf
                sdev = np.sum(pslice*(moment**2))
                note_stats[i][1] = sdev
                skew = np.sum(pslice*(moment**3))
                note_stats[i][2] = skew
                kurt = np.sum(pslice*(moment**4))
                note_stats[i][3] = kurt

        return note_stats
