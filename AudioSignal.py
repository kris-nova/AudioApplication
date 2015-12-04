import numpy as np
__SOURCE_MIC__ = 0
#..

class Asig:
    def __init__ (self,delta_time=.001, segment_lengths = [1], segment_analytics_levels=[0], bytes_per_measurement = 32, source = 0):
        '''
        
        '''
        self.consistent = False
        #////////////////////////////
        # First, make sure we have sensible input
        num_seg_sizes = len(segment_lengths)
        num_analytics_levels = len(segment_analytics_levels)
        dcheck = num_seg_sizes-num_analytics_levels

        if ( (dcheck == 0) and (num_seg_sizes >= 1) and (delta_time > 0) ):
            #We have been given consistent input
            #Initialize the data structure
            self.consistent = True
            self.num_seg_sizes = num_seg_sizes
            self.num_analytics_levels = num_analytics_levels
            self.segment_lengths = segment_lengths   # segment lengths in seconds
            self.analytics_levels = segment_analytics_levels  # level of analytics for each segment size
            self.delta_time = delta_time  # the time interval between measurements
            self.source_type = source
            self.nelem = [] # number of elements in each level of segment

            for i in range(self.num_seg_sizes):
                num = int(self.segment_lengths[i]/self.delta_time)
                self.nelem.append(num)
            self.signal = []  # the full signal
            self.intervals = [] # list of segment metadata objects
            for i in range(self.num_seg_sizes):
                self.intervals.append([]) 

            self.segment_data = []  # nested list of numpy arrays used in segment analysis
            self.indices = []  # list of indices used for placing chunks into each segment
            #set the data type
            self.set_dtype(bytes_per_measurement)

            # initialize the numpy arrays for the segment analyses
            for i in range(self.num_seg_sizes):
                self.segment_data.append(np.zeros(self.nelem[i],dtype = self.dtype))
                self.indices.append(0)
    def check_consistency(self):
        return self.consistent

    def set_dtype(self,bytes_per_measurement):
        if (bytes_per_measurement == 32):
            self.dtype = 'float32'

    def add_chunk(self,chunk):
        # chunk is a SIGNED number of int or float type
        self.signal.append(chunk) # add the chunk to the end of the full signal
        for i in range(self.num_seg_sizes):
            # place the chunk to each segment
            self.segment_data[i][self.indices[i]] = chunk        
            self.indices[i]+=1
            if (self.indices[i] == self.nelem[i]):
                pass
                #self.intervals[i].append(IntervalData(self.segment_data[i],self.analytics_level[i]))
                #perform analytics on this chunk
            self.indices[i] = self.indices[i] % self.nelem[i]
            
#/////////////////////////////////////////
# Simple test function for this class            
def main():    
    #segment_analytics_levels = {}
    #segment_analytics_levels[1] = 0
    #segment_analytics_levels[10] = 1
    seg_dt = [1,10]
    seg_levels = [0,1]

    measure_dt = 0.01


    test_signal = Asig(delta_time = measure_dt, segment_lengths = seg_dt, segment_analytics_levels = seg_levels)
    print test_signal.check_consistency()


#/////////////////////////////
#Call Main
main()
