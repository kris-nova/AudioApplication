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
###############################################################################

import numpy as np
import sys

from pprint import pprint
from functions import Bright
from functions import Tight


class IntervalData:
    '''
        Interval Data
        
        Data modeling for each interval we have configured to process
        Intervals are defined by the
    '''

    #Level 0 analytics:  volume information
    #Level 0 analytics do not require an FFT
    maxvol  = 0 # max volume over this interval
    minvol  = 0 # min volume over this interval
    meanvol = 0 # mean volume over this interval
    volran  = 0 # just maxvol - minvol
    stdvol  = 0 # standard deviation of volume over this TIME interval

    #Level 1 analytics:  Power Information (i.e., FREQUENCY information)
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
    
    analytics_level = -1
    ''' int
    The analytics level for this object
    '''
    
    fhz = []
    ''' list
    List of frequencies
    '''
    
    dt = -1
    ''' int
    Delta time for the object'''
    
    def __init__(self, data=[1], analytics_level=0, fhz=[], dt=-1,):
        '''
            Will init the class and run accordingly
        '''
        self.data = data
        self.analytics_level = analytics_level
        self.fhz = fhz
        self.dt = dt
#         for d in np.nditer(data):
#             print d
#         sys.exit(1)

        #We have a series of analytics_levels that are increasingly complex
        # Analytics level N may depend on levels 0 through N-1, and so
        # we use the logic below with >=  and NOT ==.  This prevents
        # redundant code (i.e. level 0 analyses appearing in the level 1 branch)        
        if analytics_level == -1:
            # RUN LEVEL -1
            pass
        if analytics_level >= 0:
            volume = np.abs(data)
            self.maxvol  = np.max(volume)
            self.minvol  = np.min(volume)
            self.meanvol = np.mean(volume)
            self.volran = self.maxvol-self.minvol
            self.stdvol = np.std(volume)
            
        if analytics_level >= 1:
            # RUN LEVEL 1
            # Here we compute the FFT and the Power
            # These are used for all analytics >= 1
            data_fft = np.fft.rfft(data)
            data_power = np.abs(data_fft)**2
            self.maxpow  = np.max(data_power)
            self.minpow  = np.min(data_power)
            self.meanpow = np.mean(data_power)
            self.powran  = self.maxpow-self.minpow
            self.stdpow  = np.std(data_power) 

            nframes = len(data)
            nfreq = nframes//2+1
            if (len(self.fhz) != nfreq):
                # The frequency wasn't supplied or has the wrong number of elements
                # Build the frequency
                # Note - we may not want to have fhz as an attribute
                self.fhz = np.empty(nframes,dtype='float32')
                df = 1.0/(dt*nframes)
                for i in range(nfreq):
                    self.fhz[i] = i*df
            ptotal = np.sum(data_power)
            numerator = np.sum(data_power*self.fhz)
            cf = numerator/ptotal
            self.central_frequency = cf
            moment = self.fhz-cf
            self.freq_sdev = np.sum(data_power*(moment**2))
            self.freq_skew = np.sum(data_power*(moment**3))
            self.freq_kurt = np.sum(data_power*(moment**4))
           
        if analytics_level >= 2:
            # RUN LEVEL 2
            pass
            
        if analytics_level >= 3:
            # RUN LEVEL 3
            pass
            
        if analytics_level >= 4:
            # RUN LEVEL 4
            pass
