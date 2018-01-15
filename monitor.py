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

def dbConnectRead(sqlite_file):
    """ Make connection to an SQLite database READ ONLY mode """

    # Validate  DB is available
    if not(os.path.isfile(sqlite_file)):              
        print ("[Error] File {} does not exist. Please verify\n".format(sqlite_file))
        exit(0)
    line = 'file:' + sqlite_file + '?mode=ro'
    conn = sqlite3.connect(line, uri=True)
    c = conn.cursor()
    return conn, c

def dbClose(conn):
    """ Commit changes and close connection to the database """
    
    conn.commit()
    conn.close()
    
# Define functions

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', '1', 'y', 'T'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'F', 'n', '0'):
        return False
    else:
        return False

def animate(i):
    """ Animates the temperature chart """
    
    data = pd.read_sql_query(sql, conn)
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
    ax1.plot(xlist, ylist, lw=2)

# Main loop
if __name__ == '__main__':
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser(description = "Display realtime weather readings")
    ap.add_argument("-a",
                    "--animate",
                    required = False,
                    default = True, 
                    type = str2bool,
                    help ="Enable live update: [yes|no]")
    args = vars(ap.parse_args())
    
    # Open DB read only mode
    conn, cursor = dbConnectRead('weather.db')
    
    fig, ax1 = plt.subplots()
    
    sql = 'SELECT * FROM weather;'
    interval = 120000
    
    if args['animate']:
        print ('[MSG] Dynamic chart displayed. Live update active')
        print ('live update every {} seconds'.format(interval/1000))
        print ('*************************')   
        ani = animation.FuncAnimation(fig, animate, interval=interval)
        plt.show()
    else:
        data = pd.read_sql_query(sql, conn)
        xlist = []
        ylist = []
        for row in range(len(data)):
            x = data['date'][row]
            x = datetime.datetime.strptime(x, '%a %b %d %H:%M:%S %Y')
            y = data['temperature'][row]
            xlist.append(x)
            ylist.append(y)
        print ('[MSG] Static chart displayed. Live update disabled')
        print ('*************************') 
        
        # Draw statc chart
        ax1.set_title('Temperature Monitor')
        ax1.set_xlabel('Date/Time')
        ax1.set_ylabel('Temp (C)')
        ax1.grid(b=True, linestyle='dashed', color='grey')
        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax1.xaxis.set_major_formatter(xfmt)
        plt.xticks(rotation=30)
        ax1.plot(xlist, ylist, lw=2)
        plt.show()
        
    # Close the database
    dbClose(conn)
    
