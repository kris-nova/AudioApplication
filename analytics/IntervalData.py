import numpy as np

class IntervalData:
    def __init__(self, data=[1], fhz=[], dt=-1, analytics_level=0):
        self.test_answer = np.mean(data)
        
