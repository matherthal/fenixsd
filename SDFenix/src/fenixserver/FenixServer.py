#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf-8
# mcsrv.py 20080524 AF

import sys, struct, socket
from copy import copy

class State(object):
    def __init__(self, acumul):
	self.acumul = acumul

def saveState(state):
    fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fd.sendto(state, (addr, port)) 

def mcast_server(addr, port):
    acumul = 0
    
    fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind udp port
    fd.bind(('', port))

    # set mcast group
    mreq = struct.pack('4sl', socket.inet_aton(addr), socket.INADDR_ANY)
    fd.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    try:
	acumulOld = -1
	portACK = 1906
        while 1:
            data, addr = fd.recvfrom(1024)
	    #print 'Recebido %s bytes de %s - mensagem: %s' % (len(data), addr, data)
	    print 'Recebido: ' + str(data)
	    acumul += int(data)
	    if acumulOld >= acumul:
		print 'acumulOld = ' + str(acumulOld)
		print 'ERRO DE SEQ'
	    acumulOld = acumul
	    #state = State(acumul)
	    #saveState(acumul)
	    print 'Acumulador = ' + str(acumul)
	    #if isinstance(data, State):
		#print 'Salvando estado...'
		#serverState = data
	    #else:
		#print 'Mensagem desconhecida: ' + str(data)
	    
	    #ACK	    
	    #fd.sendto(str(acumul), (addr, portACK)) 
	    
	    print ''
		
    except KeyboardInterrupt:
        print 'done'
        sys.exit(0)

if __name__ == '__main__':
    try:
        addr = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError:
        addr = '225.0.0.1'
        port = 1905
    finally:
        print 'Servidor rodando em %s:%d\n' % (addr, port)
        mcast_server(addr, port)