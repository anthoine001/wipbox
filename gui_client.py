#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
try:
    from tkinter import  *
except:
    from Tkinter import  *


#Définition de la taille de l ecran et du stock
stock=10
limite=4
largeur =800
hauteur=600
taille=largeur/(stock+1)
niveau =0

#initialisation de la fenêtre
fenetre = Tk()
fenetre.title('K3X8')
fenetre.resizable(0,0)
canvas = Canvas(fenetre, width=largeur, height=hauteur, background='black')
photo = PhotoImage(file="ntn.jpeg")
canvas.create_image(0, 0, anchor=NW, image=photo)
k=niveau
marqueur=canvas.create_oval(taille*k,hauteur/2+taille*0.5,taille*(k+1),hauteur/2+taille*1.5,fill='yellow')

#dessin du tableau
i=0
for i in range(stock+1):
    if i<limite:
        couleur='green'
    elif i==limite:
        couleur='orange'
    elif i>limite:
        couleur='red'
    canvas.create_rectangle(taille*i,hauteur/2-taille/2,taille*(i+1),hauteur/2+taille/2, fill=couleur,outline='white')
    canvas.create_text(taille*(0.5+i),hauteur/2,justify=CENTER,text=i,font="arial 18 bold")
canvas.pack()

#Détection du clic, de la position et positionnement d'un symbole
def touche(event):
    if hauteur/2-taille/2<event.y<hauteur/2+taille/2:
        # Capturer la case qui a été cliquée
        k=int(event.x/taille)
        print(k)
        canvas.coords(marqueur,taille*k,hauteur/2+taille*0.5,taille*(k+1),hauteur/2+taille*1.5)
        niveau=k
canvas.bind("<Button-1>", touche)
fenetre.mainloop()
