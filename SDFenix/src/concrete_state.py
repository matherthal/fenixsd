# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''
from state import State

class ConcreteState(State):
    '''
    Classe que implementa State, adicionando informações da aplicação. 
    No nosso caso, para o servidor acumulador, precisamos guardar 
    apenas accumulated_value.
    '''
    

    def __init__(self, id):
        '''
        Constructor
        '''
        State.__init__(self,id)
        self.accumulated_value = 0
        
    def strToState(self, str):
        state = State.strToState(self, str)
        concreteState = ConcreteState(state.id)
        concreteState.lastSequence = state.lastSequence
        concreteState.accumulated_value = int(state.raw_data) #interpreta o raw_data
        
        return state