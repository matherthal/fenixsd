# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

class Coordinator(object):
    '''
    Classe estática (não em constructor).
    '''
    PASSIVE = 0
    ACTIVE = 1
    _stateList = ()
    _mode = None #indefinido inicialmentes
        
    def setActive(self):
        self._mode = self.ACTIVE
        
    def setPassive(self):
        self._mode = self.PASSIVE
        
    def heartbeat(self):
        raise NotImplementedError
    
    def processMessage(self, message):
        raise NotImplementedError