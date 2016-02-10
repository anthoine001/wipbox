#!/usr/bin/env python
# coding: utf-8 

import sqlite3
from datetime import datetime

db = sqlite3.connect('wipOutillage.db')
cursor = db.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS etat(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     machine TEXT,
     niveau INTERGER,
     moment TEXT
)
""")

db.commit()
etat = []
maintenant = str(datetime.now())
etat.append(("K3X8--",0,maintenant))
etat.append(("K2X8--",0,maintenant))
etat.append(("CX7---",0,maintenant))
etat.append(("KX10--",0,maintenant))
etat.append(("MAZAK1",0,maintenant))
etat.append(("MAZAK2",0,maintenant))
etat.append(("DANOBA",0,maintenant))
etat.append(("ET2201",0,maintenant))
etat.append(("ET2202",0,maintenant))
cursor.executemany("""
            INSERT INTO etat(machine, niveau, moment) VALUES(?, ?, ?)""", etat)
db.commit()
db.close()