calendar-on-call
================

Current live link (to see what it looks like:) [calendar-on-call](http://dev.isaacdontjelindell.com/calendar-on-call/main.cgi)


TODO
-------
* Error handling!
  - when there isn't anyone on duty
  - any API unreachable
  - can't find person on duty in contact list
  - invalid form data (maybe JavaScript form validation)
  - more...
* link to location-specific interface from admin/main
* change isResLife fallback number in location-specific interface
* multiple people on duty
* get working on Knuth (install dependencies, set environment variables). Will have to work with Miller on this.
* more...



Design
-------
Every time `main.cgi` is called, it reads in all information (locations, etc) from a JSON text file (`calendar-on.call.dat`. JSON is like YAML but doesn't require another dependency). If 
any changes are made (adding/removing a location, updating contact list, manual override), it saves all that information
into the DAT file for the next time. `update.cgi` also reads in this DAT file to get the list of locations to call `update()` on.

* `Location.py`: takes a dictionary of parameters, including the Twilio phone number ID, the icalendar URL, a location name, and a sub-dictionary containing the contact list for that location.
* `main.cgi`: Currently displays all locations that have been added, allows for adding a new location, and manually triggering an update check (using `update.cgi`, below)
* `update.cgi`: When called, triggers an update check on all locations in the calendar-on-call.dat file. Will update the Twilio forwarding number for that location if the person on duty has changed (based on the Google Calendar icalendar URL associated with that location).

update.cgi is currently called by cronjob every 3 minutes. The interval should probably be increased later.

Dependencies
----------
* pip install twilio
* pip install python-dateutil
* pip install icalendar


Misc
-------
* What should the web interface handle? 
  * Manually specifying a number to forward to for a `Location` (overriding duty calendar).
	-@smitau01 I think a manual override is a great idea but it needs to have a shutoff value set and a defult shutoff override.
  * Show current information - Locations, forwarding numbers, calendars, etc.
	-@smitau01 I'd say if there can be an "admin" dashboard of sorts that anyone with the top level admin login can see all the numbers in use and who they are set up to forward to at the present time.
	  Also if we can do some basic authentication stuff (maybe later once this is covered in class? otherwise I know a basic form of it would be pretty easy to implement so that each AHD or "location manager" can only edit or manually override for their location.


My attempt at a google Contacts API key request:

Client ID:	
709696327552.apps.googleusercontent.com
Email address:	
709696327552@developer.gserviceaccount.com
Client secret:	
fxZAnABYEpMr4V_lGSaw-fqF
Redirect URIs:	https://knuth.luther.edu/~smitau01/*
https://knuth.luther.edu/~dontis01/*
JavaScript origins:	none
