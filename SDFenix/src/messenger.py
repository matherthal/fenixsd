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
from coordinator import Coordinator

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
    #multicast_group = '225.0.0.1'
    timeout = 3 #timeout em segundos
    
    msgStr = None
    dest = None
    msg = None
    
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
        msgStr = message     
        self.msg = Message(sender=self.coordinator.id, \
                      receiver=destination,\
                      sequence=0, \
                      msg_type=Message.NORMAL_MESSAGE, \
                      data=message)
        
        if destination in Consts.SERVER_NAMES:
            multicast = Consts.SERVER_MULTICAST_GROUP
        elif destination in Consts.CLIENT_NAMES:
            multicast = Consts.CLIENT_MULTICAST_GROUP
        else:
            raise Exception('Destino desconhecido: ' + destination)
        
        """
        Aqui vai entrar o temporizador, e tratar o reenvio de mensagens.
        """
        
        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.sendto(str(self.msg), (multicast, self.port))
        fd.close()        
    
    def receive(self):               
        '''
        Retorna (mensagem, origem) quando a mensagem chega dentro do timeout
        E retornar um erro quando o timeout chega ao fim
        '''
        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        if self.msg != None and self.msg.msg_type == self.msg.REPLY:
            fd.settimeout(.5)
                
        # bind udp port
        fd.bind(('', self.port))
    
        # set mcast group
        mreq = struct.pack('4sl', socket.inet_aton(Consts.SERVER_MULTICAST_GROUP), socket.INADDR_ANY)
        fd.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        #Definir o tempo de timeout
        fd.settimeout(self.timeout)
        
        try:
            data, addr = fd.recvfrom(1024)
        except:
            #if Coordinator._mode == Coordinator.ACTIVE:
            self.send(self.dest, self.msg)
            self.receive()   
            #else: #Se a maquina for de backup, quando o timeout estoura, deve assumir o papel de coordenador
            #    Coordinator.setActive(self)
        
        msg = self.stringToMessage(data)        
        self.coordinator.processMessage(msg)        
        return msg.data, msg.sender 