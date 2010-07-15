# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

from message import Message
from messenger import Messenger
from consts import Consts
from threading import Timer
from state import State

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
    active_timer = None
    passive_timer = None
        
    def setActive(self):
        self._mode = self.ACTIVE
        if self.id == Consts.SERVER_NAME:
            self.setActiveTimer()
        
    def setActiveTimer(self):
        if self.active_timer != None: 
            self.active_timer.cancel()
            del self.active_timer
        self.active_timer = Timer(Consts.TIMEOUT_ACTIVE,self.heartbeat)
        self.active_timer.start()
        
    def setPassiveTimer(self):
        if self.passive_timer != None: 
            self.passive_timer.cancel()
            del self.passive_timer
        self.passive_timer = Timer(Consts.TIMEOUT_PASSIVE,self.assumeControl)
        self.passive_timer.start()
        
    def setPassive(self):
        self._mode = self.PASSIVE
        self.setPassiveTimer()
    
    def assumeControl(self):
        print '|--------------------------|'
        print '|   Assumindo o controle!  |'
        print '|--------------------------|'
        self.passive_timer.cancel()        
        self.setActive()
    
    def heartbeat(self):
        #print 'Enviando heartbeat'
        state = State()
        self.messenger.send(self.id, str(state),Message.STATE_MESSAGE)
        self.setActiveTimer()
    
    def refreshState(self, state):
        """
        Salva o estado na lista de states
        """
        
        
        if not state.isEmpty():       
            stateListAux = []
            for s in self.stateList:
                if s != None:
                    if s.message.sender != state.message.sender:
                        stateListAux.append(s)
            
            #if len(stateListAux) == len(self.stateList):
                #print 'Estado de Cliente novo detectado'
            
            stateListAux.append(state)
            self.stateList = stateListAux                
            #print 'State inserido na lista'
        #else:
            #print 'Mensagem era um heartbeat'
        #zerar o timer do passivo, aqui
        
    def sendState(self, message):
        """            
        Como vamos salvar o estado, logo em seguida, resetamos o timer para evitar
        o envio de um State nulo.
        """
        if self.id == Consts.SERVER_NAME and self._mode == self.ACTIVE:
            self.setActiveTimer()            
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
                #print '    LISTA DE ESTADOS'
                #for stt in self.stateList:
                    #print '       ' + str(stt)
                #print 'Enviando State do sendState: ' + str(state)
                self.messenger.send(self.id, str(state),Message.STATE_MESSAGE)          
                #self.messenger.receiveAck()
    
    def stateListToClientList(self):
        clientList = {}
        for state in self.stateList:
            clientList[state.message.sender] = int(state.data)
        #print clientList
        return clientList
    
    def processMessage(self, message):
        if message.receiver != self.id:
            #print 'Msg não era para mim!'
            return self.messenger.receive()
                
        if message.msg_type == Message.STATE_MESSAGE:
            """
            A maquina passiva recebe um estado.
            """
            #print 'Processando uma mensagem STATE'
            
            if self._mode == self.ACTIVE: 
                #print 'Ignorando STATE enviado'
                return self.messenger.receive()
                        
            #print 'Recebido msg: ' + str(message)
            #if message.data == 'None' or int(message.data) == 0: # As vezes retorna o heartbeat como 0 ou como None
            #    print 'Recebido heartbeat'
            #else:
            state = self.messenger.stringToState(message.data)
            print 'Salvando estado do cliente: ' + str(state.message.sender) + '    acumulador = ' + str(state.data)
            #print 'state convertido:' + str(state)
            self.refreshState(state)
            
            #Reinicia o contador para assumir o controle:
            self.setPassiveTimer()            
            
            #print '    LISTA DE ESTADOS'
            #for stt in self.stateList:
                #print '       ' + str(stt)
            
            """
            Envia msg de ACK
            """
            #print 'Enviando ACK para a máquina ativa'
            self.messenger.send(self.id, str(None),Message.ACK_MESSAGE)
            
            return self.messenger.receive() #volta a escutar
            
        elif message.msg_type == Message.NORMAL_MESSAGE:
            """
            A máquina ativa ou passiva receberam uma mensagem
            """
            #print 'Processando mensagem NORMAL'
            
            if self._mode == self.PASSIVE:
                #A máquina passiva recebe mensagens, mas as ignora.
                #print 'Ignorando mensagem'                        
                return self.messenger.receive() #volta a escutar
            
            #Descobrir se o número de seq já existe
            for stt in self.stateList:
                if message.sender == stt.message.sender: 
                    if message.sequence <= stt.message.sequence:
                        self.messenger.send(message.sender, str(message),Message.NORMAL_MESSAGE)
                        print 'Duplicata'
                        return self.messenger.receive() #volta a escutar
                                
        elif message.msg_type == Message.ACK_MESSAGE:
            #print 'Processando uma mensagem ACK'            
            if self._mode == self.ACTIVE:
                #print 'Recebi ACK da passiva'
                pass
            else:
                #zerar contador do reenvio do principal
                #print 'Ignorando ACK enviado'
                pass            
            return self.messenger.receive() #volta a escutar
        else:    
            raise Exception("Tipo de mensagem desconhecido: " + message.msg_type)
        
        return message
    