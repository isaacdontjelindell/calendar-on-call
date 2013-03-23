from icalendar import Calendar
import urllib

# ical url (found in calendar settings)
url = "http://www.google.com/calendar/ical/luther.edu_jnpvad28dg0rerr8l0eq193su8%40group.calendar.google.com/public/basic.ics"

ics = urllib.urlopen(url).read()

ical = Calendar.from_ical(ics)
for vevent in ical.subcomponents:
    if vevent.name != "VEVENT":
        continue
    title = str(vevent.get('SUMMARY'))
    description = str(vevent.get('DESCRIPTION'))
    location = str(vevent.get('LOCATION'))
    start = vevent.get('DTSTART').dt      # a datetime
    end = vevent.get('DTEND').dt        # a datetime

    print title