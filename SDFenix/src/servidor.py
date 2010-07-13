# -*- coding: utf-8 -*-
'''
Created on 12/07/2010

@author: Douglas
'''

from messenger import Messenger
import coordinator
import sys
from consts import Consts
from state import State
from message import Message 

class Servidor(object):
    '''
    classdocs
    '''

    def __init__(self, isPassive):
        self.isPassive = isPassive
        
    def start(self):
        '''
        Inicialização de TF:
        '''        

        const = Consts()           
        #coord = coordinator.Coordinator(const.CORDINATOR_TYPE[2])    
        coord = coordinator.Coordinator()
        messenger = Messenger() 
        coordinator.init_FenixSD(messenger, coord)
        if not self.isPassive:
            coord.setActive()
            coord.id = Consts.SERVER_NAMES[0]
        
        clientList = {}        
        while(True):            
            print 'Servidor: esperando requisições...'                        
            message = messenger.receive()
            data, client = message.data, message.sender
            if not (client in clientList):
                print 'Servidor: novo cliente'
                clientList[client] = 0 #cria o cliente
            
            print 'Servidor: processando requisição'
            clientList[client] += int(data)
            print 'Servidor: enviando resposta para ' + str(client)
            state = State()
            state.message = message
            state.data = clientList[client] 
            coord.refreshState(state)
            messenger.send(client, clientList[client])
            


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Parâmetros: a/p - ativo/passivo'
    else:
        servidor = Servidor(sys.argv[1] == 'p')
        servidor.start()