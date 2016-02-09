#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

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
db.close()