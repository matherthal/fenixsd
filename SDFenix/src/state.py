# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

class State(object):
    '''
    Classe que mantém o estado entre a máquina em questão e uma outra. 
    Nesse sentido, o State mantém o estado de uma comunicação cliente-servidor.
    Sendo assim, é necessário guardar o id do cliente o qual está ocorrendo a 
    comunicação e o último número de sequência recebido (last_sequence).
    '''


    def __init__(self, id):
        '''
        Constructor
        '''
        self.lastSequence = 0
        self.id = id