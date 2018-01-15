#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 23:23:06 2018

@author: stein

************************************
*                                  *
*           Weather.py             *
*          Version: 1.2            *
*                                  *
************************************

Usage:
    python3 weather.py --conf <file.json>
    python3 weagher.py -c <file.jsoin>
    
Connects to www.weather.com to read the weather conditions of a 
determined location and saves the results in a SQLite database
"""

# Import libraries

import sqlite3
import json
import datetime
import os
import argparse
import numpy as np
import pandas as pd
import signal
from datetime import timedelta
import time
from requests import get


# Define functions

def handler(signum, frame):
    print ('\n[MSG] CTRL+C received. Exiting.')
    dbClose(conn)
    exit(0)

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

# Main loop

if __name__ == '__main__':
    # Print routine header
    print(__doc__)
    # Parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True,
        help="usage: python3 weather.py --conf [file.json]")
    args = vars(ap.parse_args())
    conf = json.load(open(args["conf"]))
    
    # Define www.openweather.com web call
    oweather_key = conf['oweather_key']
    oweather_city = conf['oweather_city']
    oweather_call = "http://api.openweathermap.org/data/2.5/weather?id=" + \
                    oweather_city + "&units=metric&appid=" + oweather_key
    
    # Open DB
    conn, cursor = dbConnect('weather.db')
    
    # Initialize loop
    INTERVAL = conf['read_interval']
    #INTERVAL = 10
    loop = True
    reading = 0
    # Set CTRL+C capture event
    print ('Initiating weather sampling. Press Ctrl+C to finish')
    signal.signal(signal.SIGINT, handler)
    
    while loop:
        reading += 1
        print ('Reading no. {}'.format(reading))
        print ('Requesting weather report...')
        try:
            weather = get(oweather_call).json()
            tstamp = datetime.datetime.now().strftime('%c')
            temp = weather['main']['temp']
            press = weather['main']['pressure']
            hum = weather['main']['humidity']
            
            #temp = 7.5
            #press = 1000
            #hum = 60
            
            print ('Report received...')
            print ('City: {}'.format(weather['name']))
            print ('Country: {}'.format(weather['sys']['country']))
            print ('Time: {}'.format(tstamp))
            print ('temperature: {}'.format(temp))
            print ('Pressure: {}'.format(press))
            print ('Humidity: {}'.format(hum))
            print ('Saving data into DB...')
            print ('**********************')
            
            # Save data into DB
            row = (oweather_city, tstamp, temp, hum, press)
            sql = 'INSERT INTO weather (location, date, temperature, humidity, pressure) \
                VALUES (?, ?, ?, ?, ?)'
            cursor.execute(sql, row)
            conn.commit()
        except:
            print('[ERROR]: Report not received. Will try again later')
        
        nextread = datetime.datetime.now() + timedelta(seconds=INTERVAL)
        print ('Next reading at: {} '.format(nextread))
        time.sleep(INTERVAL)
    
    
    
