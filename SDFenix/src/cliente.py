# -*- coding: utf-8 -*-
'''
Created on Jul 12, 2010

@author: Giulio
'''

from messenger import Messenger
import coordinator
import sys
import random
import time

class Cliente(object):
    '''
    classdocs
    '''

    def __init__(self, isPassive):
        self.isPassive = isPassive
        self.serverID = 'Server'
        
    def start(self):
        '''
        Inicialização de TF:
        ''' 
        print 'Cliente: Inicializando...'       
        messenger = Messenger()            
        coord = coordinator.Coordinator()
        coordinator.init_FenixSD(messenger, coord)
        if not self.isPassive:
            coord.setActive()
            coord.id = 'Bob'
               
        while(True):
            print 'Cliente: enviando requisição'
            message = str(5)
            messenger.send(self.serverID, message)
            resp = messenger.receive()
            print 'Cliente: resposta = ' + resp
            time.sleep(int(random.random() * 5 + 1)) #espera de 1 a 5 segundos

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Parâmetros: a/p - ativo/passivo'
    else:
        cliente = Cliente(sys.argv[1] == 'p')
        cliente.start()