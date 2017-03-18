
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
#ATTENTION : nous allons coder les noms de machine sur 6 caracteres obligatoirement
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

print("adress " + serveur_ip + "[" + str(serveur_port) + "]" )


#Definition de la taille de l ecran et du stock
fenetre = Tk()

limite = input ("quelle est la limite de lot a ne pas depasser le seuil critique : ")
# ligne ci dessous ajoutee le 29 novembre 2016
limite = int(limite)
# 
largeur = fenetre.winfo_screenwidth()
hauteur = fenetre.winfo_screenheight()
taille = largeur/(stock+1)
niveau =0



#initialisation de la fenetre
fenetre.title(args.nom)
fenetre.resizable(0,0)
canvas = Canvas(fenetre, width=largeur, height=hauteur, background='black')
try:
    photo = PhotoImage(file="ntn.jpeg")
    canvas.create_image(0, 0, anchor=NW, image=photo)
except:
    print ("load img fail")
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
    print (niveau)
    codebyte=str(niveau).encode('ascii')
    nombyte=str(args.nom).encode('ascii')
    limitebyte = str(limite).encode('ascii')
    print (codebyte)
    print (nombyte)
    print (limitebyte)
    s.send((nombyte) + (codebyte) + (limitebyte))
    

#Detection du clic, de la position et positionnement d'un symbole
def touche(event):
    if hauteur/2-taille/2<event.y<hauteur/2+taille/2:
        # Capturer la case qui a ete cliquee
        k=int(event.x/taille)
        #print( k)
        canvas.coords(marqueur,taille*k,hauteur/2+taille*0.5,taille*(k+1),hauteur/2+taille*1.5)
        niveau=k
        send_niveau(niveau)
canvas.bind("<Button-1>", touche)
fenetre.mainloop()
