#!/usr/bin/env python
# coding: utf-8 

import sqlite3
import datetime
import time
db = sqlite3.connect('wipOutillageYnnis.db')
cursor = db.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS Machine (
     machine_ID TEXT,
     unix REAL,
     datestamp TEXT,
     level REAL,
     threshold INTEGER,
     coordx INTEGER,
     coordy INTEGER
)
""")

db.commit()
Machine = []
unix=time.time()
maintenant = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
Machine.append(("K3X8--",unix,maintenant,0,4,0,0))
Machine.append(("K2X8--",unix,maintenant,0,4,0,0))
Machine.append(("CX7---",unix,maintenant,0,4,0,0))
Machine.append(("KX10--",unix,maintenant,0,4,0,0))
Machine.append(("MAZAK1",unix,maintenant,0,4,0,0))
Machine.append(("MAZAK2",unix,maintenant,0,4,0,0))
Machine.append(("DANOBA",unix,maintenant,0,4,0,0))
Machine.append(("ET2201",unix,maintenant,0,4,0,0))
Machine.append(("ET2202",unix,maintenant,0,4,0,0))
Machine.append(("CAZENE",unix,maintenant,0,4,0,0))
cursor.executemany("""
            INSERT INTO Machine(machine_ID, unix, datestamp, level, threshold, coordx,coordy) VALUES(?, ?, ?, ?, ?, ?, ?)""", Machine)
db.commit()
db.close()
