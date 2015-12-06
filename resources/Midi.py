import sys

def get_midi_note_values():
    '''
        Returns a dictionary of MIDI note values indexed by number
    '''
    i = 0
    notes = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
    n = 0
    note_values = {}
    while i <= 127:
        note_values[i] = notes[n]
        i = i + 1
        if n == 11:
            n = 0
        else:
            n = n + 1
    return note_values

def get_notes_dict():
    notes = {}
    notes["c"] = 0
    notes["c#"] = 0 
    notes["d"] = 0
    notes["d#"] = 0
    notes["e"] = 0
    notes["f"] = 0
    notes["f#"] = 0
    notes["g"] = 0
    notes["g#"] = 0
    notes["a"] = 0
    notes["a#"] = 0
    notes["b"] = 0
    return notes

def get_chromatic_scale(fund):
    scale = {}
    notes = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
    i = 0
    for n in notes:
        if n == fund:
            d = 0
            while d <= 11:
                scale[d] = [notes[i + d]]
                d = d + 1
            break;
        i = i + 1
    return scale
        
         
def get_midi_frequency_values():
    '''
        Returns a dictionary of MIDI note frequencies indexed by number
    '''
    
def gen_notes(noctaves = 7):
    """Returns a nested list of notes and associated frequencies over
         the requested range of octaves.
    
       Parameters:
                    noctaves - Number of octaves' worth of notes to generate.
                               The first note is taken to be 3 octaves below middle C
                               at C1.  This parameter is optional and defaults to 7.
       Returns:
                    notes    - a list of two-element tuples corresponding to the
                               desired notes in the format (note name, note frequency [in Hz])
    """
    # returns a list of notes and their frequencies (in Hz)
    # Noctaves octaves are generated, beginning with C1
    notes = [] # List of tuples describing notes and their frequencies to be returned
    funds = [] # fundamental notes
    
    #Define a set of fundamental notes, starting with C1
    # 'n' denotes "normal".  's' denotes "sharp"
    funds.append(("C",32.703,'n')) 
    funds.append(("C",34.648,'s')) # C1#
    funds.append(("D",36.708,'n'))
    funds.append(("D",38.891,'s')) # D1#
    funds.append(("E",41.203,'n'))
    funds.append(("F",43.654,'n'))
    funds.append(("F",46.249,'s')) # F1#, etc.
    funds.append(("G",48.999,'n'))
    funds.append(("G",51.913,'s'))
    funds.append(("A",55.000,'n'))
    funds.append(("A",58.270,'s'))
    funds.append(("B",61.735,'n'))
    
    #Generate the note list by computing harmonics of the fundamentals.
    #Members of octave X have twice the frequency of members of octave X-1
    for j in range(noctaves):
        for item in funds:
            note = item[0]+str(j+1)
            f = item[1]
            sn = item[2]
            if (sn == 's'):
                note = note+"#"
            f = f*(2**j)
            notes.append( (note,f))
    
    return notes
