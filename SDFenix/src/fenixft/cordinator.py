'''
Created on 11/07/2010

@author: Rondon
'''

class Cordinator(object):
    '''
    classdocs
    '''
    passive = 0
    active = 1

    _stateList = ()
    _mode = passive

    def __init__(self):
        '''
        Constructor
        '''
        
    def setActive(self):
        _mode = self.active
        
    def setPassive(self):
        _mode = self.passive
        
    def heartbeat(self):
        pass
    
    def _messageToState(self, message):
        pass
    
        
        
        