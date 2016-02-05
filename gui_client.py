
#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
try:
    from tkinter import  *
except:
    from Tkinter import  *
import socket
import argparse


parser = argparse.ArgumentParser(description='wipbox client')
parser.add_argument('--ip', nargs=1, help='adresse ip')
parser.add_argument('--port', type=int, help='numero de port')
parser.add_argument('--stock', type=int, help='stock')
parser.add_argument('--nom', type=str, help='nom de la machine')
args = parser.parse_args()

serveur_ip = ""
if(args.ip is not None):
    serveur_ip = args.ip[0]
serveur_port = 1111
if(args.port is not None):
    serveur_port = args.port
stock=10
if(args.stock is not None):
    stock = args.stock

print "adress " + serveur_ip + "[" + str(serveur_port) + "]" 


#Definition de la taille de l ecran et du stock
root = Tk()
limite=4
largeur =root.winfo_screenwidth()
hauteur=root.winfo_screenheight()
taille=largeur/(stock+1)
niveau =0
root.destroy()

#initialisation de la fenetre
fenetre = Tk()
fenetre.title('K3X8')
fenetre.resizable(0,0)
canvas = Canvas(fenetre, width=largeur, height=hauteur, background='black')
try:
    photo = PhotoImage(file="ntn.jpeg")
    canvas.create_image(0, 0, anchor=NW, image=photo)
except:
    print "load img fail"
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


def send_niveau(niveau):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serveur_ip, serveur_port))
    s.send(args.nom + " niveau " + str(niveau))

#Detection du clic, de la position et positionnement d'un symbole
def touche(event):
    if hauteur/2-taille/2<event.y<hauteur/2+taille/2:
        # Capturer la case qui a ete cliquee
        k=int(event.x/taille)
        print(k)
        canvas.coords(marqueur,taille*k,hauteur/2+taille*0.5,taille*(k+1),hauteur/2+taille*1.5)
        niveau=k
        send_niveau(niveau)
canvas.bind("<Button-1>", touche)
fenetre.mainloop()
