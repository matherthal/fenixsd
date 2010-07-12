'''
Created on 12/07/2010

@author: Douglas
'''

from cordinator import Cordinator
from messenger import Messenger


class Servidor (object):
    '''
    classdocs
    '''
    

    def __init__(selfparams):
        '''
        Constructor
        '''
        
    def main(self):
        clientList = {}
        messenger = Messenger()            
        cord = Cordinator()
        while(True):            
            data, client = messenger.receive()
            if not (client in clientList):
                clientList[client] = data
            else:
                clientList[client] += data
            messenger.send(client, clientList[client])
            
            
            
        
        
           