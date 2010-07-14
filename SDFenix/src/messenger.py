# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''
import sys, socket, struct

from message import Message
from state import State
import exceptions
from consts import Consts
from threading import Timer
from threading import Lock

class Messenger(object):
    '''
    Classe estática
    
    É a entidade que faz interface com o programador da aplicação. 
    Ele envia as mensagens com o send e receive, e por baixo dos panos, o Messenger 
    conversa com o Coordinator para saber o que fazer.
    Quando o programa da aplicação envia uma mensagem (que é uma String) através do 
    send, o Messenger precisa adicionar o header de tolerância a falhas na mensagem, 
    criando um objeto do tipo Message. Isso é feito através do método _insertHeader. 
    A operação inversa (transformar um Message em String) é feita pelo _removeHeader. 
    Além disso, para preencher essas informações, o Messenger precisa se comunicar 
    com o Coordinator para poder obter a última sequencia recebida de um cliente. 
    '''
    port = 1905    
    timeout = 5 #timeout em segundos
    next_sequence = 0
    resendList = [] #lista de mensagens a serem reenviadas
    send_mutex = Lock()
    resendList_mutex = Lock()
        
    def stringToMessage(self, string):
        """
        Campos da mensagem:
        Type Sender Receiver Sequence Data
        """ 
        fields = string.split() 
        
        return Message(sender=fields[1], \
                      receiver=fields[2], \
                      sequence=int(fields[3]), \
                      msg_type=int(fields[0]), \
                      data=fields[4])
        
    def messageToString(self, message):
        return str(message)
    
    def getNextSeq(self, id):
        for state in self.coordinator.stateList:
            if state.message.sender == id:
                return state.message.sequence + 1
        return 0 
    
    def stringToState(self, string):
        """
        Campos do state:
        Message Data
        """     
        
        fields = string.split()
        
        if len(fields) != 6:
            raise Exception('Impossivel converter para State: ' + string)
                
        state = State()
        state.message = self.stringToMessage(string)
        state.data = fields[6]
        return state
        
    def resend(self, msg):
        print 'Reenviando mensagem'
        
        multicast = Consts.GROUPS[msg.receiver]
        if multicast == None:
            raise Exception('Destino desconhecido: ' + str(msg.receiver))
        
        self.send_mutex.acquire()
        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.sendto(str(msg), (multicast, self.port))
        fd.close()
        self.send_mutex.release()
    
    def send(self, destination, message, type=Message.NORMAL_MESSAGE):
        if destination != None and message != None:          
            
            msg = Message(sender=self.coordinator.id, \
                          receiver=destination,\
                          sequence=self.next_sequence, \
                          msg_type=type, \
                          data=message)            
            
            if type == Message.NORMAL_MESSAGE: #o reenvio eh somente para msgs normais
                self.resendList_mutex.acquire()
                self.resendList.append(msg)
                self.resendList_mutex.release()
            
            multicast = Consts.GROUPS[destination]
            if multicast == None:
                raise Exception('Destino desconhecido: ' + str(destination))
            
            self.send_mutex.acquire()
            fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            fd.sendto(str(msg), (multicast, self.port))
            fd.close()
            self.send_mutex.release()
        else:
            raise Exception('destino ou mensagem são nulos')
    
    def receive(self, useTimeout=False):               
        '''
        Retorna (mensagem, origem) quando a mensagem chega dentro do timeout
        E retornar um erro quando o timeout chega ao fim
        '''
        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
        # bind udp port
        fd.bind(('', self.port))

        if useTimeout:
            fd.settimeout(self.timeout)
        
        multicast = Consts.GROUPS[self.coordinator.id]
        if multicast == None:
            raise Exception('ID da maquina nao pertence a nenhum grupo multicast: ' + str(self.coordinator.id))
        mreq = struct.pack('4sl', socket.inet_aton(multicast), socket.INADDR_ANY)                
        fd.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)                                
        try:
            data, addr = fd.recvfrom(1024)            
        except Exception as inst:
            if useTimeout: #timeout implica reenvio
                self.resendList_mutex.acquire()        
                msg = self.resendList[0] #pega o primeiro da "fila"
                self.resendList_mutex.release()
                fd.close()
                self.resend(msg)
                #parar depois de N tentativas (falta implementar)
                return self.receive(useTimeout)
            else: #saiu uma excessão e não estavamos no modo timetou
                raise inst #sobe a excessão
        finally:
            fd.close()
        
        if useTimeout: #timeout implica reenvio
            self.resendList_mutex.acquire()
            self.resendList.pop() #recebeu com sucesso, remove da lista
            self.resendList_mutex.release()
        
        msg_rec = self.stringToMessage(data)
        
        #return msg_rec.data, msg_rec.sender
        return self.coordinator.processMessage(msg_rec)           
            
    def prepare(self):
        self.next_sequence += 1
        print 'NextSequence = ' + str(self.next_sequence)
        