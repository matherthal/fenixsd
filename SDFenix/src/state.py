# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

from message import Message

class State(object):
    '''
    Classe que mantém o estado entre a máquina em questão e uma outra. 
    Nesse sentido, o State mantém o estado de uma comunicação cliente-servidor.
    Sendo assim, é necessário guardar o id do cliente o qual está ocorrendo a 
    comunicação e o último número de sequência recebido (last_sequence).
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.message = None
        self.data = None
    
    def __str__(self):
        return str(self.message) + ' ' + str(self.data)