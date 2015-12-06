import numpy as np
import sys

from functions import Bright
from functions import Tight


class IntervalData:
    
    
    def __init__(self, data=[1], fhz=[], dt=-1, analytics_level=0):
        '''
            
        '''
        bright = Bright.Bright(data)
        bright.process()
        bright_score = bright.get_score()
        print bright_score
        
