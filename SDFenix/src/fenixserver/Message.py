'''
Created on 11/07/2010

@author: Rondon
'''
import fenixserver

class Message(object):
    '''
    classdocs
    '''
    PEDIDO = 0
    RESPOSTA = 1
    

    def __init__(self, sender, receiver, sequence, message_type, data):
        '''
        Constructor
        '''
        self.sender = sender
        self.receiver = receiver
        self.sequence = sequence
        self.msg_type = message_type
        self.data = data