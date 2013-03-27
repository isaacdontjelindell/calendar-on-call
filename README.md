calendar-on-call
================


TODO
-------
* Error handling!
  - when there isn't anyone on duty
  - multiple people on duty
  - any API unreachable
  - more...
* allow removal of locations
* time checks for reslife applications (person on duty on 25th is actually on call until 7am on 26th, etc)
* more...



Design
-------
* `Location.py`: takes a dictionary of parameters, including the Twilio phone number ID, the icalendar URL, a location name, and a sub-dictionary containing the contact list for that location.
* `main.cgi`: Currently displays all locations that have been added, allows for adding a new location, and manually triggering an update check (using `update.cgi`, below)
* `update.cgi`: When called, triggers an update check on all locations in the calendar-on-call.dat file. Will update the Twilio forwarding number for that location if the person on duty has changed (based on the Google Calendar icalendar URL associated with that location).


Dependencies
----------
* pip install twilio
* pip install python-dateutil
* pip install icalendar


Misc
-------
* How do we want to handle contact lists? Should a separate contact list be created, either in a Google account or maintained internally by this program?
	-@smitau01 I'd say ultimently we should interface with google contacts and I can look into how difficult this will be but we could also have a contanct list maintained by the program.
	-@smitau01 OK on second thought... the more I read about OAuth an how much of a pain in the butt it is I'd say let's just have the program itself maintain the contacts information because all the OAuth token stuff I can figure out only provides short lived access so I'm thinking getting phone numbers this way is going to be more of a liability than a help.
* What should the web interface handle? 
  * Manually specifying a number to forward to for a `Location` (overriding duty calendar).
	-@smitau01 I think a manual override is a great idea but it needs to have a shutoff value set and a defult shutoff override.
  * Show current information - Locations, forwarding numbers, calendars, etc.
	-@smitau01 I'd say if there can be an "admin" dashboard of sorts that anyone with the top level admin login can see all the numbers in use and who they are set up to forward to at the present time.
	  Also if we can do some basic authentication stuff (maybe later once this is covered in class? otherwise I know a basic form of it would be pretty easy to implement so that each AHD or "location manager" can only edit or manually override for their location.

* Another thought is we'll want to make sure whatever chron job is set up to update it runs in sync with round time values (ie. 7:00, 7:15 etc NOT 7:03)

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
