#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
try:
    from tkinter import  *
except:
     from Tkinter import  *

fenetre = Tk()
#fenetre.attributes('-fullscreen', 1)
fenetre.attributes('-topmost', 1)

label = Label(fenetre, text="Hello World")
label.pack()

bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.pack()

fenetre.mainloop()
