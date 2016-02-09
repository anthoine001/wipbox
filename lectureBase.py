#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

db = sqlite3.connect('wipOutillage.db')

cursor = db.cursor()
id = "CX7---"
cursor.execute("""SELECT machine, niveau, moment FROM etat WHERE machine=?""", (id,))
response = cursor.fetchone()
print(response)
db.close()