#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, socket

class State(object):
    def __init__(self, acumul):
        self.acumul = acumul

class Message:
    def __init__(self, seqNum, msgType, clientID, data):
        self.data
        self.seqNum
        self.msgType
        self.clientID

if __name__ == '__main__':
    try:
        addr = '225.0.0.1'
        port = 1905
        #state = State(32)        
        buff = sys.argv[1]
    except IndexError:
        print 'Use: %s + <valor>' % sys.argv[0]
        sys.exit(1)
        
    fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    fd.sendto(buff, (addr, port))
    #for i in range(100):
    #fd.sendto(str(i), (addr, port))    
    '''
    try:
	portACK = 1906
	fd.bind(('', portACK))
    except socket.error, err:
	print "Couldn't be a udp server on port %d : %s" % (port, err)
	raise SystemExit
    
    
    fd.sendto('1', (addr, port)) 
    #datagram = fd.recv(MAX_TO_READ)
    datagram = fd.recvfrom(portACK)
    print "ACK " + str(datagram)
    
    fd.sendto('3', (addr, port)) 
    #datagram = fd.recv(MAX_TO_READ)
    datagram = fd.recvfrom(portACK)
    print "ACK " + str(datagram)
    
    fd.sendto('2', (addr, port)) 
    #datagram = fd.recv(MAX_TO_READ)
    datagram = fd.recvfrom(portACK)
    print "ACK " + str(datagram)
    '''
    fd.close()