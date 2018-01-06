# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 00:13:41 2018

@author: stein
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sqlite3
import pandas as pd
import os

# Database management functions

def dbConnect(sqlite_file):
    """ Make connection to an SQLite database """

    # Validate  DB is available
    if not(os.path.isfile(sqlite_file)):              
        print ("[Error] File {} does not exist. Please verify\n".format(sqlite_file))
        exit(0)
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c

def dbClose(conn):
    """ Commit changes and close connection to the database """
    
    conn.commit()
    conn.close()
    

fig, ax1 = plt.subplots()


sql = 'SELECT * FROM weather;'

# Open DB read only mode
conn = sqlite3.connect('file:weather.db?mode=ro', uri=True)
c = conn.cursor()

def animate(i):
    data = pd.read_sql_query(sql, conn)
    xlist = []
    ylist = []
    for row in range(len(data)):
        x = data['date'][row]
        y = data['temperature'][row]
        xlist.append(x)
        ylist.append(y)
    ax1.clear()
    ax1.set_title('Temperature Monitor')
    ax1.set_xlabel('Date/Time')
    ax1.set_ylabel('Temp (C)')
    ax1.grid(b=True, linestyle='dashed', color='grey')
    fig.autofmt_xdate()
    ax1.plot(xlist, ylist, lw=2)
    
ani = animation.FuncAnimation(fig, animate, interval=5000)