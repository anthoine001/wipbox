
#!/usr/bin/env python
# -*- coding: utf-8 -*-


 
from Tkinter import *
 
def pointeur(event):
    chaine.configure(text = "Clic detecte en X =" + str(event.x) +", Y =" + str(event.y))
    print("Clic detecte en X =" + str(event.x) +", Y =" + str(event.y))
    coordx=(event.x)+6
    print coordx
fen = Tk()
cadre = Frame(fen, width =200, height =150, bg="light yellow")
cadre.bind("<Button-1>", pointeur)
cadre.pack()
chaine = Label(fen)
chaine.pack()
 
fen.mainloop()
