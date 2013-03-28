#!/usr/local/bin/python

from Location import Location
import json
import os
import cgitb
import cgi


# global variables
locations = []

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
                <link rel="stylesheet" type="text/css" href="style.css">
                <title>Calendar On Call</title>
            </head>
            <body>
    '''
    includeNewLocationForm()
    includeCurrentLocations()
    includeUpdateButton()

    print '''
            </body>
        </html>
    '''

def includeUpdateButton():
    print '''
        <input type="button" onclick="var img = new Image(); img.src='update.cgi'" value="Update forwarding numbers based on duty calendars. (Refresh page to see changes)">
    '''

def includeNewLocationForm():
    print '''
        <form method=POST action="main.cgi?newLocation" name="newLocation">
            Location name: <input type='text' name='name' value=""/><br>
            Duty calendar url: <input type='text' name='cal' value=""/><br>
            Twilio phone number id: <input type='text' name='twilio_id' value=""/><br>
            Phone number list: <textarea rows="5" cols="30" name='contacts' value=""></textarea><br>
            <input type="submit" value="Submit"/>
        </form>
        <br><br>
    '''

def includeCurrentLocations():
    print "<div id='locations'>"
    print '''<form method=POST action="main.cgi?removeLocation" name="removeLocation">'''
    print   "<ul>"
    for loc in locations:
        info = loc.getInfo()
        print "<li>"
        print    "<input type='checkbox' name='location' value='" + info["location_name"] + "'>"
        print    "Location: " + info["location_name"] + "<br>"
        print    "Currently on call: " + loc.getCurrentPersonOnDuty()[0] + "<br>"   # TODO handle multiple
        print    "Current forwarding destination: " + loc.getCurrentForwardingDestination() + "<br>"
        print    "<span class='small gray'>"
        print    "Advanced information:<br>"
        print    "Calendar URL: " + info["calendar_url"] + "<br>"
        print    "Forwarding number ID: " + info["forwarding_number_id"] + "<br>"
        print    "</span>"
        print "</li>"
    
    print   "</ul>"
    print   "<input type='submit' value='Remove selected locations'>"
    print   "</form>"
    print "</div>"

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

def removeLocations(form):
    remove_loc = form.getlist("location")
    temp = []
    for r_loc in remove_loc:
        for loc in locations:
            if loc.getInfo()["location_name"] == r_loc:
                temp.append(locations.index(loc))

    for i in temp:
        locations.pop(i)
    
def main():
    cgitb.enable()

    readFromFile() # recover existing locations

    query_string = os.environ['QUERY_STRING']

    form = cgi.FieldStorage() # special object!
    
    if "newLocation" in query_string:
        addNewLocation(form)

    if "removeLocation" in query_string:
        removeLocations(form)

    showWebInterface()
    dumpToFile()


main()
