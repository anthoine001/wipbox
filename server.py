#!/usr/bin/env python
# coding: utf-8 

import socket
import threading
from datetime import datetime
import sqlite3


port = 1111
listeMachines = ['K3X8--','K2X8--','CX7---','KX10--']
listeNiveaux = [0,0,0,0]
file_save = "toto.txt"

def ranger(texte,valeur):
    for i in range(len(listeMachines)):
        if listeMachines[i]==texte:
            listeNiveaux[i]=valeur

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def run(self): 
   
        print("Connection de %s %s" % (self.ip, self.port, ))
        maintenant =str(datetime.now())
        r = self.clientsocket.recv(2048)
        r2 =  maintenant + "; " + r
        print (r)

        file = open(file_save, 'a')
        file.write(r2 + "\n")
        file.close()
        machine = r[0:6]
        niveau = r[6]
        ranger(machine,niveau)
        #rangement dans la base SQLite
        db = sqlite3.connect('wipOutillage.db')
        cursor = db.cursor()
        cursor.execute("UPDATE etat SET niveau = niveau WHERE machine = machine")
        #cursor.execute("UPDATE etat SET moment = maintenant  WHERE machine = machine")
        db.commit()
        db.close()
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

