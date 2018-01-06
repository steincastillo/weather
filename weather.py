# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 23:23:06 2018

@author: stein
"""


import json
import datetime
import time
from requests import get
import numpy as numpy
import pandas as pd
import os
import sqlite3

oweather_key = conf['oweather_key']
oweather_city = conf['oweather_city']
oweather_call = "http://api.openweathermap.org/data/2.5/weather?id=" + oweather_city + "&units=metric&appid=" + oweather_key

INTERVAL = 600
loop = True

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



ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
    help="usage: python3 weather.py --conf [file.json]")
args = vars(ap.parse_args())
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

# Define www.openweather.com web call
oweather_key = conf['oweather_key']
oweather_city = conf['oweather_city']
oweather_call = "http://api.openweathermap.org/data/2.5/weather?id=" + oweather_city + "&units=metric&appid=" + oweather_key

# Open DB
conn, cursor = dbConnect('weather.db')

# Initialize loop
loop = True

while loop:
    print ('Requesting wheater report...')
    tstamp = datetime.datetime.now().strftime('%c')
    weather = get(oweather_call).json()
    temp = weather['main']['temp']
    press = weather['main']['pressure']
    hum = weather['main']['humidity']
    
    print ('Report received...')
    print ('Time: {}'.format(tstamp))
    print ('temperature: {}'.format(temp))
    print ('Pressure: {}'.format(press))
    print ('Humidity: {}'.format(hum))
    
    print ('Saving data into DB...')
    print ('**********************')

    
    row = (loc, tstamp, temp, hum, press)
    sql = 'INSERT INTO weather (location, date, temperature, humidity, pressure) \
        VALUES (?, ?, ?, ?, ?)'
    cursor.execute(sql, row)
    conn.commit()
    
    print ('Waiting for next iteration...')
    time.sleep(INTERVAL)
    
    
    
