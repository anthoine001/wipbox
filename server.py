#!/usr/bin/env python
# coding: utf-8 

import socket
import threading
from datetime import datetime
from Tkinter import *
from threading import Thread

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

        r = self.clientsocket.recv(2048)
        r2 =  str(datetime.now()) + "; " + r
        print (r)

        file = open(file_save, 'a')
        file.write(r2 + "\n")
        file.close()
        machine = r[0:6]
        niveau = r[6]
        ranger(machine,niveau)
        print("Client déconnecté...")

class Afficheur(Thread):

    """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self,liste1,liste2):
        Thread.__init__(self)
        self.liste1 = liste1
        self.liste2 = liste2

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        print('demarre le thread affichage')
        fenetre = Tk()
        #threadLock.acquire()
        for i in range(len(self.liste1)):
            Button(fenetre, text=self.liste1[i], borderwidth=1).grid(row=1, column=i+1)
            Button(fenetre, text=self.liste2[i], borderwidth=1).grid(row=2, column=i+1)
        fenetre.mainloop()
        print('fin thread affichage')
       # threadLock.release()

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1111))
thread_1 = Afficheur(listeMachines,listeNiveaux)
while True:
    tcpsock.listen(10)
    print( "En écoute... port " + str(port))
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    thread_1.start()
    newthread.start()
   
    newthread.join()
    thread_1.join()

