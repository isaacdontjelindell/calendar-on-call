#!/usr/local/bin/python

# run as a cronjob and log to /home/isaac/cron_log
# */3 * * * * cd /var/www/dev/calendar-on-call; ./update.cgi 1> /home/isaac/cron_log 2>&1


import json
from Location import Location

locations = []

def readFromFile():
    inlist = []
    with open('calendar-on-call.dat', 'r') as infile:
       inlist = json.load(infile)

    for info in inlist:
        locations.append(Location(info))


def update():
    readFromFile()
    for loc in locations:
        loc.update()

update()
