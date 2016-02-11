
#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from tkinter import  *
except:
    from Tkinter import  *
import sqlite3 

#Definition de la taille de l ecran et du stock
root = Tk()
largeur =root.winfo_screenwidth()
hauteur=root.winfo_screenheight()

#initialisation de la fenetre
root.title("WIPBOX by NTN CREZANCY - Instant Vizualisation Of WIP in the Tooling Workshop")
root.resizable(0,0)
canvas = Canvas(root, width=largeur-6, height=hauteur, background='black')
while True:
    db = sqlite3.connect('wipOutillage.db')
    cursor = db.cursor()
    cursor.execute("""SELECT machine, niveau, moment, alerte FROM etat""")
    rows = cursor.fetchall()
    i=0
    for row in rows:
        print('{0} - {1} - {2} - {3}'.format(row[0], row[1], row[2], row[3]))
        txt = canvas.create_text(75, 60+i*hauteur/10, text=row[0], font="Arial 16 italic", fill="white")
        txt2 = canvas.create_text(125, 60+i*hauteur/10, text=row[1], font="Arial 16 italic", fill="yellow")
        i=i+1
    db.close
    #canvas.delete("all")
    canvas.pack()
root.mainloop()