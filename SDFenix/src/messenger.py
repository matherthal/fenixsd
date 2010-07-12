# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''
import sys, socket, struct

from message import Message

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
    multicast_group = None
    
    def _insertHeader(self, data):
        raise NotImplementedError
    
    def _removeHeader(self, message):
        raise NotImplementedError
    
    def send(self, destination, message):
        """
        Aqui não se deve enviar a mensagem diretamente, deve-se criar um objeto Message.
        Aqui vai entrar o temporizador, e tratar o reenvio de mensagens.
        """
        
        #next_sequence = 
        
        msg = Message(sender=self.coordinator.id, \
                      receiver=destination,sequence=0, \
                      msg_type=Message.NORMAL_MESSAGE, \
                      data=message)
        
        
        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.sendto(message, (destination, self.port))
        fd.close()
    
    def receive(self):
        raise NotImplementedError

        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
        # bind udp port
        fd.bind(('', self.port))
    
        # set mcast group
        mreq = struct.pack('4sl', socket.inet_aton(self.multicast_group), socket.INADDR_ANY)
        fd.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    