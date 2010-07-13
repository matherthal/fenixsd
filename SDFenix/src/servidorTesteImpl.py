'''
Created on 12/07/2010

@author: Douglas
'''

from messenger import Messenger
import coordinator

class Servidor(object):
    '''
    classdocs
    '''
    

    def __init__(self, params):
        '''
        Constructor
        '''
        
    def main(self):
        clientList = {}
        messenger = Messenger()            
        coordinator = coordinator.Coordinator()
        coordinator.init_FenixSD(messenger, coordinator)
        
        while(True):            
            data, client = messenger.receive()
            if not (client in clientList):
                clientList[client] = data
            else:
                clientList[client] += data
            messenger.send(client, clientList[client])
