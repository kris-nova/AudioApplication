###############################################################################
#
# variables
# 
#
# (c) 2015-2016 
# Soundeavor Holdings LLC
# All Rights Reserved
# More Information: `info@soundeavor.com`
#
# Author: Kris Childress
#
###############################################################################

from pprint import pprint
import sys

class VariableScore:
    '''
        The object representation of the Soundeavor variables
    '''
    brightness = 0
    intensity = 0
    tightness = 0
    fullness = 0
    fluidity = 0
    cleanliness = 0
    structure = 0
    
    def update_variables(self, audio_signal, last_interval):
        '''
            Will update our variables by running analysis on our current AudioSignal object
        '''
        last_interval.data = None
        analysis_level = last_interval.analysis_level
        pprint(vars(last_interval))
    
