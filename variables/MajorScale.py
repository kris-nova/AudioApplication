import sys

from aubio import source, pitch, freqtomidi

class MajorScale:
    '''
        Will return the likelihood that the chunk is in a major key
    '''

    chunk = ''
    
    def __init__(self, chunk, tolerance = 0.8):
        self.chunk = chunk
        downsample = 1
        win_s = 4096 / downsample # fft size
        hop_s = 512  / downsample # hop size
        pitch_o = pitch("yin", win_s, hop_s, samplerate)
        pitch_o.set_unit("midi")
        pitch_o.set_tolerance(tolerance)
        x = pitch_o(self.chunk)
        print x
            
    
    def get_is_major_score(self):
        '''
            Will return a number on a scale of -10 to 10
            Where :
                -10 is complete opposite of major
                0 is neutral
                10 is completely major
        '''
    
    
   