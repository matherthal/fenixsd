# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

from message import Message
from messenger import Messenger

def init_FenixSD(messenger,coordinator):
    '''
    Função para fazer as classes se conhecerem
    '''
    
    messenger.coordinator = coordinator
    coordinator.messenger = messenger
    

class Coordinator(object):
    '''
    Classe estática (não em constructor).
    '''
    PASSIVE = 0
    ACTIVE = 1
    _stateList = []
    _mode = PASSIVE #indefinido inicialmentes
    id = None #id da máquina
    
        
    def setActive(self):
        self._mode = self.ACTIVE
        
    def setPassive(self):
        self._mode = self.PASSIVE
        
    def heartbeat(self):
        raise NotImplementedError
    
    def processMessage(self, message):
        if message.msg_type == Message.STATE_MESSAGE:
            print 'Processando uma mensagem STATE'
            
            state = Messenger.stringToState(message.data)

            """
            Tem que ser uma mensagem vindo do ATIVO
            """
            
            """
            Reiniciar o temporizador, já que recebeu um state
            """
            
            if state.data != None:                       
                stateListAux = []
                for s in self._stateList:
                    if s != None:
                        if s.id != state.id:
                            stateListAux.append(s)
                
                if len(stateListAux) == len(self._stateList):
                    'Estado de Cliente novo detectado'
                
                stateListAux.append(state)
                self._stateList = stateListAux                
                print 'State inserido na lista'
            else:
                print 'Mensagem era um heartbeat'
            
        elif message.msg_type == Message.NORMAL_MESSAGE:
            print "Mensagem do tipo normal =)"
        elif message.msg_type == Message.ACK_MESSAGE:
            print 'Processando uma mensagem ACK'          
            raise NotImplementedError
        else:    
            raise Exception("Tipo de mensagem desconhecido")
        
        