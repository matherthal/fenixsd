# -*- coding: utf-8 -*-
'''
Created on 12/07/2010

@author: Douglas
'''

from messenger import Messenger
import coordinator

class Servidor(object):
    '''
    classdocs
    '''

    def __init__(self, isPassive):
        self.isPassive = isPassive
        
    def main(self):
        '''
        Inicialização de TF:
        '''        
        messenger = Messenger()            
        coordinator = coordinator.Coordinator()
        coordinator.init_FenixSD(messenger, coordinator)
        if not self.isPassive:
            coordinator.setActive()
        
        clientList = {}        
        while(True):
            print 'Servidor: esperando msgs...' 
            data, client = messenger.receive()
            if not (client in clientList):
                print 'Servidor: novo cliente'
                clientList[client] = 0 #cria o cliente
            
            print 'Servidor: processando requisição'
            clientList[client] += int(data)
            print 'Servidor: enviando resposta'
            messenger.send(client, clientList[client])
