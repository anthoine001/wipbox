#!/usr/bin/env python
# coding: utf-8 

import socket
import threading
import datetime
import sqlite3
import time

port = 1111
listeMachines = ['K3X8--','K2X8--','CX7---','KX10--']
file_save = "histo.txt"

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))
        unix=time.time()
        maintenant =str(datetime.datetime.fromtimestamp(unix).strftime("%Y-%m-%d %H:%M:%S"))
        receivedData = self.clientsocket.recv(2048)
        DecodedData=receivedData.decode("utf-8")
        print (DecodedData)
        machine = str(DecodedData[0:6])
        print (machine)
        level = (DecodedData[6:7])
        threshold= (DecodedData [7:])
        print (threshold)
       
        print (level)
               
        #rangement dans la base SQLite wipOutillage
        db = sqlite3.connect('wipOutillageYnnis.db')
        cursor = db.cursor()
        cursor.execute("UPDATE Machine SET level = ?, unix = ?, datestamp = ?, threshold= ? WHERE machine_ID = ?",(level,unix,maintenant,threshold,machine))
        db.commit()
        db.close()
        
        #rangement dans la base SQLite wipHistorique
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO histo(machine, level, unix, datestamp,threshold) VALUES(?,?,?,?,?)",(machine , level , unix, maintenant,threshold))
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
    
