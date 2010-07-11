# -*- coding: utf-8 -*-
'''
Created on 11/07/2010

@author: Rondon
'''

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
        
    def _insertHeader(self, data):
        raise NotImplementedError
    
    def _removeHeader(self, message):
        raise NotImplementedError
    
    def send(self, message):
        raise NotImplementedError
    
    def receive(self):
        raise NotImplementedError