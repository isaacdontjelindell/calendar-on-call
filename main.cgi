#!/usr/local/bin/python

from Location import Location
import json
import os
import cgitb
import cgi
import httplib2
import sys


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
        try:
            locations.append(Location(info))
        except httplib2.ServerNotFoundError:
           showErrors("Twilio seems to be unreachable - try again later.")

def showErrors(error):
    
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
    
    print "<div id='error'>"
    print     error
    print "</div>"


    print '''
            </body>
        </html>
    '''
    sys.exit()

def showMainInterface():
    print "Content-Type: text/html"
    print 

    print '''
        <!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="style.css">
                <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
                <script type="text/javascript" src="main.js"></script>
                <title>Calendar On Call</title>
            </head>
            <body>
    '''
    includeNewLocationForm()
    includeAllCurrentLocations()
    includeUpdateButton()

    print '''
            </body>
        </html>
    '''

def showLocationInterface(loc_name):
    print "Content-Type: text/html"
    print 

    print '''
        <!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="style.css">
                <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
                <script type="text/javascript" src="main.js"></script>
                <title>Calendar On Call</title>
            </head>
            <body>
    '''
    
    includeLocation(loc_name)

    print '''
            </body>
        </html>
    '''

def includeLocation(loc_name):
    loc = getLocationFromName(loc_name)

    info = loc.getInfo()

    print "<div id='locationContainer'>"

    print   "Location: " + info["location_name"] + "<br>"

    on_call_list = loc.getCurrentPersonsOnDuty()
    print   "Currently on call: " 
    for name in on_call_list:
        print name + ", "
    print "<br>"

    forwarding_destinations, fail_number = loc.getCurrentForwardingDestinations()
    print   "Current forwarding destinations: "
    for number in forwarding_destinations:
        print number + ", "
    print   "<br>"

    print   "<span class='small gray'>"
    print       "<a class='show_hide' href='#' rel='#advancedInfo'>+Advanced Information</a>"
    print        "<div id='advancedInfo' class='toggleDiv' style='display: none;'>"
    print           "<b>Calendar URL</b>: " + info["calendar_url"] + "<br>"
    print           "<b>Forwarding number ID</b>: " + info["forwarding_number_id"] + "<br>"
    print           "<b>Is Res-life?</b>: " + str(info['isResLife']) + "<br>"
    print        "</div>"
    print   "</span>"
    
    includeContactListForm(info)    
    includeIsResLifeToggleForm(info)

    print "</div>"

def includeIsResLifeToggleForm(info):
    curr_isResLife = info['isResLife']

    print "<div id='isResLifeToggle'>"
    print   "<form id='resLifeToggleForm' method=POST action=''>"
    print       "<input type=hidden name='formName' value='resLifeToggleForm'>"

    print       "<input type='hidden' value='False' name='isResLife'>"
    if curr_isResLife:
        print   "Is Res-life: <input type=checkbox name='isResLife' value='True' checked onclick='this.form.submit();'><br>"
    else:
        print   "Is Res-life: <input type=checkbox name='isResLife' value='True' onclick='this.form.submit();'><br>"
    print   "</form>"
    print "</div>"

def includeContactListForm(info):
    cl = info["contact_list"]

    print "<div id='contactList'>"
    print   "<form id='contactListRemoveForm' method=POST action=''>" 
    print       "<input type=hidden name='formName' value='contactListRemoveForm'>"

    print       "<table>"
    for contact in cl:
        print       "<tr>"
        print           "<td><input type='checkbox' name='contact' value='" + contact + "'>" 
        print           "<td>" + contact + ":   </td>" 
        print           "<td>" + cl[contact] + "</td>"
        print       "</tr>"
    print       "</table>"
    print       "<input type='submit' value='Remove selected contacts'>"
    print   "</form>"
    print
    print   "<form id='contactListAddForm' method=POST action=''>"

    print       "<a class='show_hide' href='#' rel='#newContact'>+Add a contact</a>" 
    print       "<div id='newContact' class='toggleDiv' style='display: none;'>"
    print           "<input type=hidden name='formName' value='contactListAddForm'>"

    print           "<input type=text name='contact' value='Name'>"
    print           "<input type=text name='phone' value='Phone'>"
    print           "<input type=submit value='Add contact'>"
    print       "</div>"
    print   "</form>"
    print "</div>"


def includeUpdateButton():
    print '''
        <input type="button" onclick="var img = new Image(); img.src='update.cgi'" value="Update forwarding numbers based on duty calendars. (Refresh page to see changes)">
    '''

