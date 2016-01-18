def gen_notes(noctaves = 7, full_keyboard = False):
    """Returns a nested list of notes and associated frequencies over
         the requested range of octaves.

       Parameters:
                    noctaves - Number of octaves' worth of notes to generate.
                               The first note is taken to be 3 octaves below middle C
                               at C1.  This parameter is optional and defaults to 7.
                    fullkeyboard - (optional; default is False)  When set, all 88 piano keys are returned
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
    if (full_keyboard):
        noctaves = 7
        notes.append(("A0",27.5))
        notes.append(("A0#",29.135))
        notes.append(("B0",30.868))
    for j in range(noctaves):
        for item in funds:
            note = item[0]+str(j+1)
            f = item[1]
            sn = item[2]
            if (sn == 's'):
                note = note+"#"
            f = f*(2**j)
            notes.append( (note,f))
    if (full_keyboard):
        notes.append(("C8",4186.0))
    return notes
