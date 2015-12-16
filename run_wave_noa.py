#!/usr/local/bin/python
import sys
import wave
import struct
import pprint

from stream import AudioSignal
    
def main():
    '''
        Will run a wave file
    '''
    
    readframes = 44000
    measure_dt = 1.0 / 44000
    unpackstring = "hh"
    filename = sys.argv[1]
    try:
        wav_stream = wave.open(filename, 'r')
    except:
        print "Invalid Input File"
        pass
    aud_sig = AudioSignal.AudioSignal(delta_time=measure_dt)
    for i in range(wav_stream.getnframes()):
        frame = wav_stream.readframes(1)
        unpacked = struct.unpack(unpackstring, frame)
        aud_sig.add_chunk(unpacked[0])
        
    
main()
