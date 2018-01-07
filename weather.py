# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 23:23:06 2018

@author: stein
"""

# Import libraries
import json
import datetime
from datetime import timedelta
import time
import os
import argparse
from requests import get
import numpy as numpy
import pandas as pd
import sqlite3

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
INTERVAL = conf['interval']
#INTERVAL = 10
loop = True
reading = 0

while loop:
    reading += 1
    print ('Reading no. {}'.format(reading))
    print ('Requesting weather report...')
    weather = get(oweather_call).json()
    tstamp = datetime.datetime.now().strftime('%c')
    temp = weather['main']['temp']
    press = weather['main']['pressure']
    hum = weather['main']['humidity']
    
    #temp = 7.5
    #press = 1000
    #hum = 60
    
    print ('Report received...')
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
    
    nextread = datetime.datetime.now() + timedelta(seconds=INTERVAL)
    print ('Next reading at: {} '.format(nextread))
    time.sleep(INTERVAL)
    
    
    
