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
        for state in self.coordinator._stateList:
            if state.message.sender == id:
                return state.message.sequence + 1
        return 0 
    
    def stringToState(self, string):
        """
        Campos do state:
        Message Data
        """
        
        fields = string.split()
        
        state = State()
        state.message = self.stringToMessage(fields[0])
        state.data = fields[1]
        
    def resend(self):
        print 'resend'      
    
    def send(self, destination, message, type=Message.NORMAL_MESSAGE):
        if destination != None and message != None:          
            
            msg = Message(sender=self.coordinator.id, \
                          receiver=destination,\
                          sequence=self.next_sequence, \
                          msg_type=type, \
                          data=message)
            
            
            multicast = Consts.GROUPS[destination]
            if multicast == None:
                raise Exception('Destino desconhecido: ' + str(destination))
            
            fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            fd.sendto(str(msg), (multicast, self.port))
            fd.close()
        else:
            raise Exception('destino ou mensagem são nulos')
    
    def receive(self):               
        '''
        Retorna (mensagem, origem) quando a mensagem chega dentro do timeout
        E retornar um erro quando o timeout chega ao fim
        '''
        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
        # bind udp port
        fd.bind(('', self.port))
        
        multicast = Consts.GROUPS[self.coordinator.id]
        if multicast == None:
            raise Exception('ID da maquina nao pertence a nenhum grupo multicast: ' + self.coordinator.id)
        mreq = struct.pack('4sl', socket.inet_aton(multicast), socket.INADDR_ANY)
                
        fd.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)                        
        
        data, addr = fd.recvfrom(1024)        
                    
        msg_rec = self.stringToMessage(data)
        
        
        #return msg_rec.data, msg_rec.sender
        return self.coordinator.processMessage(msg_rec)           
            
    def prepare(self):
        self.next_sequence += 1
        print 'NextSequence = ' + str(self.next_sequence)
        