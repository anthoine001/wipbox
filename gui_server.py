#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from tkinter import  *
except:
    from Tkinter import  *
import sqlite3 
from tkinter.messagebox import *
from datetime import datetime
import time



class ServerGui():
    def __init__(self):
        #Definition de la taille de l ecran
        self.root = Tk()
        self.largeur = self.root.winfo_screenwidth()-10
        self.hauteur = self.root.winfo_screenheight()-10

        #initialisation de la fenetre
        self.root.title("WIPBOX by NTN CREZANCY - Instant Vizualisation Of WIP in the Tooling Workshop")
        self.root.resizable(0,0)
        #initialisation du menu
        menubar = Menu(self.root)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Inialiser une machine", command=self.initMachine)
        menu1.add_command(label="Editer", command=self.alert)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Configuration", menu=menu1)

        menu2 = Menu(menubar, tearoff=0)
        menu2.add_command(label="Couper", command=self.alert)
        menu2.add_command(label="Copier", command=self.alert)
        menu2.add_command(label="Coller", command=self.alert)
        menubar.add_cascade(label="Aide", menu=menu2)
        self.root.config(menu=menubar)

        print (self.largeur) 
        print (self.hauteur)
        self.canvas = Canvas(self.root, width = self.largeur-6, height = self.hauteur-46, background = 'black')
        self.canvas.pack()

        self.label = Label(text="test", fg = 'yellow')
        self.label.pack(side="bottom")
        
        #timer
        self.update_timer()

        #loop principale
        self.root.mainloop()
        
    def alert(self):
        showinfo("alerte", "Bravo!")

    def initMachine(self) :
        def saveConfigMachine() :
            print("saveConfigMachine")
            db = sqlite3.connect('wipOutillage.db')
            cursor = db.cursor()
            maintenant =str(datetime.now())
            #for e in entries:
            #    i=0
            #    print(e.get())
            cursor.execute("UPDATE etat SET niveau = ?, moment = ? WHERE machine = ?",(entries[0].get(),maintenant,"K3X8--"))
            db.commit()
            db.close()
            
        dialogueConfigMachine = Tk()
        dialogueConfigMachine.title("Entrez la valeur des wip")
        db = sqlite3.connect('wipOutillage.db')
        cursor = db.cursor()
        cursor.execute("""SELECT count(machine) FROM etat""")
        nbMachines = cursor.fetchone()
        nb=int(nbMachines[0])
        cursor.execute("""SELECT machine, niveau, moment, alerte FROM etat""")
        donnees = cursor.fetchall()
        i=0
        entries =[]
        for line in donnees:
            l = Label(dialogueConfigMachine, text=line[0], width=10)
            e = Entry(dialogueConfigMachine, width=10)
            l.grid(row=i, column=0)
            e.grid(row=i, column=1)
            entries.append(e)
            i=i+1
        db.close
        b1 = Button(dialogueConfigMachine, text='Valider', command=saveConfigMachine)
        b1.grid(row=i, column=0)
        b2 = Button(dialogueConfigMachine, text='Annuler', command=dialogueConfigMachine.destroy)
        b2.grid(row=i, column=1)
        dialogueConfigMachine.mainloop()


        
        
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
            self.canvas.create_image(260, 80, anchor=NW, image=self.photo)
            print("load img ok")
        except:
            print ("load img fail")



s = ServerGui()


