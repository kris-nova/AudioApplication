import sys
import numpy
from aubio import source, pitch, freqtomidi, onset
from analysis import scale


class AubioProcess:
    
    source = None
    win_s = 512
    hop_s = 512
    
    def __init__(self, filename, samplerate=44100, win_s=1024, hop_s=512):
        '''
        
        '''
        self.source = source(filename, samplerate, hop_s)
        self.win_s = win_s
        self.hop_s = hop_s
        
    def get_bright_score(self, tolerance=0.8):
        samplerate = self.source.samplerate
        pitch_o = pitch("mcomb", self.win_s, self.hop_s, samplerate)
        pitch_o.set_unit("midi")
        pitch_o.set_tolerance(tolerance)
        total_frames = 0
        pitches = []
        confidences = []
        while True:
            samples, read = self.source()
            midi_pitch = pitch_o(samples)[0]
            confidence = pitch_o.get_confidence()
            if confidence < tolerance: midi_pitch = 0.
            pitches += [midi_pitch]
            confidences += [confidence]
            total_frames += read
            if read < self.hop_s: break

          
#         scale = scale.gen_notes()
#         a = {}
#         for p in pitches:
#             if p == 0.0: continue
#             smallest_delta = -1
#             for name, freq in scale:
#                 this_delta = abs(p - freq)
#                 if smallest_delta == -1:
#                     smallest_delta = this_delta
#                     continue;
#                 if this_delta < smallest_delta:
#                     winning_pitch = name
#                     smallest_delta = this_delta
#             try:
#                 a[winning_pitch] = a[winning_pitch] + 1
#             except:
#                 a[winning_pitch] = 1
#         sorted_notes = sorted(a.iteritems(), key=lambda (v, k): (k, v), reverse=True)
#         fundamental = sorted_notes[0]
#         for sn in sorted_notes:
#             print sn
#         print fundamental
#         sys.exit(1)    
        
        
        # 
        # Now we have our MIDI pitches, lets analyze    
        midi_values = scale.get_midi_note_values()
        
        notes = scale.get_notes_dict()
        for p in pitches:
            if p == 0: continue
            rp = int(round(p))
            if rp > 96 or rp < 52: continue
            v = midi_values[rp]
            notes[v] = notes[v] + 1
        sorted_notes = sorted(notes.iteritems(), key=lambda (v, k): (k, v), reverse=True)
        fundamental = sorted_notes[0][0]
        scale = scale.get_chromatic_scale(fundamental)
        major_indexes = [2, 4, 6, 7, 9]
        non_major_indexes = [1, 3, 5, 8, 10]
        total_major = 0
        total_non_major = 0
        for val in sorted_notes:
            n = val[0]
            s = val[1]
            for i in major_indexes:
                tn = scale[i][0]
                if n == tn:
                    total_major = total_major + s
                    break
            for i in non_major_indexes:
                tn = scale[i][0]
                if n == tn:
                    total_non_major = total_non_major + s
                    break
        bs = float(total_major) / float(total_non_major)
        if bs < 1 :
            brightness_score = (1 - bs) * -1 * 10
        else:
            brightness_score = (bs - 1) * 10
        
        for note, score in sorted_notes:
            print note + " :" + str(score)
        print "Fundamental : " + fundamental
        print str(total_major) + " / " + str(total_non_major)
        print "Score : " + str(brightness_score)
        
        
    def get_tight_score(self):
        o = onset("energy", self.win_s, self.hop_s, self.source.samplerate)
        onsets = []
        total_frames = 0
        while True:
            samples, read = self.source()
            if o(samples):
                onsets.append(o.get_last())
            total_frames += read
            if read < self.hop_s: break
        tsmean = numpy.mean(onsets)
        ts = tsmean / 100000
        print ts
        
        
        
        
        
