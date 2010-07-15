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
        coord = coordinator.Coordinator()
        coord.id = 'Server'
        messenger = Messenger() 
        coordinator.init_FenixSD(messenger, coord)
        if not self.isPassive:
            coord.setActive()
        else:
            coord.setPassive()        
        
        clientList = {}        
        while(True):   
            print 'Esperando requisições...'                        
            message = messenger.receive()
            #print 'Servidor: recebi: ' + str(message)
            data, client = message.data, message.sender
            
            clientList = coord.stateListToClientList()
            #print 'Servidor: retornou o clientList: ' + str(clientList)
            
            if not (client in clientList):
                #print 'Servidor: novo cliente'
                clientList[client] = 0 #cria o cliente
                
            print 'Processando requisição do cliente '+ str(client)
            clientList[client] += int(data)   
            
            state = State()
            state.message = message                     
            state.data = clientList[client]
            #print 'Servidor: state: ' + str(state)
            
            coord.refreshState(state)
            print 'Salvando estado do cliente: ' + str(state.message.sender) + '    acumulador = ' + str(state.data)
            coord.sendState(message)
    
            print 'Enviando resposta para ' + str(client)
            messenger.send(client, str(clientList[client]))
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Parâmetros: a/p - ativo/passivo'
    else:
        servidor = Servidor(sys.argv[1] == 'p')
        servidor.start()