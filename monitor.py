#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 00:13:41 2018

@author: stein

************************************
*                                  *
*           Weather.py             *
*          Version: 1.2            *
*                                  *
************************************

Usage:
    python3 monitor.py --animate [yes|no]
        
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as md
import time
import datetime
import argparse
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
    
# Define functions

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        return False

def animate(i):
    """ Animates the temperature chart """
    
    data = pd.read_sql_query(sql, conn)
    #data = data[(len(data)-10):]
    xlist = []
    ylist = []
    for row in range(len(data)):
        x = data['date'][row]
        x = datetime.datetime.strptime(x, '%a %b %d %H:%M:%S %Y')
        y = data['temperature'][row]
        xlist.append(x)
        ylist.append(y)
    print ('[MSG] Updating chart...{}'.format(datetime.datetime.now()))
    ax1.clear()
    ax1.set_title('Temperature Monitor')
    ax1.set_xlabel('Date/Time')
    ax1.set_ylabel('Temp (C)')
    ax1.grid(b=True, linestyle='dashed', color='grey')
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax1.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=30)
    #fig.autofmt_xdate()
    ax1.plot(xlist, ylist, lw=2)

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(description = "Display realtime weather readings")
ap.add_argument("-a",
                "--animate",
                required = False,
                default = False, 
                type = str2bool,
                help ="Animate the chart with realtime readings")
args = vars(ap.parse_args())

print(args)

# Open DB read only mode
conn = sqlite3.connect('file:weather.db?mode=ro', uri=True)
c = conn.cursor()

fig, ax1 = plt.subplots()

sql = 'SELECT * FROM weather;'
interval = 120000

if args['animate']:
    print ('[MSG] Dynamic chart displayed. Live update active')
    print ('live update every {} seconds'.format(interval/1000))   
    ani = animation.FuncAnimation(fig, animate, interval=interval)
    plt.show()
else:
    data = pd.read_sql_query(sql, conn)
    #data = data[(len(data)-10):]
    xlist = []
    ylist = []
    for row in range(len(data)):
        x = data['date'][row]
        x = datetime.datetime.strptime(x, '%a %b %d %H:%M:%S %Y')
        y = data['temperature'][row]
        xlist.append(x)
        ylist.append(y)
    print ('[MSG] Static chart displayed. Live update disabled')
    ax1.clear()
    ax1.set_title('Temperature Monitor')
    ax1.set_xlabel('Date/Time')
    ax1.set_ylabel('Temp (C)')
    ax1.grid(b=True, linestyle='dashed', color='grey')
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax1.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=30)
    #fig.autofmt_xdate()
    ax1.plot(xlist, ylist, lw=2)
    plt.show()
    
