from icalendar import Calendar
import urllib
import pytz


class DutyCalendar:
    def __init__(self, url):
        ''' url is a string ics URL '''
        self.url = url



    def getCurrentOnCall(self):
        ''' Should return a string name '''
        ics = urllib.urlopen(self.url).read()
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
            print start
            print end
            print ""