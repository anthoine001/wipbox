#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
try:
    from tkinter import  *
except:
    from Tkinter import  *

fenetre = Tk()

s = Spinbox(fenetre, from_=0, to=10)
s.pack()

Button(fenetre, text ='Bouton 1',height=50).pack(side=LEFT)
Button(fenetre, text ='Bouton 2',height=50).pack(side=LEFT)


fenetre.mainloop()
