# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

class Message(object):
    '''
    classdocs
    '''
    PEDIDO = 0
    RESPOSTA = 1
    

    def __init__(self, sender, receiver, sequence, type, data):
        '''
        Constructor
        '''
        self.sender = sender
        self.receiver = receiver
        self.sequence = sequence
        self.type = type
        self.data = data