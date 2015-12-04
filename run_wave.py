#!/usr/local/bin/python
import sys
import wave
import struct
from analytics import AudioSignal

def main():
    '''
        Will run a wave file
    '''
    filename = sys.argv[1]
    try:
        wav_stream = wave.open(filename, 'r')
    except:
        print "Invalid Input File"
        pass
    all_frames = wav_stream.getnframes()
    seg_dt = [1, 30]
    seg_lvl = [0, 100]
    measure_dt = 1.0 / 44000
    aud_sig = AudioSignal.AudioSignal(delta_time=measure_dt, segment_lengths=seg_dt, segment_analytics_levels=seg_lvl)
    print aud_sig.check_consistency()
    while(all_frames >= 0):
        chunk = wav_stream.readframes(44000)
        all_frames = all_frames - 1
        try:
            unpacked = struct.unpack("88000h", chunk)
        except:
            pass
        aud_sig.add_chunk(unpacked[0])
        
    
main()
