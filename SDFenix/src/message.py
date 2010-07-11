# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

class Message(object):
    '''
    classdocs
    '''
    #não entendi para que servem
    PEDIDO = 0
    RESPOSTA = 1
    
    #Tipos de mensagem
    NORMAL_MESSAGE = 0 #a mensagem deve ser repassada para a aplicação
    STATE_MESSAGE = 1  #a mensagem carrega um State em data
    

    def __init__(self, sender, receiver, sequence, type, data):
        '''
        Constructor
        '''
        self.sender = sender
        self.receiver = receiver
        self.sequence = sequence
        self.type = type
        self.data = data