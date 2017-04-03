# -*- coding: utf-8 -*-
try:
    from tkinter import  *
except:
    from Tkinter import  *

import sqlite3
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
        self.fen.title("GUI Server")
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
        self.menu2.add_command(label="Historique", command=self.graph_data)
        self.menu1.add_separator()
        self.menu1.add_command(label="Quitter", command=self.fen.destroy)
        menubar.add_cascade(label="Configuration", menu=self.menu1)
        menubar.add_cascade(label="Analyse", menu=self.menu2)
        self.fen.config(menu=menubar)

        
    def init_background(self):
        self.largeur =self.fen.winfo_screenwidth()-10
        self.hauteur = self.fen.winfo_screenheight()-10 
        self.cadre= Canvas(self.fen, width =self.largeur, height =self.hauteur, bg="snow")
        self.cadre.create_rectangle(100,80,160,764,fill='gray',width=5)
        self.cadre.create_rectangle(1040,80,1100,764,fill='gray',width=5)
        self.cadre.create_rectangle(100,80,1100,140,fill='gray',width=5)
        self.cadre.create_rectangle(100,704,1100,764,fill='gray',width=5)
        self.cadre.create_rectangle(220,764,360,900,fill='cornflower blue',width=5)
        self.cadre.create_rectangle(350,-5,410,900,fill='gray',width=5)
        self.cadre.create_line(310,120,380,190,width=35,fill='gray')
        self.cadre.create_line(290,120,360,190,width=5,fill='black')
        self.cadre.create_line(450,120,380,190,width=35,fill='gray')
        self.cadre.create_line(470,120,400,190,width=5,fill='black')
        self.cadre.create_line(380,654,450,724,width=35,fill='gray')
        self.cadre.create_line(400,654,470,724,width=5,fill='black')
        self.cadre.create_line(380,654,310,724,width=35,fill='gray')
        self.cadre.create_line(360,654,290,724,width=5,fill='black')
        self.cadre.create_rectangle(0,140,100,704,fill='light gray',width=5)
        self.cadre.create_rectangle(105,82.75,1095,137.5,fill='gray',width=0)
        self.cadre.create_rectangle(105,706.5,1090,762,fill='gray',width=0)
        self.cadre.create_rectangle(1042.5,82.5,1097.5,761.5,fill='gray',width=0)
        self.cadre.create_rectangle(102.5,82.5,157.5,761.5,fill='gray',width=0)
        self.cadre.create_rectangle(352.5,-5,407.5,897.5,fill='gray',width=0)
        self.cadre.create_text(285,825, text= "3D")
        self.cadre.create_text(380,830, text= "FORGES")
        self.cadre.create_text(380,20, text= "BUREAU")
        self.cadre.create_text(380,40, text= "OUT.")
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
        if askyesno('reset les machines', 'Etes vous sur de vouloir reset les machines?'):
            self.init_machine_change()
            
    def init_machine_change(self):
        self.tounga=False
        self.cadre.destroy()
        self.init_background()
        self.cadre.pack(side="right")
        
        self.clickcount= -1
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
        db = sqlite3.connect('wipOutillageYnnis.db')
        cursor = db.cursor()
        cursor.execute("UPDATE Machine SET coordx = ?, coordy = ?, rotation = ? WHERE machine_ID = ?", ( self.x, self.y, rotation, self.name))
        db.commit()
        db.close()
        
    def confirm_machines(self):
            if askyesno('valider', "l'emplacement des machines vous correspond ?"):
                self.tounga=True
                self.cadre.unbind("<Motion>")
                self.refresh()
            else:
                self.cadre.delete("citron")
                self.init_machines()

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
            print ("bybyby")
            self.database_connect()
            self.init_machines()
            self.fen.after(10000, self.refresh)
        else:
            return
        
    def rotate(self,event):
        self.newRotation=self.newRotation * -1
        
    def graph_data(self):
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='K2X8--'")
        data = c.fetchall()
        c.close()
        dates = []
        values = [] 
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='K3X8--'")
        data2 = c.fetchall()
        c.close()
        dates2 = []
        values2 = []
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='CX7---'")
        data3 = c.fetchall()
        c.close()
        dates3 = []
        values3 = []
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='KX10--'")
        data4 = c.fetchall()
        c.close()
        dates4 = []
        values4 = []
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='MAZAK1'")
        data5 = c.fetchall()
        c.close()
        dates5 = []
        values5 = []
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='MAZAK2'")
        data6 = c.fetchall()
        c.close()
        dates6 = []
        values6 = []
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='DANOBA'")
        data7 = c.fetchall()
        c.close()
        dates7= []
        values7 = []
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='ET2201'")
        data8 = c.fetchall()
        c.close()
        dates8 = []
        values8 = []
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='ET2202'")
        data9 = c.fetchall()
        c.close()
        dates9 = []
        values9 = []
        db = sqlite3.connect('wipHistoriqueYnnis.db')
        c=db.cursor()
        c.execute("SELECT unix, level, machine FROM histo WHERE machine='CAZENE'")
        data10 = c.fetchall()
        c.close()
        dates10 = []
        values10 = [] 
        
        for row in data:
            dates.append(datetime.datetime.fromtimestamp(row[0]))
            values.append(row[1])
        for row in data2:
            dates2.append(datetime.datetime.fromtimestamp(row[0]))
            values2.append(row[1])
        for row in data3:
            dates3.append(datetime.datetime.fromtimestamp(row[0]))
            values3.append(row[1])
        for row in data4:
            dates4.append(datetime.datetime.fromtimestamp(row[0]))
            values4.append(row[1])
        for row in data5:
            dates5.append(datetime.datetime.fromtimestamp(row[0]))
            values5.append(row[1])
        for row in data6:
            dates6.append(datetime.datetime.fromtimestamp(row[0]))
            values6.append(row[1])
        for row in data7:
            dates7.append(datetime.datetime.fromtimestamp(row[0]))
            values7.append(row[1])
        for row in data8:
            dates8.append(datetime.datetime.fromtimestamp(row[0]))
            values8.append(row[1])
        for row in data9:
            dates9.append(datetime.datetime.fromtimestamp(row[0]))
            values9.append(row[1])
        for row in data10:
            dates10.append(datetime.datetime.fromtimestamp(row[0]))
            values10.append(row[1])
        plt.subplot2grid((3,3),(0,0), colspan=2, rowspan=3)
        plt.rc('axes',prop_cycle=(cycler('color',['r','lightsalmon','navy','blue','cornflowerblue','mediumturquoise','mediumseagreen','forestgreen','gold','black']) +
                                  cycler('lw',[3,3,3,3,3,3,3,3,3,3])))
        plt.plot_date(dates,values,'-', label='K2X8')
        plt.plot_date(dates2,values2,'-',label='K3X8')
        plt.plot_date(dates3,values3,'-',label='CX7')
        plt.plot_date(dates4,values4,'-',label='KX10')
        plt.plot_date(dates5,values5,'-',label='MAZAK1')
        plt.plot_date(dates6,values6,'-',label='MAZAK2')
        plt.plot_date(dates7,values7,'-',label='DANOBA')
        plt.plot_date(dates8,values8,'-',label='ET2201')
        plt.plot_date(dates9,values9,'-',label='ET2202')
        plt.plot_date(dates10,values10,'-',label='CAZENE')
        fig = plt.gcf()
        fig.canvas.set_window_title('Historique des niveaux')
        plt.legend(bbox_to_anchor=(1.05,0.9),loc=2, borderaxespad=0.)
        plt.show()
        


s = GuiServer()

