from variables import MajorScale

class Bright:
    '''
        How likely is this a major key?
    '''
    
    chunk = ''
    score = 0
    
    def __init__(self, chunk):
        '''
            Will instantiate the class with a chunk of data to process
        '''
        self.chunk = chunk
    
    def process(self):
        '''
            Will process the data. This is separated into it's own method so
            we can control when any expensive operations happen. Abstraction 
            is good xD
        '''
        mscale = MajorScale.MajorScale(self.chunk)
        self.score = mscale.get_is_major_score()
    
    def get_score(self):
        '''
            Will return the score for this chunk of data
        '''
        return self.score