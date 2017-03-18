#!/usr/bin/env python
# coding: utf-8 

import sqlite3
import datetime

db = sqlite3.connect('wipHistoriqueYnnis.db')
cursor = db.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS histo(
     unix REAL,
     datestamp TEXT,
     machine TEXT,
     level REAL,
     threshold INTEGER)
""")

db.commit()
db.close()
