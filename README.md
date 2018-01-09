# weather.py
weather logging and monitoring

Work in progress...  
## What does it do?  
**Weather.py** is a two program application:  
1. weather.py: connects to www.openweather.com and downloads the weather conditions of an specific location and saves the information in a sqlite Database.  
2. monitor.py: Reads the database created by weather.py and graphs the results. This routine can run in two modes:
* Static: Read the weather database and graph the results  
* Dynamic: Read the weather database and graph the results with a live update of the conditions (animated chart)  
