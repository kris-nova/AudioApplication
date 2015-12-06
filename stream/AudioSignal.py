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
###############################################################################

import numpy as np
import sys

from stream import IntervalData
from pprint import pprint

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
    
    seg_length_to_run_level = {}
    ''' dict
    key-value pairs of segment lengths in seconds to their corresponding run levels'''
    
    
    num_segment_lengths = -1
    ''' int
    The number of segment lengths to run levels we are working with'''
    
    delta_time = -1
    ''' float
    The defined length in seconds for each segment
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
    
    nelem = []
    '''list
    List of elements
    '''
    
    indices = []
    ''' list
    List of indices used for placing chunks into each segment'''
    
    set_dtype = -1
    ''' int
    The datatype for each measurement'''
    
    def __init__ (self, delta_time=.001, seg_length_to_run_level={1:0, 10:1}, bytes_per_measurement=32, source=0):
        '''
            Will build and validate the object
            Will populate the data structures
        '''
        if (delta_time < 0):
            print "Major Error, Invalid input in AudioSignal"
            return -1
        self.consistent = True
        self.seg_length_to_run_level = seg_length_to_run_level
        self.num_segment_lengths = len(seg_length_to_run_level)
        self.delta_time = delta_time
        self.source_type = __SOURCE_ENUM__[source]
        self.set_dtype(bytes_per_measurement)
        self.nelem = []
        for seg_secs in self.seg_length_to_run_level:
            num = int(seg_secs / self.delta_time)
            self.segment_data.append(np.zeros(num, dtype=self.dtype))
            self.intervals.append([]) 
            self.indices.append(0)
            self.nelem.append(num)
            
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

    def add_chunk(self, chunk):
        '''
            Used to add a chunk of data
                chunk - SIGNED number (float or int)
        '''
        self.signal.append(chunk)
        i = 0  # TODO This can be done without a counter, need to verify with Nick first
        for seg_sec, run_level in self.seg_length_to_run_level.iteritems():
            self.segment_data[i][self.indices[i]] = chunk
            self.indices[i] += 1
            # We have been adding chunks until our index reaches the defined number of elements
            if (self.indices[i] == self.nelem[i]):
                interval = IntervalData.IntervalData(self.segment_data[i], run_level)
                pprint(vars(interval))
                sys.exit(1)
            i = i + 1
                
                
            
            
