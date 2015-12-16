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

import numpy as np
import sys
import operator

from pprint import pprint
from stream import IntervalData
from analysis import variables

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
    
    interval_ratios = {}
    
    def __init__ (self, delta_time=.001, seg_length_to_analysis_level={1:0, 5:1}, bytes_per_measurement=32, source=0):
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
        self.seg_length_to_analysis_level = seg_length_to_analysis_level
        self.num_segment_lengths = len(seg_length_to_analysis_level)
        self.delta_time = delta_time
        self.source_type = __SOURCE_ENUM__[source]
        self.set_dtype(bytes_per_measurement)
        self.variable_score = variables.VariableScore()
        for seg_secs, analysis_level in self.seg_length_to_analysis_level.iteritems():
            self.interval_ratios[analysis_level] = 1
            
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
            
            
                
            
            
