from icalendar import Calendar
import urllib
import datetime


class DutyCalendar:
    def __init__(self, url):
        ''' url is a string ics URL '''
        self.url = url

    def getCurrentOnCall(self):
        ''' Should return a string list of names.
            This is assuming there could be more than
            one person on duty.
        '''
        on_duty_names = []

        curr_date = datetime.datetime.now().strftime("%Y-%m-%d")

        ics = urllib.urlopen(self.url).read()
        ical = Calendar.from_ical(ics)

        for vevent in ical.subcomponents:
            if vevent.name != "VEVENT":  # if it's not an event, ignore it
                continue

            start_date = vevent.get('DTSTART').dt.strftime("%Y-%m-%d")  # .dt is a datetime, start_date will be a string

            if(start_date == curr_date): # if this event is for today
                title = str(vevent.get('SUMMARY')) # this will be the title of the event (hopefully an RA name)
                on_duty_names.append(title)

        return on_duty_names

def testDutyCalendar():
    dc = DutyCalendar("http://www.google.com/calendar/ical/luther.edu_p5c373m13dppnsqeajcs4se5nc%40group.calendar.google.com/public/basic.ics")
    names = dc.getCurrentOnCall()
    print names

# testDutyCalendar()

