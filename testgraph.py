import matplotlib.pyplot as plt
import time
import datetime
import matplotlib.dates as mdates
from matplotlib import style
import sqlite3
style.use('fivethirtyeight')

db = sqlite3.connect('wipHistoriqueYnnis.db')
c=db.cursor()

def graph_data():
    c.execute('SELECT moment,niveau FROM histo')
    data = c.fetchall()
    #print (data)
    dates = []
    values = []
    
    for row in data:
        moment=row[0]
        tounga=datetime.datetime.strptime(moment,'%Y-%m-%d %H:%M:%S')
        print (tounga)
        wounga=float (mdates.datestr2num(tounga))
        dates.append(datetime.datetime.fromtimestamp(wounga))
        print (dates)
        values.append(row[1])
        print (values)

    plt.plot_date(dates,values,'-')
    plt.show()
graph_data()
c.close()
