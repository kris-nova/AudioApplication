#!/usr/local/bin/python
import sys
import wave
import struct
import pprint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from stream import AudioSignal as AS
from stream import wave_tools as wt #.SoundData as SoundData

#from wave_tools import SoundData
def main():
    '''
        Open a wave file, process, and animate volume associated with each piano key
    '''
    sample_rate_hz = 44100.0 # a typical source (i.e., wave file and mic) samples 44,100 samples per second
    dt = 1.0 / sample_rate_hz   # Elapsed time between samples
    chunk_size = 1536 # number of frames read at once - this is approximately 1/30th of a second worth of data
    unpackstring = "hh"
    filename = sys.argv[1]

    # The following intervals are indicated in terms of sample count
    segment_interval = [chunk_size  ,chunk_size*3] # analyze in intervals separated by 1/30th and 1/10th of a second
    segment_length   = [chunk_size*5,chunk_size*15] # analyze intervals that are 1/10th and 3/10th of a second long
    analysis_level = [3,1] #two different analysis levels

    segment_info = [segment_interval, segment_length, analysis_level]
    aud_sig = AS.AudioSignal(chunk_size,delta_time=dt,seg_par = segment_info)
    try:
        sdata = wt.SoundData(filename)  # Read in the data
        num_chunks = len(sdata.mono)//chunk_size
    except:
        print "Invalid Input File"
        pass
    #num_chunks = 7
    efkeys = np.zeros(84,dtype='float32') #84 keys
    fig, line = plt.subplots()
    line, = plt.plot(efkeys,efkeys,'ro')
    plt.xlim([12,5000])
    plt.ylim([0,1.1])
    plt.xscale('log')
    #The animation example is carrying out this loop implicitly
    #for i in range(num_chunks):
    #    chunk = sdata.get_next_chunk(chunk_size)
    #    aud_sig.add_chunk(chunk,plot_info = plt_info)


    #these next two functions are just me attempting to clumsily drive the animator
    #If we didn't want to animate, use the loop above and forget the rest of this
    def grab_and_add(nothing):
        c = nothing
        chunk = sdata.get_next_chunk(chunk_size)
        aud_sig.add_chunk(chunk,plot_info = line)
        return line,
    def data_gen():
        for i in range(num_chunks-1):
            c = i
            yield c

    interv = 1000.0/30.0
    ani = animation.FuncAnimation(fig, grab_and_add,frames=data_gen, blit=False, interval=interv,
                                  repeat=False)        
    plt.show()
    
main()
