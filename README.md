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


Misc
-------
* How do we want to handle contact lists? Should a separate contact list be created, either in a Google account or maintained internally by this program?
* What should the web interface handle? 
  * Manually specifying a number to forward to for a `Location` (overriding duty calendar).
  * Show current information - Locations, forwarding numbers, calendars, etc.
