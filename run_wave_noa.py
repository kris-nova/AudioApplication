#!/usr/local/bin/python
import sys
import wave
import struct
from stream import AudioSignal
#from stream import AubioProcess


#def run_aubio():
    #ap = AubioProcess.AubioProcess(sys.argv[1])
    # bright_score = ap.get_bright_score(0.0)
    #tight_score = ap.get_tight_score()
    
    
def run_in_house():
    '''
        Will run a wave file
    '''
    
    readframes = 44000
    measure_dt = 1.0 / 44000
    unpackstring = "88000h"
    
    filename = sys.argv[1]
    try:
        wav_stream = wave.open(filename, 'r')
    except:
        print "Invalid Input File"
        pass
    all_frames = wav_stream.getnframes()

    aud_sig = AudioSignal.AudioSignal(delta_time=measure_dt)
    while(all_frames >= 0):
        chunk = wav_stream.readframes(readframes)
        all_frames = all_frames - 1
        try:
            unpacked = struct.unpack(unpackstring, chunk)
        except:
            pass
        aud_sig.add_chunk(unpacked[0])
        
    
# run_aubio()
run_in_house()
