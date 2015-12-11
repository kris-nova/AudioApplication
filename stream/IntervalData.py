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
    maxvol  = 0 # max volume over this interval
    minvol  = 0 # min volume over this interval
    meanvol = 0 # mean volume over this interval
    volran  = 0 # just maxvol - minvol
    stdvol  = 0 # standard deviation of volume over this interval

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
            pass
            
        if analytics_level >= 2:
            # RUN LEVEL 2
            pass
            
        if analytics_level >= 3:
            # RUN LEVEL 3
            pass
            
        if analytics_level >= 4:
            # RUN LEVEL 4
            pass
