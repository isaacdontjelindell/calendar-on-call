#!/usr/bin/python

from Location import Location
import json
import os
import cgitb
import cgi


# global variables
locations = []


def setup():
    calendar_url = "http://www.google.com/calendar/ical/luther.edu_p5c373m13dppnsqeajcs4se5nc%40group.calendar.google.com/public/basic.ics"
    forwarding_number_id = "PN3370cd26b57b0bf69e7bfce10c008a4b"

    contact_list = {}
    contact_list["Isaac DL"] = "612-978-3683"
    contact_list["Austen Smith"] = "319-743-8485"

    info["calendar_url"] = calendar_url
    info["forwarding_number_id"] = forwarding_number_id
    info["contact_list"] = contact_list

    location = Location(info)

def dumpToFile():
    outlist = []
    for loc in locations:
        outlist.append(loc.getInfo())
    with open('calendar-on-call.dat', 'w') as outfile:
        json.dump(outlist, outfile)

def readFromFile():
    inlist = []
    with open('calendar-on-call.dat', 'r') as infile:
        inlist = json.load(infile)

    for info in inlist:
        locations.append(Location(info))


def showWebInterface():
    print "Content-Type: text/html"
    print

    print '''
        <!DOCTYPE html>
        <html>
        <head>
        <title>Calendar On Call</title>
        </head>
        <body>
    '''
    includeNewLocationForm()
    includeCurrentLocations()

    print '''
        </body>
        </html>
    '''


def includeNewLocationForm():
    print '''
        <form method=POST action="main.py" name="newLocation">
            Location name: <input type='text' name='name' value=""/><br>
            Duty calendar url: <input type='text' name='cal' value=""/><br>
            Twilio phone number id: <input type='text' name='twilio_id' value=""/><br>
            Phone number list: <textarea rows="10" cols="40" name='contacts' value=""></textarea><br>
            <input type="submit" value="Submit"/>
        </form>
        <br><br>
    '''

def includeCurrentLocations():
    print '''<div id="locations">'''
    for loc in locations:
        info = loc.getInfo()
        print "Location: " + info["location_name"] + "<br>"
        print "Calendar URL: " + info["calendar_url"] + "<br>"
        print "Forwarding number ID: " + info["forwarding_number_id"] + "<br>"
        print "<br>"
    
    print '''</div>'''

def parseNewLocationForm(form):
    new_info = {}
    
    new_info["location_name"] = form["name"].value
    new_info["calendar_url"] = form["cal"].value
    new_info["forwarding_number_id"] = form["twilio_id"].value
    
    contact_list = {}

    cl = form["contacts"].value
    cl = cl.split('\n')
    for contact in cl:
        temp = contact.split(':')
        name = temp[0].strip()
        number = temp[1].strip()
        contact_list[name] = number

    new_info["contact_list"] = contact_list
    return new_info

def addNewLocation(form):
    new_info = parseNewLocationForm(form)
    new_location = Location(new_info)
    locations.append(new_location)

def main():
    cgitb.enable()

    readFromFile() # recover existing locations

    form = cgi.FieldStorage() # special object!
    
    # if the page has just been loaded, form won't contain anything
    if "name" in form:
        addNewLocation(form)

    showWebInterface()
    dumpToFile()


main()
