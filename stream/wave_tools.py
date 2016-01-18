import wave
import struct
import numpy as np
""" Tools for the manipulation of wav file data
    These tools build on python's intrinsic Wave module. 
    There may be some redundancy here.  One option is 
    to augment Python's wave.py directly.  This is
    faster for now.
"""

class SoundData:
    """ Class for storing and performing basic manipulations
        on sound data based on the wave-file format.  Input/Ouput
        to a wave file can be accomplished using methods in this class
        that wrap to routines in python's Wave module.

        Attributes:
                    nchannels - number of channels (1 for mono, 2 for stereo)
                    sampwidth - number of bytes per channel
                    framerate - number of frames (i.e., samples) per second
                    nframes   - number of frames
                    comptype  - compression type (NONE for wave format)
                    compname  - human readable compression type ('not compressed' = NONE)

                    frames    - bytestring representing entire wave signal

                    channels        - numpy array structured [0:nchannels-1,0:nframes-1] containing the audio signal
                    have_channels   - Boolean describing whether the frames have been unpacked yet

                    fftc (SOON)     - numpy array (complex) containing the fft of the different channels
                    powc (SOON)     - numpy array (real, 64 bit) containing the power spectrum of each channel

                    mono (SOON)     - numpy array containing the average signal, averaged over both channels
                    fftm (SOON)     - numpy array (complex) containing the fft of the mono signal
                    powm (SOON)     - numpy array(real, 64 bit) containing the power spectrum of the mono signal

        Methods:
                    __init__        - constructor method
                    setframes       - sets the value of frames
                    setpars         - sets the value of nchannels, sampwidth, ..., compname
                    
    """
    def __init__(self,wavfile='nothing'):
        self.have_fft = False
        self.have_channels = False
        self.index = 0 # for reading chunks
        if (wavfile != 'nothing'):
            self.read(wavfile)
        else:
            self.setpars((0,0,0,0,0,0))
            self.frames = 'no frames yet'

    def get_next_chunk(self,chunk_size):
        chunk = self.mono[self.index:self.index+chunk_size]
        self.index+=chunk_size
        return chunk

    def setframes(self,frames):
        self.frames = frames        
        self.build_channels()
        self.gettime()

    def setpars(self,wavpars):
            self.nchannels = wavpars[0]
            self.sampwidth = wavpars[1]
            self.framerate = wavpars[2]
            self.nframes   = wavpars[3]
            self.comptype  = wavpars[4]
            self.compname  = wavpars[5]        

    def getpars(self):
        wavpars = (self.nchannels, self.sampwidth, self.framerate,
                   self.nframes, self.comptype, self.compname)
        return wavpars

    def gettime(self):
        nt = self.nframes
        self.time = np.empty(nt,dtype = 'float32')
        dt = 1.0/self.framerate
        for i in range(nt):
            self.time[i] = i*dt

    def tospectral(self, channel = -1):
        if (not self.have_channels):
            self.build_channels()
            self.get_time()
        self.build_frequency()
        self.fft = np.empty((self.nchannels,self.nfreq),dtype='complex128')
        if (channel >= 0):
            self.fft[channel,:] = np.fft.rfft(self.channels[channel,:])
        else:
            for i in range(self.nchannels):
                self.fft[i,:] = np.fft.rfft(self.channels[i,:])
        self.have_fft = True

    def getpower(self,channel=-1):
        if (not self.have_fft):
             self.tospectral()
        self.power = np.empty((self.nchannels,self.nfreq),dtype='float64')
        if ( channel >= 0):
            self.power[channel,:] = np.abs(self.fft[channel,:])
        else:
            for i in range(self.nchannels):
                self.power[i,:] = np.abs(self.fft[i,:])   
            
    def build_frequency(self):
        time_span = self.time[self.nframes-1]-self.time[0]
        df = 1.0/time_span  # frequency resolution (Hz)
        self.nfreq = self.nframes//2+1
        self.frequency = np.empty(self.nfreq,dtype='float32')
        for i in range(self.nfreq):
            self.frequency[i] = i*df

    def write(self,filename):
            ww = wave.open(filename,'w')
            pars = self.getpars()
            ww.setparams(pars)
            ww.writeframes(self.frames)
            ww.close()

    def read(self,filename):
            wr = wave.open(filename,'r')
            wavpars = wr.getparams()
            self.setpars(wavpars)
            self.frames = wr.readframes(self.nframes)
            wr.close()

            self.build_channels()
            self.gettime()
    def build_channels(self):
            #Convert the bytestring to numbers.
            #For now, assume the data is 16 bit signed integer, and native Endian
            nstr = str(self.nframes*2)
            tmp = struct.unpack(nstr+"h",self.frames) 
            self.channels = np.empty((2,self.nframes),dtype = 'float32')
            self.mono = np.empty(self.nframes,dtype = 'float32')
            for i in range(self.nframes):
                i2 = i*2
                self.channels[0,i] = tmp[i2]
                self.channels[1,i] = tmp[i2+1]
                self.mono[i] = (self.channels[0,i]+self.channels[1,i])*0.5
            self.have_channels = True
    def subsample(self,tstart,tend, inplace = False):
        """
            Subsamples the frames of the wave
        """
        bpf = self.sampwidth*self.nchannels  #bpf = bytes per frame
        sec_per_frame = 1.0/self.framerate

        deltat = tend-tstart
        nfsample = int(self.framerate*deltat)

        fstart = int(tstart*self.framerate)
        fend = fstart+nfsample
        
        subsampled_frames = self.frames[fstart*bpf:fend*bpf]        
        wavepars = self.getpars()
        newpars = (wavepars[0], wavepars[1], wavepars[2],nfsample,
                   wavepars[4], wavepars[5])

        if (not inplace):
            new_data = SoundData()
            new_data.setpars(newpars)
            new_data.setframes(subsampled_frames)
            return new_data
        else:
            self.setpars(newpars)
            self.frames = subsampled_frames


