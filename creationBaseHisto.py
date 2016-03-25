#!/usr/bin/env python
# coding: utf-8 

import sqlite3
from datetime import datetime

db = sqlite3.connect('wipHistorique.db')
cursor = db.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS histo(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     machine TEXT,
     niveau INTERGER,
     moment TEXT,
     alerte INTEGER
)
""")

db.commit()
db.close()
