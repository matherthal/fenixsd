# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''
import sys, socket, struct

from message import Message
from state import State

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
    multicast_group = '225.0.0.1'
    
    def _insertHeader(self, data):
        raise NotImplementedError
    
    def _removeHeader(self, message):
        raise NotImplementedError
    
    def stringToMessage(self, string):
        """
        Campos da mensagem:
        Type Sender Receiver Sequence Data
        """ 
        fields = string.split() 
        
        return Message(sender=fields[1], \
                      receiver=fields[2],sequence=fields[3], \
                      msg_type=fields[0], \
                      data=fields[4])
        
    def messageToString(self, message):
        return str(message)
    
    def stringToState(self, string):
        """
        Campos do state:
        Message Data
        """
        
        fields = string.split()
        
        state = State()
        state.message = self.stringToMessage(fields[0])
        state.data = fields[1]        
    
    def send(self, destination, message):       
        msg = self.stringToMessage(message)
        raise NotImplementedError
        
        """        
        Aqui vai entrar o temporizador, e tratar o reenvio de mensagens.
        """
        
        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.sendto(message, (destination, self.port))
        fd.close()        
    
    def receive(self):

        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
        # bind udp port
        fd.bind(('', self.port))
    
        # set mcast group
        mreq = struct.pack('4sl', socket.inet_aton(self.multicast_group), socket.INADDR_ANY)
        fd.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        data, addr = fd.recvfrom(1024)
        
        msg = self.stringToMessage(data)
        
        self.coordinator.processMessage(msg)
        
        return msg.data, addr
    