calendar-on-call
================


TODO
-------
- [  ] create DutyCalendar
- [  ] create ContactList
- [  ] create Location
- [  ] create main/central control code
- [  ] web interface



Design
-------

|                      |                              |  
| -------------------- |------------------------------|
| `ForwardingNumber.py`| Class representing a Twilio number, and containing methods to change the forwarding destination. |
| `DutyCalendar.py`    | (name TBD). Class representing a Google Calendar, and containing methods to get current person on duty.|
| `ContactList.py`     | (name TBD). Class representing a Google contact list that will be used for number lookups.|
| `Location.py`        | (name TBD). Class representing a location (i.e. dorm). Maintains a `ForwardingNumber`, `DutyCalendar`, and `ContactList`, and contains methods to trigger updates.| 
| `main.py`            | (name TBD). Central control. Called periodically (cronjob?). Responsible for maintaining list of `Location` objects and calling update methods on them.|
| Web interface        | See Misc (below)|


Dependencies
----------
* pip install python-dateutil
* pip install icalendar


Misc
-------
* How do we want to handle contact lists? Should a separate contact list be created, either in a Google account or maintained internally by this program?
	-@smitau01 I'd say ultimently we should interface with google contacts and I can look into how difficult this will be but we could also have a contanct list maintained by the program.
* What should the web interface handle? 
  * Manually specifying a number to forward to for a `Location` (overriding duty calendar).
	-@smitau01 I think a manual override is a great idea but it needs to have a shutoff value set and a defult shutoff override.
  * Show current information - Locations, forwarding numbers, calendars, etc.
	-@smitau01 I'd say if there can be an "admin" dashboard of sorts that anyone with the top level admin login can see all the numbers in use and who they are set up to forward to at the present time.
	  Also if we can do some basic authentication stuff (maybe later once this is covered in class? otherwise I know a basic form of it would be pretty easy to implement so that each AHD or "location manager" can only edit or manually override for their location.

* Another thought is we'll want to make sure whatever chron job is set up to update it runs in sync with round time values (ie. 7:00, 7:15 etc NOT 7:03)