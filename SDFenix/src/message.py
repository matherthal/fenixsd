# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

from state import State

class Message(object):
    '''
    classdocs
    '''
    
    #Tipos de mensagem
    NORMAL_MESSAGE = 0 #a mensagem deve ser repassada para a aplicação
    STATE_MESSAGE = 1  #a mensagem carrega um State em data
    ACK_MESSAGE = 2 #mensagem de confirmação de recebimento de um State vindo do servidor Principal para o Secundário
    
    def __init__(self, sender='', receiver='', sequence=-1, msg_type=-1, data=''):
        '''
        Constructor
        '''
        self.sender = sender
        self.receiver = receiver
        self.sequence = sequence
        self.msg_type = msg_type
        self.data = data
        
    def __str__(self):
        return str(self.msg_type) + ' ' + str(self.sender) + ' ' + str(self.receiver) + ' ' + str(self.sequence) + ' ' + str(self.data)