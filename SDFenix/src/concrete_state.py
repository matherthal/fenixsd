# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''
from state import State

class ConcreteState(State):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.accumulated_value = 0