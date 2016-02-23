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
        
        print (self.largeur) 
        print (self.hauteur)
        self.canvas = Canvas(self.root, width = self.largeur-6, height = self.hauteur-66, background = 'black')
        self.canvas.pack()

        self.label = Label(text="test", fg = 'yellow')
        self.label.pack()
        
        #timer
        self.update_timer()

        #loop principale
        self.root.mainloop()

    #rafrachissement toutes les 1000 ms
    def update_timer(self):
        self.update_clock();
        self.update_canvas();
        self.root.after(1000, self.update_timer)

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        
    def update_canvas(self):
        
        self.canvas.delete('all')
        db = sqlite3.connect('wipOutillage.db')
        cursor = db.cursor()
        cursor.execute("""SELECT count(machine) FROM etat""")
        nbMachines = cursor.fetchone()
        nb=int(nbMachines[0])
        print(nb)
        cursor.execute("""SELECT machine, niveau, moment, alerte FROM etat""")
        rows = cursor.fetchall()
        i=0.5
        for row in rows:
            print('{0} - {1} - {2} - {3}'.format(row[0], row[1], row[2], row[3]))
            txt = self.canvas.create_text(75, i*self.hauteur/(nb+1), text=row[0], font="Arial 16 italic", fill="white")
            txt2 = self.canvas.create_text(125, i*self.hauteur/(nb+1), text=row[1], font="Arial 16 italic", fill="yellow")
            if row[3] > row[1]:
                self.canvas.create_rectangle(175-10, i*self.hauteur/(nb+1)-10,175+10, i*self.hauteur/(nb+1)+10,fill = 'green')
            elif row[3] == row[1]:
                self.canvas.create_rectangle(175-10, i*self.hauteur/(nb+1)-10,175+10, i*self.hauteur/(nb+1)+10,fill = 'orange')
            else:
                self.canvas.create_rectangle(175-10, i*self.hauteur/(nb+1)-10,175+10, i*self.hauteur/(nb+1)+10,fill = 'red')
            i=i+1
        db.close
        try:
            self.photo = PhotoImage(file="plan.gif")
            self.canvas.create_image(220, 10, anchor=NW, image=self.photo)
            print("load img ok")
        except:
            print ("load img fail")



s = ServerGui()


