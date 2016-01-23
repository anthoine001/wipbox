#!/usr/bin/env python
# coding: utf-8 

import socket
import threading
from datetime import datetime

port = 1111

file_save = "toto.txt"


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def run(self): 
   
        print("Connection de %s %s" % (self.ip, self.port, ))

        r = str(datetime.now()) + ";" + self.clientsocket.recv(2048)
        print r

        file = open(file_save, 'a')
        file.write(r + "\n")
        file.close()
        print("Client déconnecté...")

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1111))

while True:
    tcpsock.listen(10)
    print( "En écoute... port " + str(port))
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()