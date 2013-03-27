from Location import Location
import json

info = {}

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
    with open('calendar-on-call', 'w') as outfile:
        json.dump(info, outfile)


setup()
dumpToFile()