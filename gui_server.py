# -*- coding: utf-8 -*-
try:
    from tkinter import  *
except:
    from Tkinter import  *

import sqlite3
import tkMessageBox
import datetime
#import numpy as np
#from cycler import cycler
import time
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#from matplotlib import style
import sqlite3
#style.use('fivethirtyeight')


class GuiServer:
    def __init__(self):
        self.fen = Tk()
        self.fen.title("WIPbox by NTN CREZANCY - Ecran de supervision")
        self.clickcount = -1
        self.newRotation = 1
        self.active = False
        self.tounga= True
        self.init_menu()
        self.init_background()
        self.init_machines()
        self.refresh()
        self.fen.mainloop()

    def init_menu(self):
        menubar = Menu(self.fen)
        self.menu1 = Menu(menubar, tearoff=0)
        self.menu2 = Menu(menubar, tearoff=0)
        self.menu1.add_command(label="Initialiser les machines", command=self.config)
        #self.menu2.add_command(label="Historique", command=self.graph_data)
        self.menu1.add_separator()
        self.menu1.add_command(label="Quitter", command=self.fen.destroy)
        menubar.add_cascade(label="Configuration", menu=self.menu1)
        #menubar.add_cascade(label="Analyse", menu=self.menu2)
        self.fen.config(menu=menubar)

        
    def init_background(self):
        self.largeur =self.fen.winfo_screenwidth()-10
        self.hauteur = self.fen.winfo_screenheight()-10 
        self.cadre= Canvas(self.fen, width =self.largeur, height =self.hauteur, bg="snow")
        self.cadre.create_rectangle(100,80,160,764,fill='gray',width=5)
        self.cadre.create_rectangle(1040,80,1100,764,fill='gray',width=5)
        self.cadre.create_rectangle(100,80,1100,140,fill='gray',width=5)
        self.cadre.create_rectangle(100,704,1100,764,fill='gray',width=5)
        self.cadre.create_rectangle(750,-5,810,764,fill='gray',width=5)
        self.cadre.create_rectangle(0,140,100,704,fill='light gray',width=5)
        self.cadre.create_rectangle(105,82.75,1095,137.5,fill='gray',width=0)
        self.cadre.create_rectangle(105,706.5,1090,762,fill='gray',width=0)
        self.cadre.create_rectangle(1042.5,82.5,1097.5,761.5,fill='gray',width=0)
        self.cadre.create_rectangle(102.5,82.5,157.5,761.5,fill='gray',width=0)
        #self.cadre.create_text(285,825, text= "3D")
        #self.cadre.create_text(380,830, text= "FORGES")
        self.cadre.create_oval(710,780,740,810,fill="red")
        self.cadre.create_text(770,800, text= "BUREAU")
        #self.cadre.create_text(380,40, text= "OUT.")
        self.cadre.pack(side="right")

    def database_connect(self):
        db = sqlite3.connect('wipOutillage.db')
        cursor = db.cursor()
        cursor.execute("SELECT machine_ID, coordx, coordy, threshold, level, rotation, unix FROM Machine")
        self.machines = cursor.fetchall()
        db.close()
        
    def init_machines(self):
        self.database_connect()
        for machine in self.machines:
            self.name = machine[0]
            self.x = int(machine[1])
            self.y = int(machine[2])
            threshold = machine[3]
            level = machine[4]
            rotation = int(machine[5])
            self.display_machinebox(rotation)
            self.display_boxcolor(threshold, level, rotation)
            self.cadre.create_text(self.x, self.y, text=self.name, tag="citron")
            self.display_level(level, rotation)

    def config(self):
        if tkMessageBox.askyesno('Reset machines', 'Etes vous sur de vouloir reset les machines?'):
            self.init_machine_change()
            
    def init_machine_change(self):
        self.tounga=False
        self.cadre.destroy()
        self.init_background()
        self.cadre.pack(side="right")
        
        self.clickcount= -1
        # programmation du comportement de la souris pendant le positionnement des machines
        self.cadre.bind("<Button-3>",self.rotate)
        self.cadre.bind("<Button-1>", self.pointeur)
        self.cadre.bind("<Motion>", self.position)


    def pointeur(self,event):
        self.active=True
        self.x = int(event.x)
        self.y = int(event.y)
        self.click_counter()

    def position(self,event):
        old_x=event.x
        old_y=event.y
        self.cursorbox(old_x,old_y)


    def cursorbox(self,old_x, old_y):
        machine2 = self.machines[self.clickcount+1]
        self.name2 = machine2[0]
        self.cadre.delete("pomelos")
        if self.newRotation == 1:
            
            self.cadre.create_rectangle(old_x - 30, old_y - 30, old_x + 80,old_y + 30, fill="linen", width=3, tag="pomelos")
            self.cadre.create_text(old_x, old_y, text=self.name2, tag="pomelos")
        else:
            self.cadre.create_rectangle(old_x - 30, old_y - 30, old_x + 30, old_y + 80, fill="linen", width=3, tag="pomelos")
            self.cadre.create_text(old_x, old_y, text=self.name2, tag="pomelos")
            
        
    def click_counter(self):
        if self.clickcount  < (len(self.machines) - 1):
                if self.active==True:
                        self.active=False
                        self.clickcount= self.clickcount+1
                        self.modify_machine_layout()
                        print ("nombre de click =" + str(self.clickcount + 1))
                        if self.clickcount == (len(self.machines) - 1):
                            self.confirm_machines()
                else:
                        return
        else :
            self.tounga=True
            self.refresh()

            
    def modify_machine_layout(self):
        machine = self.machines[self.clickcount]
        self.name = machine[0]
        threshold = machine[3]
        level = machine[4]
        rotation = self.newRotation
        self.display_machinebox(rotation)
        self.display_boxcolor(threshold, level,rotation)
        self.cadre.create_text(self.x, self.y, text=self.name, tag="citron")
        self.display_level(level,rotation)
        db = sqlite3.connect('wipOutillage.db')
        cursor = db.cursor()
        cursor.execute("UPDATE Machine SET coordx = ?, coordy = ?, rotation = ? WHERE machine_ID = ?", ( self.x, self.y, rotation, self.name))
        db.commit()
        db.close()
        
    def confirm_machines(self):
            if tkMessageBox.askyesno('valider', "l'emplacement des machines vous correspond ?"):
                self.tounga=True
                self.cadre.unbind("<Motion>")
                self.refresh()
            else:
                self.cadre.delete("citron")
                self.init_machine_change()

    def display_machinebox(self, rotation):
        if rotation == 1 :
            
            self.cadre.create_rectangle(self.x - 30, self.y - 30, self.x + 80, self.y + 30, fill="linen", width=3, tag="citron")
            
        else:
            self.cadre.create_rectangle(self.x - 30, self.y - 30, self.x + 30, self.y + 80, fill="linen", width=3, tag="citron")  
        
                            
    def display_level(self,level,rotation):
        if rotation == 1:
            self.cadre.create_text(self.x+60 , self.y, text=level, font="Arial 16 italic", fill="gray12", tag="citron")
        else:
            self.cadre.create_text(self.x , self.y+40, text=level, font="Arial 16 italic", fill="gray12", tag="citron") 

    def display_boxcolor(self, threshold, level, rotation):
        boxcolor = self.get_box_color(threshold, level)
        if rotation == 1:
            self.cadre.create_rectangle(self.x + 40, self.y+15, self.x + 80, self.y - 15, fill=boxcolor, width=3, tag="citron")
        else:
            self.cadre.create_rectangle(self.x -20, self.y+25, self.x + 20, self.y+55 , fill=boxcolor, width=3, tag="citron")   
        
    def get_box_color(self, threshold, level):
        if threshold > level:
            return 'lime green'
        elif threshold == level:
            return 'sandybrown'
        else:
            return 'indianred3'

    def refresh(self):
        if self.tounga ==True:
            self.cadre.delete("citron")
            print ("rafraichissement")
            self.database_connect()
            self.init_machines()
            self.fen.after(10000, self.refresh)
        else:
            return
        
    def rotate(self,event):
        self.newRotation=self.newRotation * -1
        
        

s = GuiServer()

