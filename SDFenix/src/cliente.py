# -*- coding: utf-8 -*-
'''
Created on Jul 12, 2010

@author: Giulio
'''

from messenger import Messenger
from consts import Consts
import coordinator
import sys
import random
import time
from message import Message
from state import State

class Cliente(object):
    '''
    classdocs
    '''

    def __init__(self, isPassive):
        self.isPassive = isPassive
        self.serverID = 'Server'
        self.id = ''
        
    def start(self):
        '''
        Inicialização de TF:
        ''' 
        print 'Cliente: Inicializando...'       
        messenger = Messenger()            
        #coord = coordinator.Coordinator(Consts.CORDINATOR_TYPE[0])
        coord = coordinator.Coordinator()
        coordinator.init_FenixSD(messenger, coord)
        if not self.isPassive:
            coord.setActive()
        coord.id = self.id
        
        while(True):
            print 'Cliente: enviando requisição'
            message = str(5)
            """
            state = State()
            state.message = Message(sender=self.id, \
                                    receiver=self.serverID, \
                                    sequence=seq, \
                                    msg_type=message.REQUEST, \
                                    data=message)
            state.data = message
            coord.refreshState(state)
            """
            messenger.prepare()
            messenger.send(self.serverID, message)         
            
            print 'Cliente: esperando resposta...'
            message = messenger.receive(True)
            resp, id = message.data, message.sender
            print 'Cliente: resposta = ' + str(resp) + ' ' + str(id) 
            #time.sleep(int(random.random() * 5 + 1)) #espera de 1 a 5 segundos
            time.sleep(int(random.random() + 1)) #espera de 1 a 5 segundos
            

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Parâmetro 1: a/p - ativo/passivo'
        print 'Parâmetro 2: nome do cliente'
    else:
        cliente = Cliente(sys.argv[1] == 'p')
        cliente.id = sys.argv[2]
        cliente.start()