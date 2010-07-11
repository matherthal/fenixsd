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


    def __init__(self, id):
        '''
        Constructor
        '''
        self.lastSequence = 0
        self.id = id
        
    def strToState(self, str):
        if str.type != Message.STATE_MESSAGE:
            raise Exception('Tentativa de converter uma Mensagem que não é do tipo state')
        """
            A codificação de um State vai ser a seguinte:
            ID sequencia dados_da_aplicacao
        """
        fields = str.data.split()
        
        assert(len(fields) == 3)
        
        state = State(id=fields[0])
        state.lastSequence = fields[1]
        state.raw_data = fields[2] #espaço temporário para o concrete_state interpretar
        
        return state