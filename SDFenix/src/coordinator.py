# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

from message import Message
from messenger import Messenger
from consts import Consts
from threading import Timer

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
    stateList = []
    _mode = PASSIVE #indefinido inicialmentes
    id = None #id da máquina
    state_timer = None
        
    def setActive(self):
        self._mode = self.ACTIVE
        self.setStateTimer()
        
    def setStateTimer(self):
        if self.state_timer != None: 
            self.state_timer.cancel()
        self.state_timer = Timer(Consts.TIMEOUT_STATE,self.heartbeat)
        self.state_timer.start()
        
    def setPassive(self):
        self._mode = self.PASSIVE
        
    def heartbeat(self):
        print 'Enviando heartbeat'   
        self.messenger.send(self.id, str(None),Message.STATE_MESSAGE)
        self.setStateTimer()
    
    def refreshState(self, state):
        """
        Salva o estado na lista de states
        """
        if state != None:                       
            stateListAux = []
            for s in self.stateList:
                if s != None:
                    if s.message.sender != state.message.sender:
                        stateListAux.append(s)
            
            if len(stateListAux) == len(self.stateList):
                print 'Estado de Cliente novo detectado'
            
            stateListAux.append(state)
            self.stateList = stateListAux
        else:
            print 'Mensagem era um heartbeat'
        #zerar o timer do passivo, aqui
    
    
    def processMessage(self, message):
        if message.msg_type == Message.STATE_MESSAGE:
            """
            A maquina passiva recebe um estado.
            Não interessa a máquina ativa receber um estado.
            """
            print 'Processando uma mensagem STATE'
            
            if self._mode == self.ACTIVE: 
                print 'Ignorando salvamento de estado'
                return self.messenger.receive()
            
            print 'Recebido msg: ' + str(message)
            state = self.messenger.stringToState(message.data)
            self.refreshState(state)
            
            """
            Envia msg de ACK
            """
            print 'Enviando ACK para a máquina ativa'
            self.messenger.send(self.id, str(None),Message.ACK_MESSAGE)
            
            return self.messenger.receive() #volta a escutar
            
        elif message.msg_type == Message.NORMAL_MESSAGE:
            """
            A máquina ativa ou passiva receberam uma mensagem
            """
            print 'Processando mensagem NORMAL'            
            
            if self._mode == self.PASSIVE:                
                #A máquina passiva recebe mensagens, mas as ignora.
                print 'Ignorando mensagem'                        
                return self.messenger.receive() #volta a escutar
            
            """            
            Como vamos salvar o estado, logo em seguida, resetamos o timer para evitar
            o envio de um State nulo.
            """      
            self.setStateTimer()
            
            """
            Para salvar o estado, temos que procurar o id do cliente correspondente.
            """
            state = None
            for s in self.stateList:
                if s != None:
                    if s.message.sender == message.sender:
                        state = s
                        break            
            
            if state != None:
                """
                Devemos enviar o estado mais atual do cliente agora, antes de processar.            
                """
                print 'Enviando State: ' + str(state)
                self.messenger.send(self.id, str(state),type=Message.STATE_MESSAGE)
                #esperar o ACK aqui?
            
        elif message.msg_type == Message.ACK_MESSAGE:
            print 'Processando uma mensagem ACK'          
            #zerar contador do reenvio do principal
            return self.messenger.receive() #volta a escutar
        else:    
            raise Exception("Tipo de mensagem desconhecido: " + message.msg_type)
        
        return message

