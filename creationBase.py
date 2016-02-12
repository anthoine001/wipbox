#!/usr/bin/env python
# coding: utf-8 

import sqlite3
from datetime import datetime

db = sqlite3.connect('wipOutillage.db')
cursor = db.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS etat(
     machine TEXT PRIMARY KEY UNIQUE,
     niveau INTERGER,
     moment TEXT,
     alerte INTEGER
)
""")

db.commit()
etat = []
maintenant = str(datetime.now())
etat.append(("K3X8--",0,maintenant,4))
etat.append(("K2X8--",0,maintenant,4))
etat.append(("CX7---",0,maintenant,4))
etat.append(("KX10--",0,maintenant,4))
etat.append(("MAZAK1",0,maintenant,4))
etat.append(("MAZAK2",0,maintenant,4))
etat.append(("DANOBA",0,maintenant,4))
etat.append(("ET2201",0,maintenant,4))
etat.append(("ET2202",0,maintenant,4))
etat.append(("CAZENE",0,maintenant,4))
cursor.executemany("""
            INSERT INTO etat(machine, niveau, moment, alerte) VALUES(?, ?, ?, ?)""", etat)
db.commit()
db.close()