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
            <div id='header'>'''
    includeHeader()
    print '''</div>
             <div id='content'>
    '''
    includeAllCurrentLocations()
    includeNewLocationForm()

    print '''
            </div>
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
            <div id='header'> '''
    includeHeader()
            
    print '''
            </div>
            <div id='content'> '''
    includeLocation(loc_name)

    print '''
            </div>
            </body>
        </html>
    '''

def includeHeader():
    print "<img src='logo.png'>"

def includeLocation(loc_name):
    loc = getLocationFromName(loc_name)

    info = loc.getInfo()

    print "<div id='locationContainer' class='location'>"

    print   "Location: " + info["location_name"] + "<br>"

    on_call_list = loc.getCurrentPersonsOnDuty()
    print   "Currently on call: " 
    for name in on_call_list[:-1]:
        print name + ", "
    print on_call_list[-1]
    print "<br>"

    forwarding_destinations, fail_number = loc.getCurrentForwardingDestinations()
    print   "Current forwarding destinations: "

    for number in forwarding_destinations[:-1]:
        print number + ", "
    print forwarding_destinations[-1]
    print   "<br>"

    print   "<span class='small gray'>"
    print       "<a class='show_hide' href='#' rel='#advancedInfo'><b>+Advanced</b></a>"
    print        "<div id='advancedInfo' class='toggleDiv' style='display: none;'>"
    print           "<b>Calendar URL</b>: " + info["calendar_url"] + "<br>"
    print           "<b>Forwarding number</b>: " + loc.getTwilioNumber() + "<br>"
    print           "<b>Forwarding number ID</b>: " + info["forwarding_number_id"] + "<br>"
    print           "<b>Is Res-life?</b>: " + str(info['isResLife']) + "<br>"
    print        "</div>"
    print   "</span>"
    print "</div>"

    print "<div id='locationSettingsContainer' class='sidebar'>"
    includeContactListForm(info)    
    includeIsResLifeToggleForm(info)
    includeSMSToggleForm(info)
    print "</div>"

def includeSMSToggleForm(info):
    curr_sendSMS = info['send_sms']

    print "<div id='sendSMSToggle'>"
    print   "<form class='bottommargin' method=POST action=''>"
    print       "<input type='hidden' name='formName' value='smsToggleForm'>"

    if curr_sendSMS:
        print "Send SMS notifications: <input type=checkbox name='send_sms' value='True' checked onclick='this.form.submit();'><br>"
    else:
        print "Send SMS notifications: <input type=checkbox name='send_sms' value='True' onclick='this.form.submit();'><br>"
    print   "</form>"
    print "</div>"


def includeIsResLifeToggleForm(info):
    curr_isResLife = info['isResLife']

    print "<div id='isResLifeToggle'>"
    print   "<form id='resLifeToggleForm' class='bottommargin' method=POST action=''>"
    print       "<input type=hidden name='formName' value='resLifeToggleForm'>"

    if curr_isResLife:
        print   "Is Res-life: <input type=checkbox name='isResLife' value='True' checked onclick='this.form.submit();'><br>"
    else:
        print   "Is Res-life: <input type=checkbox name='isResLife' value='True' onclick='this.form.submit();'><br>"
    print   "</form>"
    print "</div>"

def includeContactListForm(info):
    cl = info["contact_list"]

    print "<div id='contactList'>"
    print   "<form id='contactListRemoveForm' class='bottommargin' method=POST action=''>" 
    print       "<input type=hidden name='formName' value='contactListRemoveForm'>"

    print       "<table>"
    for contact in cl:
        print       "<tr>"
        print           "<td><input type='checkbox' name='contact' value='" + contact + "'>" 
        print           "<td>" + contact + ":   </td>" 
        print           "<td>" + cl[contact] + "</td>"
        print       "</tr>"
    print       "</table>"
    print       "<input type='submit' class='button' value='Remove selected contacts'>"
    print   "</form>"
    print
    print   "<form id='contactListAddForm' class='bottommargin' method=POST action='' onsubmit='return validateNewContact();'>"

    print       "<a class='show_hide' href='#' rel='#newContact'>+Add a contact</a>" 
    print       "<div id='newContact' class='toggleDiv' style='display: none;'>"
    print           "<input type=hidden name='formName' value='contactListAddForm'>"

    print           "<input type=text name='contact' placeholder='Name'><br>"
    print           "<input type=text name='phone' placeholder='Number (xxx-xxx-xxxx)'><br>"
    print           "<input type=submit class='button' value='Add contact'>"
    print       "</div>"
    print   "</form>"
    print "</div>"


def includeNewLocationForm():
    print '''
        <div id="newLocationForm" class='sidebar'">
            <a class="show_hide" href="#" rel="#newLocationContainer">+Add a new location</a>
            <div id="newLocationContainer" class="toggleDiv" style="display: none;">
                <form method=POST action="" name="newLocation" onsubmit='return validateNewLocation();'>
                    <input type=hidden name='formName' value='newLocationForm'>'''
    print '''
                    Location name: <input type='text' name='name' value=""/><br>
                    Duty calendar url: <input type='text' name='cal' value=""/><br>
                    Twilio phone number id: <input type='text' name='twilio_id' value=""/><br>
                    Phone number list (name:xxx-xxx-xxx): <textarea rows="5" cols="30" name='contacts' value=""></textarea><br>
                    Is Res-life: <input type=checkbox name='isResLife' value='True'><br>
                    <input type="submit" class='button' value="Add location"/>
                </form>
            </div>
        </div>
        <br><br>
    '''

def includeAllCurrentLocations():
    print "<div id='locations'>"
    print '''<form id="removeLocationForm" method=POST action="main.cgi" name="removeLocation">'''
    print       "<input type=hidden name='formName' value='removeLocationForm'>"
    for loc in locations:
        info = loc.getInfo()
        print "<div class='location'>"
        print    "Location: <a href='main.cgi?location=" + info["location_name"] + "'>" + info["location_name"] + "</a><br>"
        on_duty_list = loc.getCurrentPersonsOnDuty()
        print    "Currently on call: "
        for name in on_duty_list[:-1]:
            print name + ", "
        print on_duty_list[-1]
        print "<br>"
        forwarding_destinations, fail_number = loc.getCurrentForwardingDestinations()

        print    "Current forwarding destinations: "
        for number in forwarding_destinations[:-1]:
            print number + ", "
        print forwarding_destinations[-1]
        print "<br>"

        print    "<span class='small gray'>"
        print    "<a class='show_hide' href='#' rel='#advancedInfo" + info['location_name'] + "'><b>+Advanced</b></a>"
        print    "<div id='advancedInfo" + info['location_name'] + "' class='toggleDiv' style='display: none;'>"
        print       "<b>Calendar URL</b>: " + info["calendar_url"] + "<br>"
        print       "<b>Forwarding number ID</b>: " + info["forwarding_number_id"] + "<br>"
        print       "<b>Is Res-life?</b>: " + str(info['isResLife']) 
        print       """<a href='#'><img src='delete.png' class='deleteIcon' onclick="removeLoc('""" + info["location_name"] + """');"></a>"""
        print    "</div>"
        print    "</span>"
        print "</div>"
    
    print   "</form>"
    print "</div>"

def parseNewLocationForm(form):
    new_info = {}
    
    new_info["location_name"] = form["name"].value
    new_info["calendar_url"] = form["cal"].value
    new_info["forwarding_number_id"] = form["twilio_id"].value
    new_info["send_sms"] = False  # default off
    if "isResLife" in form:
        new_info['isResLife'] = True
    else:
        new_info['isResLife'] = False
    
    contact_list = {}

    cl = form["contacts"].value.strip()
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
    

def toggleIsResLife(loc_name):
    loc = getLocationFromName(loc_name)

    loc.getInfo()['isResLife'] = not loc.getInfo()['isResLife']

    loc.update()

def toggleSendSMS(loc_name):
    loc = getLocationFromName(loc_name)

    loc.getInfo()['send_sms'] = not loc.getInfo()['send_sms']

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
                toggleIsResLife(loc_name)
             
            if form_name == "smsToggleForm":
                toggleSendSMS(loc_name)

        showLocationInterface(loc_name)

    elif 'formName' in form:
         form_name = form['formName'].value

         if form_name == "newLocationForm":
             addNewLocation(form)

         if form_name == "removeLocationForm":
             removeLocations(form)
         
         showMainInterface()

    else:
        showMainInterface()

    dumpToFile()


main()

