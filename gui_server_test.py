#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from tkinter import  *
except:
    from Tkinter import  *
import sqlite3 


import time



class ServerGui():
    def __init__(self):
        #Definition de la taille de l ecran
        self.root = Tk()
        self.largeur = self.root.winfo_screenwidth()
        self.hauteur = self.root.winfo_screenheight()

        #initialisation de la fenetre
        self.root.title("WIPBOX by NTN CREZANCY - Instant Vizualisation Of WIP in the Tooling Workshop")
        self.root.resizable(0,0)
        
        print self.largeur 
        print self.hauteur
        canvas = Canvas(self.root, width = self.largeur-6, height = self.hauteur-200, background = 'black')
        canvas.pack()

        self.label = Label(text="")
        self.label.pack()
        
        #timer
        self.update_timer()

        #loop principale
        self.root.mainloop()

    #rafrachissement toutes les 1000 ms
    def update_timer(self):
        self.update_clock();
        #self.update_canvas();
        self.root.after(1000, self.update_timer)

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        
    def update_canvas(self):
        print "anthoine il faut coder!!!"
        #ton code ici
        



s = ServerGui()

#db = sqlite3.connect('wipOutillage.db')
#cursor = db.cursor()
#cursor.execute("""SELECT machine, niveau, moment, alerte FROM etat""")
#rows = cursor.fetchall()
#i=0
#for row in rows:
#    print('{0} - {1} - {2} - {3}'.format(row[0], row[1], row[2], row[3]))
#    txt = canvas.create_text(75, 60+i*hauteur/10, text=row[0], font="Arial 16 italic", fill="white")
#    txt2 = canvas.create_text(125, 60+i*hauteur/10, text=row[1], font="Arial 16 italic", fill="yellow")
#    i=i+1
#db.close
#canvas.delete("all")

