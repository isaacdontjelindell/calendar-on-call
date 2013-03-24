from icalendar import Calendar
import urllib
from datetime import date
import datetime
from django.utils import timezone
import time
import pytz

isResLife = False

#This is the current Brandt Duty Calender
#url = "http://www.google.com/calendar/ical/luther.edu_1qh57c21giu69npv6kj3vdihh0%40group.calendar.google.com/public/basic.ics";

#This is a fake Duty Calender for testing purposes
url = "http://www.google.com/calendar/ical/luther.edu_p5c373m13dppnsqeajcs4se5nc%40group.calendar.google.com/public/basic.ics";

ics = urllib.urlopen(url).read()

ical = Calendar.from_ical(ics)
for vevent in ical.subcomponents:
    print vevent
    #if vevent.name != "VEVENT":
    #    continue
    title = str(vevent.get('SUMMARY'))
    description = str(vevent.get('DESCRIPTION'))
    location = str(vevent.get('LOCATION'))
    start = vevent.get('DTSTART').dt      # a datetime
    end = vevent.get('DTEND').dt        # a datetime
    dtstamp = vevent.get('DTSTAMP').dt  #date time stamp
    print "Title: |" + title + "|"
    print "Start: ", start
    print "End: ", end
    hasTime = True
    try:
        eventStartTime = start.time()
        eventEndTime = end.time()
    except:
        hasTime = False
    if hasTime:
        #Create Another Function to Handle Time Specified Events
        print "This event HAS a TIME"
        if (eventStartTime <= datetime.datetime.now().time() and eventEndTime <= datetime.datetime.now().time()):
            print "THIS EVENT IS GOING ON NOW"
    if isResLife:
        startDuty = datetime.datetime(start.year, start.month, start.day, 19,0,0,0)
        endDuty = datetime.datetime(start.year, start.month, start.day + 1, 8,0,0,0)
        now = datetime.datetime.now()


        if (start <= now and startDuty <= now and endDuty > now):
            print "RESLIFE - ON DUTY: ", title


    print "DateTimeStamp: ", dtstamp
    print start.day == date.today().day

today = date.today()

#When Called Returns "Title Field" of Current On Call
def getCurrentOnCall(url):
    ics = urllib.urlopen(url).read()
    ical = Calendar.from_ical(ics)
    for vevent in ical.subcomponents:
        start = vevent.get('DTSTART').dt
        if start.day == date.today().day:
            title = str(vevent.get('SUMMARY'))
            description = str(vevent.get('DESCRIPTION'))
            location = str(vevent.get('LOCATION'))
            start = vevent.get('DTSTART').dt      # a datetime
            end = vevent.get('DTEND').dt        # a datetime
            hasTime = True
            try:
                eventTime = start.time()
            except:
                hasTime = False
            else:
                if start.time():
                    print "THIS EVENT HAS A TIME!"
            #if start.time
    return title

#print getCurrentOnCall(url)