from twilio.rest import TwilioRestClient
import datetime
from icalendar import Calendar
import urllib
from dateutil import tz

class Location:
    def __init__(self, info):
        self.info = info
        self.twilio_client = TwilioRestClient()
        self.forwarding_number_obj = self.twilio_client.phone_numbers.get(self.info["forwarding_number_id"])
        self.isResLife = info["isResLife"]

    def getInfo(self):
        return self.info

    def update(self):
        ''' checks for changes to the person on duty and makes necessary changes to forwarding info '''
        curr_forwarding_destination = self.getCurrentForwardingDestination()

        new_person_on_duty = self.getCurrentPersonOnDuty()[0] # TODO handle multiples
        new_forwarding_destination = self.info["contact_list"][new_person_on_duty]

        if not curr_forwarding_destination == new_forwarding_destination:
            self.updateForwardingDestination(new_forwarding_destination)

    def update2(self):
        ''' checks for changes to the person on duty and makes necessary changes to forwarding info '''
        curr_forwarding_destinations,failNum = self.getCurrentForwardingDestinations2()

        for name in self.getCurrentPersonsOnDuty2():
            new_person_on_duty = name
            new_forwarding_destinations = []
            new_forwarding_destinations.append(self.info["contact_list"][str(new_person_on_duty).strip().lower()])

        if not curr_forwarding_destinations == new_forwarding_destinations:
            self.updateForwardingDestinations2(new_forwarding_destinations, failNum)

    def updateForwardingDestination(self, new_destination_number):
        voice_URL = "http://twimlets.com/forward?PhoneNumber=" + new_destination_number + "&"
        self.forwarding_number_obj.update(voice_url=voice_URL)

    def updateForwardingDestinations2(self, new_destination_numbers, failNumber):
        voice_URL = "http://twimlets.com/simulring?"
        incrementNum = 0;
        for number in new_destination_numbers:
            voice_URL = voice_URL + "PhoneNumbers%5" + str(incrementNum) + "B%5D=" + number + "&"
            incrementNum = incrementNum + 1
        voice_URL = voice_URL + "http://twimlets.com/forward?PhoneNumber=" + failNumber + "&"
        self.forwarding_number_obj.update(voice_url=voice_URL)

    def getCurrentForwardingDestination(self):
        return self.forwarding_number_obj.voice_url.split("=")[1].strip("&")

    def getCurrentForwardingDestinations2(self): #Returns a tuple with the first element a list of simulring numbers
        #curently on call and the second item the fail number string
        current_numbers = []

        split_url = self.forwarding_number_obj.voice_url.split("=")
        for part in split_url:
            if str(part).__contains__("-"):
                current_numbers.append(part.split("&")[0])
        fail_number = current_numbers[current_numbers.__len__() - 1]
        current_numbers.pop(current_numbers.__len__() - 1)
        return (current_numbers, fail_number)

    def getCurrentPersonOnDuty(self):
        on_duty_names = []

        #curr_date = datetime.datetime.now() #.strftime("%Y-%m-%d")

        ics = urllib.urlopen(self.info["calendar_url"]).read()
        ical = Calendar.from_ical(ics)

        for vevent in ical.subcomponents:
            if vevent.name != "VEVENT":  # if it's not an event, ignore it
                continue

            start_date = vevent.get('DTSTART').dt #.strftime("%Y-%m-%d")  # .dt is a datetime or date
            end_date = vevent.get('DTEND').dt
            
            if(isinstance(start_date, datetime.datetime)):
                # it's a datetime.datetime object (includes time)
                start_date = start_date.astimezone(tz.tzlocal()) # convert to local time
                end_date = end_date.astimezone(tz.tzlocal())
                curr_date = datetime.datetime.now(tz.tzlocal())

            elif(isinstance(start_date, datetime.date)):
                # it's a datetime.date object (does not include time)
                curr_date = datetime.date.today()

            if(start_date <= curr_date <= end_date): # if this event is right now
                title = str(vevent.get('SUMMARY')) # this will be the title of the event (hopefully an RA name)
                on_duty_names.append(title)

        return on_duty_names

    def getCurrentPersonsOnDuty2(self):
        on_duty_names = []

        curr_date = datetime.datetime.now().strftime("%Y-%m-%d")

        ics = urllib.urlopen(self.info["calendar_url"]).read()
        ical = Calendar.from_ical(ics)

        for vevent in ical.subcomponents:
            if vevent.name != "VEVENT":  # if it's not an event, ignore it
                continue

            start_date = vevent.get('DTSTART').dt.strftime()  # .dt is a datetime, start_date will be a string

            start = vevent.get('DTSTART').dt + datetime.timedelta(hours=-5)     # a datetime
            end = vevent.get('DTEND').dt + datetime.timedelta(hours=-5)     # a datetime
            title = str(vevent.get('SUMMARY'))

            hasTime = True
            try:
                eventStartTime = start.time()
                eventEndTime = end.time()
            except:
                hasTime = False
            if hasTime:
                print "This event HAS a TIME"
                if (start.replace(tzinfo=None) <= datetime.datetime.now() and end.replace(tzinfo=None) >= datetime.datetime.now()):
                    on_duty_names.append(title)
            else:
                if (self.isResLife and not hasTime):
                    startDuty = datetime.datetime(start.year, start.month, start.day, 19,0,0,0)
                    endDuty = datetime.datetime(start.year, start.month, start.day + 1, 8,0,0,0)
                    if (datetime.datetime.now() >= startDuty and datetime.datetime.now() <= endDuty):
                        on_duty_names.append(title)
                    else:
                        on_duty_names.append("ResLife Office")
                else:
                    if(start_date == curr_date):
                        on_duty_names.append(title)

        return on_duty_names

def testLocation():
    calendar_url= "http://www.google.com/calendar/ical/luther.edu_p5c373m13dppnsqeajcs4se5nc%40group.calendar.google.com/public/basic.ics"
    forwarding_number_id = "PN3370cd26b57b0bf69e7bfce10c008a4b"

    contact_list = {}
    contact_list["Isaac DL"] = "612-978-3683"
    contact_list["Austen Smith"] = "319-743-8485"
    contact_list["ResLife Office"] = "563-387-1330"

    info = {}
    info["location_name"] = "Brandt Hall"
    info["calendar_url"] = calendar_url
    info["forwarding_number_id"] = forwarding_number_id
    info["contact_list"] = contact_list
    info["isResLife"] = True

    location = Location(info)
    location.getCurrentPersonOnDuty()
    
    location.update()
    print location.getCurrentForwardingDestination()



#testLocation()
