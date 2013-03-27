#!/usr/local/bin/python

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