def includeNewLocationForm():
    print '''
        <a class="show_hide" href="#" rel="#newLocationContainer">+Add a new location</a>
        <div id="newLocationContainer" class="toggleDiv" style="display: none;">
            <div id="newLocationForm">
                <form method=POST action="" name="newLocation">
                    <input type=hidden name='formName' value='newLocationForm'>'''
    print '''
                    Location name: <input type='text' name='name' value=""/><br>
                    Duty calendar url: <input type='text' name='cal' value=""/><br>
                    Twilio phone number id: <input type='text' name='twilio_id' value=""/><br>
                    Is Res-life: <input type=checkbox name='isResLife' value='True'><br>
                    Phone number list (name:xxx-xxx-xxx): <textarea rows="5" cols="30" name='contacts' value=""></textarea><br>
                    <input type="submit" value="Add location"/>
                </form>
            </div>
        </div>
        <br><br>
    '''

def includeAllCurrentLocations():
    print "<div id='locations'>"
    print '''<form method=POST action="main.cgi" name="removeLocation">'''
    print       "<input type=hidden name='formName' value='removeLocationForm'>"
    print   "<ul>"
    for loc in locations:
        info = loc.getInfo()
        print "<li>"
        print    "<input type='checkbox' name='location' value='" + info["location_name"] + "'>"
        print    "Location: <a href='main.cgi?location=" + info["location_name"] + "'>" + info["location_name"] + "</a><br>"
        on_duty_list = loc.getCurrentPersonsOnDuty()
        print    "Currently on call: "
        for name in on_duty_list:
            print (name + ", ")
        print "<br>"
        forwarding_destinations, fail_number = loc.getCurrentForwardingDestinations()

        print    "Current forwarding destinations: "
        for number in forwarding_destinations:
            print number + ", "
        print "<br>"

        print    "<span class='small gray'>"
        print    "<a class='show_hide' href='#' rel='#advancedInfo" + info['location_name'] + "'>+Advanced Information</a>"
        print    "<div id='advancedInfo" + info['location_name'] + "' class='toggleDiv' style='display: none;'>"
        print       "<b>Calendar URL</b>: " + info["calendar_url"] + "<br>"
        print       "<b>Forwarding number ID</b>: " + info["forwarding_number_id"] + "<br>"
        print       "<b>Is Res-life?</b>: " + str(info['isResLife']) + "<br>"
        print    "</div>"
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
    if "isResLife" in form:
        new_info['isResLife'] = True
    else:
        new_info['isResLife'] = False
    
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

def getLocationFromName(loc_name):
    for l in locations:
        if l.getInfo()['location_name'].lower() == loc_name.lower():
            return l
    showErrors("Unknown location " + loc_name)
    

def toggleIsResLife(loc_name, form):
    loc = getLocationFromName(loc_name)

    loc.getInfo()['isResLife'] = not loc.getInfo()['isResLife']

def removeContacts(loc_name, form):
    remove_contacts = form.getlist("contact")
    loc = getLocationFromName(loc_name)
    info = loc.getInfo()
    
    for r_con in remove_contacts:
        del info["contact_list"][r_con]

def addContact(loc_name, form):
    name = form['contact'].value
    number = form['phone'].value

    loc = getLocationFromName(loc_name)
    info = loc.getInfo()

    info['contact_list'][name] = number

def addNewLocation(form):
    new_info = parseNewLocationForm(form)
    new_location = Location(new_info)
    locations.append(new_location)
    new_location.update()

def removeLocations(form):
    remove_loc = form.getlist("location")
    global locations # I have no idea why this is nessessary here and nowhere else

    locations = [ l for l in locations if not l.getInfo()['location_name'] in remove_loc ]
    
def main():
    cgitb.enable()

    readFromFile() # recover existing locations

    query_string = os.environ["QUERY_STRING"]
    form = cgi.FieldStorage() # special object!
    
    if "location=" in query_string:
        temp = query_string.split("=")
        loc_name = temp[1]
        
        if 'formName' in form:
            form_name = form['formName'].value

            if form_name == "contactListRemoveForm":
                removeContacts(loc_name, form)

            if form_name == "contactListAddForm":
                addContact(loc_name, form)

            if form_name == "resLifeToggleForm":
                toggleIsResLife(loc_name, form)
             
        showLocationInterface(loc_name)

    elif 'formName' in form:
         form_name = form['formName'].value

         if form_name == "newLocationForm":
             addNewLocation(form)
             showMainInterface()

         elif form_name == "removeLocationForm":
             removeLocations(form)
             showMainInterface()

    else:
        showMainInterface()

    dumpToFile()


main()

