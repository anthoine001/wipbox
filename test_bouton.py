#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
try:
    from tkinter import  *
except:
    from Tkinter import  *
def nombreBouton(event):
	a=int(s.get())
	i=0
	for i in range(a):
		Button(fenetre, text =i,height=5).pack(side=LEFT)

fenetre = Tk()
#s = Spinbox(fenetre, from_=0, to=10)
#s.pack()
#s.bind('<Button>', nombreBouton)

taille =8
orange =4
for i in range(taille):
		if i<orange:
			Button(fenetre, text =i,height=5,bg="green").pack(side=LEFT)
		elif i==orange:
			Button(fenetre, text =i,height=5,bg="orange").pack(side=LEFT)
		elif i>orange:
			Button(fenetre, text =i,height=5,bg="red").pack(side=LEFT)

fenetre.mainloop()
